import psycopg2
import pandas as pd

# Tablas de sitios anatómicos
sitios = ['cervix', 'vagina', 'uterus', 'rectum', 'orine']

conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="postgres",
    host="localhost",
    port="5432"
)

for site in sitios:
    print(f"\n Verificando sitio: {site}")
    df = pd.read_sql_query(f"SELECT * FROM {site}", conn)
    micro_cols = [col for col in df.columns if col.startswith("x")]

    df_mother = pd.read_sql_query("SELECT index FROM mother", conn)
    mapped_indices = df_mother["index"].str.lower().tolist()

    # Detectar columnas xNN que no están mapeadas en mother
    faltantes = [x for x in micro_cols if x.lower() not in mapped_indices]

    if faltantes:
        print(f" {len(faltantes)} columnas xNN sin mapeo en mother:")
        print(", ".join(faltantes))
    else:
        print(" Todas las columnas xNN están correctamente mapeadas en mother.")

conn.close()
