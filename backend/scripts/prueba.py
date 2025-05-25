import psycopg2

# Parámetros de conexión
DB_PARAMS = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": "5432"
}

# Tablas que vamos a comprobar
TABLAS = ['cervix', 'orine', 'rectum', 'uterus', 'vagina']

# Conectar a la base de datos y verificar
conn = psycopg2.connect(**DB_PARAMS)
cur = conn.cursor()

for tabla in TABLAS:
    print(f"\n Verificando datos en tabla: {tabla}")
    try:
        # Seleccionar los primeros 5 registros
        cur.execute(f"SELECT * FROM {tabla} LIMIT 5;")
        rows = cur.fetchall()
        colnames = [desc[0] for desc in cur.description]
        print(f" Columnas: {colnames}")

        if not rows:
            print(" No hay registros en la tabla.")
        else:
            for idx, row in enumerate(rows):
                print(f"  Fila {idx + 1}:")
                for col, val in zip(colnames, row):
                    print(f"    {col}: {val}")

    except Exception as e:
        print(f"Error al consultar la tabla {tabla}: {e}")

cur.close()
conn.close()