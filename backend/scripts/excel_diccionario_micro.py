import pandas as pd

# Ruta al Excel original
excel_path = "../myapp/Rscripts/ENDORE_relab_0.01%_def_160525.xlsx"

# Leer todas las hojas
excel_file = pd.ExcelFile(excel_path)
micro_cols_global = set()

# Nombres de columnas que consideramos metadatos
metadatos = ["sample-id", "participant-id", "group", "age", "weight_kg", "height_m", "bmi", "lh"]

# Recorrer solo las hojas que corresponden a sitios anatómicos
sitios_validos = ["cervix", "uterus", "rectum", "vagina", "orine"]
sheets_filtradas = [s for s in excel_file.sheet_names if any(sitio in s.lower() for sitio in sitios_validos)]

for sheet in sheets_filtradas:
    df = excel_file.parse(sheet_name=sheet)
    df.columns = df.columns.str.strip()  

    # Excluir metadatos comparando en minúsculas
    micro_cols = [col for col in df.columns if col.lower() not in [m.lower() for m in metadatos]]
    micro_cols_global.update(micro_cols)

# Generar DataFrame de resumen
micro_cols_sorted = sorted(list(micro_cols_global))
df_micro = pd.DataFrame({
    "codigo": [f"x{i+1}" for i in range(len(micro_cols_sorted))],
    "nombre_original": micro_cols_sorted,
    "familia": ["" for _ in micro_cols_sorted],
    "genero": ["" for _ in micro_cols_sorted],
    "ena_id": ["" for _ in micro_cols_sorted],
    "ncbi_id": ["" for _ in micro_cols_sorted],
})

# Guardar a Excel
df_micro.to_excel("microorganismos_detectados_M.xlsx", index=False)
print(" Archivo generado: microorganismos_detectados_M.xlsx")
