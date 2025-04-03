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
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware import Middleware
#nuevo
from myapp.routes import analytics


models.Base.metadata.create_all(bind=engine)

app = FastAPI()
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

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#nuevo
app.include_router(analytics.router)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/file/{filename}")
def download_file(filename: str):
    # Verificar si el archivo existe en el directorio
    file_path = os.path.join("/app/myapp/files/", filename)
    if os.path.isfile(file_path):
        # Enviar el archivo al cliente
        return FileResponse(file_path, filename=filename)
    else:
        raise HTTPException(status_code=404, detail=f"El archivo {filename} no existe")


@app.get("/rscript/{uuid}")
def get_status_file(uuid: str):
    filename = "%s.png" % uuid
    file_path = os.path.join("/app/myapp/files/", filename)
    if os.path.isfile(file_path):
        return {uuid: 0} 
    else:
        raise HTTPException(status_code=404, detail=f"El archivo {filename} no existe")

@app.post("/rscript")
async def rscript( db: Session = Depends(get_db) ):
    random_uuid = uuid.uuid4()
    celery_app.send_task('myapp.tasks.r_script', args=(random_uuid,))        
    return {"rscript": random_uuid}


@app.get("/data/{table}")
async def data(table: str, db: Session = Depends(get_db) ):

    sites = ['cervix', 'uterus', 'rectum', 'vagina', 'orine']
    if table in sites:
      query = text(f"SELECT * FROM {table}")
      result = db.execute(query)
      column_names = result.keys()
      items = [dict(zip(column_names, row)) for row in result.fetchall()]
    else:
      query = text(f"SELECT * FROM mother")
      result = db.execute(query)
      column_names = result.keys()
      items = [dict(zip(column_names, row)) for row in result.fetchall()]
      items_mother = {}

      # Iterar sobre la lista original
      for item in items:
          index = item['index']
          values = [ item['family'], item['genero'], item['ena'], item['nhi'] ]
          items_mother[index] = values
      items = items_mother

    return items


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000 )

