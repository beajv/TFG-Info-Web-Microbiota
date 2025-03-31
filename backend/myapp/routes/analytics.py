from fastapi import APIRouter
import psycopg2
import pandas as pd

router = APIRouter()

@router.get("/analytics/abundancia-relativa")
def abundancia_relativa():
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="Arturo2019",
        host="localhost",
        port="5432"
    )
    df = pd.read_sql_query("SELECT * FROM vagina;", conn)
    conn.close()

    abundancias = df.filter(regex='^x')
    proporciones = abundancias.div(abundancias.sum(axis=1), axis=0)

    df['group'] = df['diseases'].apply(
        lambda x: 'Factor' if 'MALE_FACTOR' in str(x).upper() or 'TUBAL_FACTOR' in str(x).upper() else 'No Factor'
    )
    proporciones['group'] = df['group']
    abundancias_por_grupo = proporciones.groupby('group').mean().reset_index()

    return abundancias_por_grupo.to_dict(orient='records')
