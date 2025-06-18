import pandas as pd

# Ruta al archivo generado anteriormente
entrada = "microorganismos_detectados_M.xlsx"
salida = "microorganismos_detectados_con_nombre.xlsx"

# Cargar el archivo
df = pd.read_excel(entrada)

# Función para extraer el último nombre válido tras el último ';'
def extraer_nombre_final(cadena):
    if not isinstance(cadena, str):
        return ""
    partes = cadena.split(";")
    partes_limpias = [p.strip() for p in partes if p.strip() and p.strip() != "__"]
    return partes_limpias[-1] if partes_limpias else ""

# Aplicar la función a la columna de nombres originales
df["nombre_microorganismo"] = df["nombre_original"].apply(extraer_nombre_final)

# Guardar el nuevo Excel
df.to_excel(salida, index=False)

print(f" Archivo generado: {salida}")
