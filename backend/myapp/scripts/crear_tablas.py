import pandas as pd
import psycopg2

# Ruta al Excel
EXCEL_PATH = "../myapp/Rscripts/ENDORE_relab_0.01%_def_160525.xlsx"

# Datos conexión PostgreSQL
DB_PARAMS = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": "5432"
}

# Sitios que vamos a procesar
SITIOS = ['cervix', 'orine', 'rectum', 'uterus', 'vagina']
METADATOS = ["sample-id", "participant-id", "diseases", "age", "weight_kg", "height_m", "bmi", "lh"]

# Conexión a PostgreSQL
conn = psycopg2.connect(**DB_PARAMS)
cur = conn.cursor()

# Leer equivalencias desde mother
mother_query = "SELECT codigo, nombre_original FROM mother"
mother_df = pd.read_sql(mother_query, conn)
# Crear un diccionario que mapee nombres normalizados a su código x1, x2...
mapa_microbios = {}
for _, row in mother_df.iterrows():
    cod = row["codigo"]
    nombres = str(row["nombre_original"]).split(" /// ")
    for nombre in nombres:
        nombre_normalizado = nombre.strip().lower()
        mapa_microbios[nombre_normalizado] = cod


# Leer todas las hojas del Excel
excel = pd.ExcelFile(EXCEL_PATH)
sheets = excel.sheet_names
# Conexión a PostgreSQL
conn = psycopg2.connect(**DB_PARAMS)
cur = conn.cursor()

# BORRAR todas las tablas si ya existían (para evitar errores)
cur.execute("DROP TABLE IF EXISTS cervix, orine, rectum, uterus, vagina;")
conn.commit()

# Leer equivalencias desde mother
mother_query = "SELECT codigo, nombre_original FROM mother"

for sitio in SITIOS:
    hojas = [s for s in sheets if sitio in s.lower()]
    if not hojas:
        print(f" No se encontraron hojas para {sitio}")
        continue

    dfs = [excel.parse(h).copy() for h in hojas]
    for i in range(len(dfs)):
        dfs[i].columns = dfs[i].columns.str.strip().str.lower()

    df_final = pd.concat(dfs, ignore_index=True)
    # Filtrar condiciones no deseadas
    if "group" in df_final.columns:
        df_final = df_final[~df_final["group"].isin(["SOP", "ARTERIOVENOUS_MALFORMATION", "ADENOMIOSIS"])]
    elif "diseases" in df_final.columns:
        df_final = df_final[~df_final["diseases"].isin(["SOP", "ARTERIOVENOUS_MALFORMATION", "ADENOMIOSIS"])]

    #print(f"Columnas finales en {sitio}:", df_final.columns.tolist())
    
    # Renombrar columna 'group' → 'diseases' si existe
    if "group" in df_final.columns:
        df_final.rename(columns={"group": "diseases"}, inplace=True)

    # Separar columnas
    micro_cols = [col for col in df_final.columns if col not in METADATOS]
    meta_cols = [col for col in METADATOS if col in df_final.columns]

    print(f" {sitio.upper()} → Micro cols detectadas ({len(micro_cols)}):", micro_cols)

    # Generar diccionario original de renombrado
    renamed_cols = {}
    for col in micro_cols:
        clave = col.strip().lower()
        if clave in mapa_microbios:
            renamed_cols[col] = mapa_microbios[clave]

       # else:
        #    print(f" Microbio '{clave}' no está en mother y será descartado")

    print(f" {sitio.upper()} → {len(renamed_cols)} microbios mapeados a x-códigos")

    # Filtrar columnas duplicadas
    codigos_ya_usados = set()
    renamed_cols_filtrado = {}

    for original, codigo in renamed_cols.items():
        if codigo not in codigos_ya_usados:
            renamed_cols_filtrado[original] = codigo
            codigos_ya_usados.add(codigo)
        #else:
         #   print(f"Microbio '{original}' mapeado como '{codigo}' ya ha sido usado, se descarta")

    # Construir df final
    columnas_finales = meta_cols + list(renamed_cols_filtrado.keys())
    df_final = df_final[columnas_finales]
    df_final.rename(columns=renamed_cols_filtrado, inplace=True)

    print(f"Columnas en df_final ({sitio}):", df_final.columns.tolist())

    # Confirmación antes de insertar
    print(f" Muestras a insertar en '{sitio}': {df_final.shape[0]}")


    # Limpiar decimales
    # Normalizar separador decimal solo en microbios (columnas tipo x1, x2...)
    for col in renamed_cols_filtrado.values():
        if col in df_final.columns:
            df_final[col] = df_final[col].astype(str).str.replace(",", ".")
            df_final[col] = pd.to_numeric(df_final[col], errors='coerce')

    #df_final = df_final.applymap(lambda x: None if isinstance(x, str) and not x.replace('.', '', 1).isdigit() else x)

    # Crear tabla SQL
    columnas_sql = [f'"{col}"' for col in df_final.columns]
    tipos_sql = ["TEXT" if col in meta_cols else "REAL" for col in df_final.columns]

    cur.execute(f"DROP TABLE IF EXISTS {sitio};")
    create_sql = f"""
    CREATE TABLE {sitio} (
        {','.join(f'{c} {t}' for c, t in zip(columnas_sql, tipos_sql))}
    );
    """
    cur.execute(create_sql)
    conn.commit()

    # Insertar datos
    insert_sql = f"INSERT INTO {sitio} ({','.join(columnas_sql)}) VALUES ({','.join(['%s'] * len(columnas_sql))})"
    inserted = 0
    for _, row in df_final.iterrows():
        try:
            values = [None if pd.isna(v) else v for v in row]
            cur.execute(insert_sql, values)
            inserted += 1
        except Exception as e:
            print(f" Error al insertar: {e}")
    conn.commit()
    print(f" Insertadas {inserted} filas en {sitio}")

cur.close()
conn.close()
print("Todas las tablas han sido creadas y rellenadas correctamente.")
