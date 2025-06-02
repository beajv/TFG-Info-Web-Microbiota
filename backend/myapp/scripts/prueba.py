import psycopg2

# Parámetros de conexión
conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="postgres",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# Lista de sitios que queremos inspeccionar
sitios = ['cervix', 'orine', 'rectum', 'uterus', 'vagina']

for sitio in sitios:
    print(f"\nTabla: {sitio}")
    try:
        cur.execute("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name = %s
            ORDER BY ordinal_position;
        """, (sitio,))
        columnas = cur.fetchall()
        columnas = [col[0] for col in columnas]
        print("Columnas:", columnas)
    except Exception as e:
        print(f"  ❌ Error accediendo a {sitio}: {e}")

cur.close()
conn.close()
