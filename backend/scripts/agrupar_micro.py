import pandas as pd

# Cargar el archivo ya estandarizado
ruta_entrada = "microorganismos_coloreado.xlsx"
df = pd.read_excel(ruta_entrada)

# Agrupar por nombre estandarizado (que ya tiene Actinobaculum, Prevotella.7, etc.)
df_ordenado = df.sort_values(by="nombre_limpio")

# Asignar un nuevo código único por nombre estandarizado
df_ordenado["nuevo_codigo"] = (
    df_ordenado["nombre_limpio"]
    .astype(str)
    .rank(method="dense")
    .astype(int)
    .map(lambda i: f"x{i}")
)

# Guardar el archivo con los nuevos códigos
ruta_salida = "microorganismos_unificados.xlsx"
df_ordenado.to_excel(ruta_salida, index=False)

print(f" Archivo generado: {ruta_salida}")
