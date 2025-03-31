import psycopg2
import pandas as pd
from scipy.stats import entropy
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Conexión a PostgreSQL
conn = psycopg2.connect(
    dbname="postgres",       
    user="postgres",         # estándar
    password="Arturo2019",  # pon la tuya
    host="localhost",
    port="5432"
)

# 2. Consulta SQL
query = """
SELECT * FROM vagina;
"""

# 3. Leer datos a DataFrame
df = pd.read_sql_query(query, conn)

# 4. Cerramos conexión
conn.close()

# 5. Revisar qué columnas tenemos
print(df.columns)

# Seleccionar solo las columnas tipo 'x' (las abundancias)
abundancias = df.filter(regex='^x')

# Normalizamos las abundancias a proporciones por muestra
proporciones = abundancias.div(abundancias.sum(axis=1), axis=0)

# Añadimos la columna de grupo
df['group'] = df['diseases'].apply(
    lambda x: 'Factor' if 'MALE_FACTOR' in str(x).upper() or 'TUBAL_FACTOR' in str(x).upper() else 'No Factor'
)

# Unimos proporciones con grupo
proporciones['group'] = df['group']

# Agrupamos por grupo y calculamos la media de abundancia relativa por género
abundancias_por_grupo = proporciones.groupby('group').mean().reset_index()

# Mostramos el DataFrame final
print(abundancias_por_grupo)