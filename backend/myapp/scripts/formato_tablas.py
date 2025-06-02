import pandas as pd
import psycopg2

DB_PARAMS = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": "5432"
}

sitios = ['cervix', 'vagina', 'uterus', 'rectum', 'orine']
excel_path = "../myapp/Rscripts/ENDORE_relab_0.01%_def_160525.xlsx"

conn = psycopg2.connect(**DB_PARAMS)
cur = conn.cursor()

for sitio in sitios:
    print(f"\n Creando tabla `{sitio}`...")

    df_old = pd.read_excel(excel_path, sheet_name=sitio)
    df_new = pd.read_excel(excel_path, sheet_name=f"{sitio}_new")
    df = pd.concat([df_old, df_new], ignore_index=True)

    df.columns = df.columns.str.strip().str.lower()

    col_renames = {
        "sample-id": "sample_id",
        "participant-id": "participant_id",
        "group": "diseases"
    }
    df.rename(columns=col_renames, inplace=True)

    tax_cols = [c for c in df.columns if c not in ["sample_id", "participant_id", "diseases", "age", "weight_kg", "height_m", "bmi", "lh"]]
    tax_cols_sorted = sorted(tax_cols)
    tax_map = {tax: f"x{i+1}" for i, tax in enumerate(tax_cols_sorted)}
    df.rename(columns=tax_map, inplace=True)

    columnas_sql = []
    for col in df.columns:
        if col.startswith("x"):
            columnas_sql.append(f'"{col}" FLOAT')
        elif col in ["sample_id", "participant_id", "diseases"]:
            columnas_sql.append(f'"{col}" TEXT')
        else:
            columnas_sql.append(f'"{col}" FLOAT')

    sql_create = f'DROP TABLE IF EXISTS "{sitio}";\nCREATE TABLE "{sitio}" (\n  {", ".join(columnas_sql)}\n);'

    try:
        cur.execute(sql_create)
        conn.commit()
        print(f"Tabla `{sitio}` creada correctamente con {len(df.columns)} columnas")
    except Exception as e:
        print(f" Error creando tabla {sitio}:", e)

cur.close()
conn.close()
print("\n Todas las tablas fueron creadas correctamente.")
