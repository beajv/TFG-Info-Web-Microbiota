import psycopg2

# Parámetros de conexión a PostgreSQL
DB_PARAMS = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": "5432"
}

# Conectar y obtener nombres de columnas de la tabla 'cervix'
conn = psycopg2.connect(**DB_PARAMS)
cur = conn.cursor()

cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'cervix';")
columns = cur.fetchall()

print(" Columnas reales de la tabla 'cervix':")
for col in columns:
    print(" -", col[0])

cur.close()
conn.close()
