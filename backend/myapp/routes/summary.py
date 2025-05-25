from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from myapp.config import SessionLocal

router = APIRouter()

# Función para obtener la conexión a la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/summary")
def get_summary(db: Session = Depends(get_db)):
    summary = {}

    # Contar microorganismos distintos en tabla mother
    micro_query = text("SELECT COUNT(*) FROM mother")
    summary["microbes"] = db.execute(micro_query).scalar()

    # Sitios definidos manualmente (los mismos que usas en /data/{site})
    sites = ['cervix', 'uterus', 'rectum', 'vagina', 'orine']
    summary["sites"] = len(sites)

    # Contar condiciones distintas (en cualquier tabla de sitio)
    conditions = set()
    for site in sites:
        if site == "mother":
            continue
        result = db.execute(text(f"""
            SELECT DISTINCT diseases 
            FROM {site}
            WHERE diseases  IS NOT NULL 
        """))
        conditions.update([row[0] for row in result if row[0]])

    summary["conditions"] = len(conditions)

    return summary

