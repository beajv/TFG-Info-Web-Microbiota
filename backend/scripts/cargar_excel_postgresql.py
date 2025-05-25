import pandas as pd
import psycopg2

# Ruta al nuevo Excel 
excel_path = "../myapp/Rscripts/ENDORE_relab_0.01%_def_160525.xlsx"

# Sitios anatómicos que queremos procesar
sitios = ['cervix', 'orine', 'rectum', 'uterus', 'vagina']

# Parámetros de conexión
DB_PARAMS = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": "5432"
}

# Leer todas las hojas disponibles
excel_file = pd.ExcelFile(excel_path)
available_sheets = excel_file.sheet_names

# Conexión a PostgreSQL
conn = psycopg2.connect(**DB_PARAMS)
cur = conn.cursor()

for site in sitios:
    print(f"\n Procesando sitio: {site}")

    # Unir hojas site + site_new (si existen)
    df_parts = []
    for name in [site, f"{site}_new"]:
        if name in available_sheets:
            df_parts.append(excel_file.parse(sheet_name=name))
    
    if not df_parts:
        print(f"  No se encontraron hojas para {site}")
        continue

    df = pd.concat(df_parts, ignore_index=True)

    # Normalizar nombres de columnas
    df.columns = df.columns.str.lower().str.strip()

    # Renombrar columnas clave
    col_renames = {
        "sample-id": "sample_id",
        "participant-id": "participant_id",
        "group": "diseases"
    }
    df.rename(columns={k.lower(): v for k, v in col_renames.items()}, inplace=True)

    # Detectar columnas taxonómicas (todo lo que no sea metadato)
    metadatos = ["sample_id", "participant_id", "diseases", "age", "weight_kg", "height_m", "bmi", "lh"]
    tax_columns = [col for col in df.columns if col not in metadatos]
    tax_columns_sorted = sorted(tax_columns)

    # Renombrar columnas microbianas a x1, x2, ...
    tax_map = {tax_col: f"x{i+1}" for i, tax_col in enumerate(tax_columns_sorted)}
    df.rename(columns=tax_map, inplace=True)

    # Reordenar columnas
    ordered_cols = [f"x{i}" for i in range(1, 51)] + [
        "age", "weight_kg", "height_m", "bmi", "lh",
        "participant_id", "diseases", "sample_id"
    ]
    df = df[[col for col in ordered_cols if col in df.columns]]

    # Limpieza: comas decimales, a punto y conversión a numérico si posible
    for col in df.columns:
        if df[col].dtype == object:
            df[col] = df[col].astype(str).str.replace(",", ".")
            df[col] = pd.to_numeric(df[col], errors='ignore')  # deja strings si no puede convertir

    # Reemplazar valores no numéricos por None (si quedan)
    df = df.applymap(lambda x: None if isinstance(x, str) and not x.replace('.', '', 1).isdigit() else x)

    # Preparar inserción SQL
    columnas_sql = [f'"{col}"' for col in df.columns]
    insert_sql = f"INSERT INTO {site} ({','.join(columnas_sql)}) VALUES ({','.join(['%s'] * len(columnas_sql))})"

    # Borrar contenido anterior
    cur.execute(f"DELETE FROM {site};")
    conn.commit()
    print(f"  Eliminados datos anteriores de `{site}`")

    # Insertar nuevos registros
    inserted = 0
    for _, row in df.iterrows():
        try:
            values = [None if pd.isna(v) else v for v in row]
            cur.execute(insert_sql, tuple(values))
            inserted += 1
        except Exception as e:
            print(f" Error en sample_id {row.get('sample_id', '???')}: {e}")

    conn.commit()
    print(f"   Insertadas {inserted} filas en `{site}`")

# Cerrar conexión
cur.close()
conn.close()
print("\n Todos los sitios fueron cargados correctamente.")
