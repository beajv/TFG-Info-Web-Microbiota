import psycopg2
import pandas as pd
from skbio.diversity.alpha import shannon


def calcular_shannon_por_site(site: str):
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="Arturo2019",
        host="localhost",
        port="5432"
    )

    query = f"SELECT * FROM {site};"
    df = pd.read_sql_query(query, conn)
    conn.close()

    abundancias = df.filter(regex='^x')
    df['shannon'] = abundancias.apply(shannon, axis=1)

    resumen_muestra = df[['sample_id', 'diseases', 'shannon']]
    resumen_enfermedad = df.groupby('diseases')['shannon'].agg(['mean', 'std', 'count']).reset_index()

    return resumen_muestra, resumen_enfermedad
