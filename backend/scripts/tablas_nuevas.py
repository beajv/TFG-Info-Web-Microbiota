
import pandas as pd
import psycopg2

# Ruta al Excel actualizado
excel_path = "../myapp/Rscripts/ENDORE_relab_0.01%_def_160525.xlsx"
sitios = ['cervix', 'vagina', 'uterus', 'rectum', 'orine']

# Parámetros conexión
conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="postgres",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

for site in sitios:
    print(f"Procesando sitio: {site}")
    df_old = pd.read_excel(excel_path, sheet_name=site)
    df_new = pd.read_excel(excel_path, sheet_name=f"{site}_new")
    df = pd.concat([df_old, df_new], ignore_index=True)

    # Normalizar nombres
    df.columns = df.columns.str.strip().str.lower()
    
    # Eliminar columnas no usadas (por nombre exacto o aproximado)

    df = df[[col for col in df.columns if col.strip().lower() not in ["favorable/patología", "grupos más escpecíficos", "grupos mas escpecificos"] and not ("grupo" in col.lower() and "especific" in col.lower())]]


    df.rename(columns={
        "sample-id": "sample_id",
        "participant-id": "participant_id",
        "group": "diseases"
    }, inplace=True)

    # Renombrar taxonómicos como xNN
    cols_tax = [col for col in df.columns if col not in ["sample_id", "participant_id", "diseases", "age", "weight_kg", "height_m", "bmi", "lh"]]
    cols_tax_sorted = sorted(cols_tax)
    map_tax = {col: f"x{i+1}" for i, col in enumerate(cols_tax_sorted)}
    df.rename(columns=map_tax, inplace=True)

    # Reordenar
    ordered_cols = [f"x{i}" for i in range(1, len(map_tax) + 1)] + ["age", "weight_kg", "height_m", "bmi", "lh", "participant_id", "diseases", "sample_id"]
    df = df[[col for col in ordered_cols if col in df.columns]]

    # Crear tabla desde cero (sin borrar datos)
    cols_sql = []
    for col in df.columns:
        if col.startswith("x") or col in ["age", "weight_kg", "height_m", "bmi", "lh"]:
            cols_sql.append(f'"{col}" DOUBLE PRECISION')
        else:
            cols_sql.append(f'"{col}" TEXT')

    sql_create = f'CREATE TABLE IF NOT EXISTS {site} ({", ".join(cols_sql)});'
    cur.execute(sql_create)
    conn.commit()
    print(f"  Tabla `{site}` preparada")

    # Insertar datos
    col_escaped = [f'"{col}"' for col in df.columns]
    insert_sql = f'INSERT INTO {site} ({",".join(col_escaped)}) VALUES ({",".join(["%s"]*len(col_escaped))})'
    for _, row in df.iterrows():
        values = []
        for x in row:
            try:
                x = float(str(x).replace(",", "."))
            except:
                if pd.isna(x):
                    x = None
            values.append(x)
        try:
            cur.execute(insert_sql, tuple(values))
        except Exception as e:
            print(f"   Error al insertar fila: {e}")
    conn.commit()
    print(f"   Insertadas {len(df)} filas en `{site}`")

cur.close()
conn.close()
print(" Todo finalizado correctamente.")
