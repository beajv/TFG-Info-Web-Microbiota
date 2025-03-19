from celery import Celery
from celery.schedules import crontab
import os
import datetime



# Configuración de Celery
redis_url = "redis://redis:6379/0"  # URL de conexión a Redis
celery_app = Celery('myapp', broker=redis_url, backend=redis_url)

# Configura el programa de tareas periódicas en Celery
celery_app.conf.beat_schedule = {
    'task-name': {
        'task': 'myapp.celery.delete_files_rscript_tmp',
        'schedule': crontab(minute='*/15'),  # Ejecutar cada 15 minutos
    },
}


#configura el auto-descubrimiento de tareas
celery_app.autodiscover_tasks(['myapp'])

# Configuración de las tareas periódicas
@celery_app.task
def delete_files_rscript_tmp():
    directorio = '/app/myapp/files'
    
    # Obtenemos la hora actual
    hora_actual = datetime.datetime.now()
    
    # Iteramos sobre los archivos en el directorio
    for archivo in os.listdir(directorio):
        ruta_completa = os.path.join(directorio, archivo)
    
        # Verificamos si el archivo es un archivo regular (no un directorio)
        if os.path.isfile(ruta_completa):
            # Obtenemos la fecha de modificación del archivo
            fecha_modificacion = datetime.datetime.fromtimestamp(os.path.getmtime(ruta_completa))
    
            # Calculamos la diferencia de tiempo en minutos
            diferencia_minutos = (hora_actual - fecha_modificacion).total_seconds() / 60
    
            # Si la diferencia es mayor a 5 minutos, borramos el archivo
            if diferencia_minutos > 5:
                os.remove(ruta_completa)
                print(f"El archivo {archivo} ha sido eliminado.")
