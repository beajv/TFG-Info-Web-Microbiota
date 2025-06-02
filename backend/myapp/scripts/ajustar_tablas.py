import psycopg2

DB_PARAMS = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": "5432"
}

conn = psycopg2.connect(**DB_PARAMS)
cur = conn.cursor()

tablas = ['cervix', 'orine', 'rectum', 'uterus', 'vagina']
columnas_a_real = ['age', 'weight_kg', 'height_m', 'bmi', 'lh']

for tabla in tablas:
    for col in columnas_a_real:
        try:
            cur.execute(f'ALTER TABLE {tabla} ALTER COLUMN {col} TYPE REAL USING {col}::REAL;')
        except Exception as e:
            print(f"  No se pudo cambiar {col} en {tabla}: {e}")

    for i in range(1, 51):
        try:
            cur.execute(f'ALTER TABLE {tabla} ADD COLUMN IF NOT EXISTS x{i} REAL;')
        except Exception as e:
            print(f"  No se pudo crear x{i} en {tabla}: {e}")

conn.commit()
cur.close()
conn.close()
print("Tablas ajustadas correctamente.")
