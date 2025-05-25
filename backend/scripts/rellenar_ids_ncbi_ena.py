import pandas as pd
import time
import requests
from urllib.parse import quote

# Ruta del archivo original
input_file = "microorganismos_unificados.xlsx"
output_file = "microorganismos_detectados_con_ids.xlsx"

# Cargar Excel
df = pd.read_excel(input_file)

# Añadir columnas vacías si no existen
if "ncbi_id" not in df.columns:
    df["ncbi_id"] = ""
if "ena_id" not in df.columns:
    df["ena_id"] = ""

# Función para obtener el tax_id de NCBI
def get_tax_id(nombre):
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        "db": "taxonomy",
        "term": nombre,
        "retmode": "json"
    }
    try:
        r = requests.get(base_url, params=params)
        r.raise_for_status()
        data = r.json()
        id_list = data.get("esearchresult", {}).get("idlist", [])
        if id_list:
            return id_list[0]
    except Exception as e:
        print(f"Error con {nombre}: {e}")
    return ""

# Rellenar IDs
for i, row in df.iterrows():
    nombre = str(row["nombre_limpio"])
    print(f"Buscando ID para: {nombre}")
    tax_id = get_tax_id(nombre)
    df.at[i, "ncbi_id"] = tax_id
    df.at[i, "ena_id"] = tax_id  # ENA usa los mismos tax_id
    time.sleep(0.3)  # Evita peticiones muy rápidas

# Guardar resultado
df.to_excel(output_file, index=False)
print(f"\nArchivo guardado como: {output_file}")
