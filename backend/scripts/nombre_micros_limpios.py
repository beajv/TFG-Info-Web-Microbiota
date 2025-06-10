import pandas as pd

# Ruta al archivo
entrada = "microorganismos_detectados_con_nombre.xlsx"
salida = "microorganismos_detectados_limpio.xlsx"

# Cargar Excel
df = pd.read_excel(entrada)

def extraer_limpio_v2(nombre):
    if not isinstance(nombre, str) or nombre.strip() == "":
        return ""
    partes = nombre.strip().split(";")
    # Tomamos la última parte no vacía
    for parte in reversed(partes):
        tokens = parte.split("_")
        if len(tokens) > 1:
            return tokens[-1]
        elif parte.strip():
            return parte.strip()
    return ""

# Aplicar función
df["nombre_limpio"] = df["nombre_microorganismo"].apply(extraer_limpio_v2)

# Guardar nuevo Excel
df.to_excel(salida, index=False)
print(f" Archivo generado: {salida}")
