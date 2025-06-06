from fastapi import FastAPI, UploadFile, File, Request, HTTPException, Response, Depends
from starlette.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
from .celery import celery_app
import myapp.models as models 
from myapp.config import engine
import myapp.crud as crud
from sqlalchemy.orm import Session
from myapp.config import SessionLocal
from sqlalchemy import text
import uuid
# Middlewares adicionales 
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware import Middleware
# Rutas de análisis y funciones auxiliares
from myapp.routes import analytics
from myapp.services.analytics import calcular_abundancias_por_disease
from myapp.routes import search
from myapp.routes import summary

import math


import time
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from myapp.config import DATABASE_URL  

import logging
logging.basicConfig(level=logging.INFO)

# Esperar a que la base de datos esté lista
for i in range(10):
    try:
        with engine.connect() as conn:
            print("Conectado a PostgreSQL.")
            break
    except OperationalError:
        print(" Esperando a que PostgreSQL esté listo...")
        time.sleep(3)
else:
    raise Exception(" No se pudo conectar a PostgreSQL después de varios intentos.")


#Inicializa las tablas si no existen
models.Base.metadata.create_all(bind=engine)

#Inicializa la instancia de FastAPI
app = FastAPI()

##
# @brief Lista de orígenes permitidos para CORS
#
origins = [
    "http://5.134.119.124",
    "https://5.134.119.124",
    "http://5.134.119.124:5173",
    "https://5.134.119.124:5173",
    "http://5.134.119.124:8000",
    "https://5.134.119.124:8000",
    "http://192.168.1.137:8080",
    "http://192.168.1.137:5173",
    "http://localhost:8080",  # Si también estás trabajando en localhost
    "http://localhost:5173",
    "http://localhost:8000"
]

##
# @brief Middleware CORS que permite comunicación frontend-backend.
#
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Importa y registra las rutas de análisis (gráficos, índice de Shannon, etc.)
app.include_router(analytics.router)
app.include_router(search.router)
app.include_router(summary.router)


##
# @brief Generador de sesiones de base de datos para ser usadas en endpoints protegidos por Depends.
#
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

##
# @brief Descarga un archivo generado por R u otro backend.
# @param filename Nombre del archivo a recuperar.
# @return FileResponse con el archivo solicitado o error 404 si no existe.
#
@app.get("/file/{filename}")
def download_file(filename: str):
    # Verificar si el archivo existe en el directorio
    file_path = os.path.join("/app/myapp/files/", filename)
    if os.path.isfile(file_path):
        # Enviar el archivo al cliente
        return FileResponse(file_path, filename=filename)
    else:
        raise HTTPException(status_code=404, detail=f"El archivo {filename} no existe")

##
# @brief Verifica si existe un archivo generado por R en formato imagen.
# @param uuid Identificador del archivo.
# @return Diccionario con {uuid: 0} si existe o error 404 si no.
#
@app.get("/rscript/{uuid}")
def get_status_file(uuid: str):
    filename = "%s.png" % uuid
    file_path = os.path.join("/app/myapp/files/", filename)
    if os.path.isfile(file_path):
        return {uuid: 0} 
    else:
        raise HTTPException(status_code=404, detail=f"El archivo {filename} no existe")

##
# @brief Lanza una tarea asíncrona de RScript a través de Celery.
# @return Diccionario con el UUID asignado a la tarea.
#
@app.post("/rscript")
async def rscript( db: Session = Depends(get_db) ):
    random_uuid = uuid.uuid4()
    celery_app.send_task('myapp.tasks.r_script', args=(random_uuid,))        
    return {"rscript": random_uuid}

##
# @brief Devuelve datos de una tabla específica (site o tabla mother).
# @param table Nombre de la tabla a consultar.
# @return Lista de diccionarios con los datos o estructura por índice si es mother.
#
@app.get("/data/{table}")
async def data(table: str, db: Session = Depends(get_db) ):

    sites = ['cervix', 'uterus', 'rectum', 'vagina', 'orine']
    if table in sites:
      query = text(f"SELECT * FROM {table}")
      with engine.connect() as connection:
        result = connection.execute(query)

      
      column_names = result.keys()
      
      def limpiar_nan(obj):
        return {k: (v if not isinstance(v, float) or not math.isnan(v) else None) for k, v in obj.items()}

      items = [limpiar_nan(dict(zip(column_names, row))) for row in result.fetchall()]

    else:
        query = text("SELECT * FROM mother")
        result = db.execute(query)
        items_mother = {}
        for row in result.fetchall():
            item = dict(zip(result.keys(), row))
            codigo = item.get("codigo")
            values = [
                item.get("nombre_microorganismo", ""),        # [0] - nombre taxonómico original
                item.get("nombre_limpio", ""),  # [1] - nombre limpio que muestra en frontend
                item.get("ena_id", ""),
                item.get("ncbi_id", "")
            ]
            if codigo:
                items_mother[codigo] = values
        items = items_mother



    return items



# Código de prueba
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000 )

