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
    lambda x: '1' if 'MALE_FACTOR' in str(x).upper() or 'TUBAL_FACTOR' in str(x).upper() else '2'
)

# Unimos proporciones con grupo
proporciones['group'] = df['group']

# Agrupamos por grupo y calculamos la media de abundancia relativa por género
abundancias_por_grupo = proporciones.groupby('group').mean().reset_index()

# Mostramos el DataFrame final
print(abundancias_por_grupo)

from skbio.diversity.alpha import shannon

# Calculamos el índice de Shannon para cada muestra (fila del DataFrame de abundancias)
diversidades_alpha = abundancias.apply(shannon, axis=1)

# Añadimos la columna al DataFrame original
df['shannon'] = diversidades_alpha

# Visualizamos un resumen por grupo
resumen_shannon = df.groupby('group')['shannon'].describe()
print(resumen_shannon)


# Boxplot para comparar la diversidad alpha entre grupos
#plt.figure(figsize=(8, 5))
#sns.boxplot(data=df, x='group', y='shannon', palette='Set2')
#plt.title('Diversidad Alpha (Shannon) por Grupo')
#plt.xlabel('Grupo')
#plt.ylabel('Índice de Shannon')
#plt.tight_layout()
#plt.savefig("diversidad_alpha_boxplot.png")  # Guarda la imagen
#plt.show()
