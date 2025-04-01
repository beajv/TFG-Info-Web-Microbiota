from fastapi import APIRouter, Query
import psycopg2
import pandas as pd
from skbio.diversity.alpha import shannon

router = APIRouter()

@router.get("/shannon")
def calcular_shannon(site: str = Query(...)):
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="Arturo2019",
        host="localhost",
        port="5432"
    )

    # Seguridad básica: evitar SQL injection validando el nombre
    tablas_validas = ["vagina", "cervix", "uterus", "rectum", "orine"]
    if site not in tablas_validas:
        return {"error": "Nombre de tabla no permitido."}

    query = f"SELECT * FROM {site};"
    df = pd.read_sql_query(query, conn)
    conn.close()

    abundancias = df.filter(regex='^x')
   # proporciones = abundancias.div(abundancias.sum(axis=1), axis=0)
    df['shannon'] = abundancias.apply(shannon, axis=1)

    resultados = df[['sample_id', 'diseases', 'shannon']].to_dict(orient='records')
    return resultados
