import psycopg2
import pandas as pd
from skbio.diversity.alpha import shannon

##
# Calcula el índice de Shannon para cada muestra en un sitio anatómico distinto
# 
def calcular_shannon_por_site(site: str):
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432"
    )

    query = f"SELECT * FROM {site};"
    df = pd.read_sql_query(query, conn)
    conn.close()

    print("ESTO ES !!!!: " , df.head())

    abundancias = df.filter(regex='^x')
    df['shannon'] = abundancias.apply(shannon, axis=1)

    resumen_muestra = df[['sample_id', 'diseases', 'shannon']]
    resumen_enfermedad = df.groupby('diseases')['shannon'].agg(['mean', 'std', 'count']).reset_index()

    return resumen_muestra, resumen_enfermedad

##
# Calcula la abundancia media por enfermedad en un sitio anatómico
# 
def calcular_abundancias_por_disease(site: str):
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432"
    )
    query = f"SELECT * FROM {site};"
    df = pd.read_sql_query(query, conn)
    conn.close()

    abundancias = df.filter(regex='^x')
    df_abund = pd.concat([df[['diseases']], abundancias], axis=1)

    resumen = df_abund.groupby('diseases').mean().reset_index()
    return resumen.to_dict(orient='records')  #para pasar al frontend como JSON

# Código de prueba
if __name__ == "__main__":
    resultado = calcular_abundancias_por_disease("vagina")
    from pprint import pprint
    pprint(resultado[:3])  # Solo los 3 primeros grupos para no saturar

