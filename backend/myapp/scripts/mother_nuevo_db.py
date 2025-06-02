import pandas as pd
import psycopg2

# Leer Excel original
df = pd.read_excel("microorganismos_detectados_con_ids.xlsx")

# Agrupar por 'codigo' y combinar sin confundir con el carácter ;
df_agrupado = df.groupby("codigo", as_index=False).agg({
    "nombre_original": lambda x: " /// ".join(sorted(set(str(i) for i in x if pd.notna(i)))),
    "nombre_microorganismo": lambda x: " /// ".join(sorted(set(str(i) for i in x if pd.notna(i)))),
    "nombre_limpio": "first",
    "ena_id": "first",
    "ncbi_id": "first"
})

# Guardar para revisar
df_agrupado.to_excel("microorganismos_unificado.xlsx", index=False)
print("Excel generado: microorganismos_unificado.xlsx")

# Cargar en PostgreSQL
conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="postgres",
    host="db",
    port="5432"
)
cur = conn.cursor()

# Crear tabla mother
cur.execute("DROP TABLE IF EXISTS mother;")
cur.execute("""
    CREATE TABLE mother (
        codigo TEXT PRIMARY KEY,
        nombre_original TEXT,
        nombre_microorganismo TEXT,
        nombre_limpio TEXT,
        ena_id TEXT,
        ncbi_id TEXT
    );
""")

# Insertar
for _, row in df_agrupado.iterrows():
    cur.execute("""
        INSERT INTO mother (codigo, nombre_original, nombre_microorganismo, nombre_limpio, ena_id, ncbi_id)
        VALUES (%s, %s, %s, %s, %s, %s);
    """, (
        str(row["codigo"]),
        str(row["nombre_original"]),
        str(row["nombre_microorganismo"]),
        str(row["nombre_limpio"]),
        str(int(row["ena_id"])) if pd.notna(row["ena_id"]) else None,
        str(int(row["ncbi_id"])) if pd.notna(row["ncbi_id"]) else None

    ))

conn.commit()
cur.close()
conn.close()
print(" Tabla mother creada e insertada correctamente.")
