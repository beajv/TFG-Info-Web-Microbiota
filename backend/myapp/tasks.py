from celery import shared_task
import os
from myapp.config import SessionLocal
from contextlib import contextmanager

@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@shared_task
def r_script(uuid):

    cmd = "Rscript --vanilla /app/myapp/Rscripts/RPCACERVIX.R -f /app/myapp/Rscripts/ENDORE_relab_0.01.xlsx -o /app/myapp/files/%s.png" % uuid 
    os.system(cmd)


