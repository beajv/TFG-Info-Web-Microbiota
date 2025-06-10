import pandas as pd
import psycopg2

conn = psycopg2.connect(
    dbname="postgres", user="postgres", password="postgres", host="localhost", port="5432"
)

# Cargar datos cervix + mother
df = pd.read_sql_query("SELECT * FROM cervix", conn)
df_mother = pd.read_sql_query("SELECT * FROM mother", conn)
conn.close()

#  Filtrar solo columnas tipo xNN
cols_micro = [col for col in df.columns if col.startswith("x")]
df_largo = df.melt(id_vars=["sample_id", "diseases"], value_vars=cols_micro,
                   var_name="micro", value_name="abundance")

# Normalizar
df_largo["micro"] = df_largo["micro"].astype(str).str.lower().str.strip()
df_mother["index"] = df_mother["index"].astype(str).str.lower().str.strip()

# Unir con tabla mother
df_merged = df_largo.merge(df_mother, how="left", left_on="micro", right_on="index")

# Asignar nombre visible
df_merged["nombre_mostrado"] = df_merged["genero"]
df_merged.loc[df_merged["nombre_mostrado"].isna(), "nombre_mostrado"] = df_merged["micro"]

# Asegurar numeric
df_merged["abundance"] = pd.to_numeric(df_merged["abundance"], errors="coerce")

# Agrupar por género
resumen = df_merged.groupby("nombre_mostrado")["abundance"].mean().sort_values(ascending=False)

print("\n Top 10 géneros por abundancia media en CERVIX:")
print(resumen.head(10))
