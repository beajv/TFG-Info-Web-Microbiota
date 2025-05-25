import psycopg2
import pandas as pd
from skbio.diversity.alpha import shannon
from skbio.diversity import beta_diversity
from skbio.stats.ordination import pcoa
import numpy as np
from myapp.config import engine
##
#   Carga los datos de abundancia microbiana desde la base de datos PostgreSQL.
#   @param site: Nombre del sitio anatómico (por ejemplo, 'cervix', 'vagina', etc.)
#   @return: DataFrame con las filas de la tabla correspondiente.
#   
def cargar_abundancias(site: str):
    query = f"SELECT * FROM {site};"
    df = pd.read_sql_query(query, engine)
    return df




##
# Calcula el índice de Shannon para cada muestra en un sitio anatómico distinto
# 
def calcular_shannon_por_site(site: str):
    query = f"SELECT * FROM {site};"
    df = pd.read_sql_query(query, engine)

    abundancias = df.filter(regex='^x')
    abundancias = abundancias.apply(pd.to_numeric, errors='coerce').fillna(0)
    df['shannon'] = abundancias.apply(shannon, axis=1)

    resumen_muestra = df[['sample-id', 'diseases', 'shannon']]
    resumen_enfermedad = df.groupby('diseases')['shannon'].agg(['mean', 'std', 'count']).reset_index()

    return resumen_muestra, resumen_enfermedad

##
# Calcula la riqueza
#
def calcular_richness(site: str, mapeo_enfermedad_a_grupo: dict):
    query = f"SELECT * FROM {site};"
    df = pd.read_sql_query(query, engine)

    df["grupo"] = df["diseases"].map(mapeo_enfermedad_a_grupo)
    df = df[df["grupo"].notna()]

    micro_cols = [col for col in df.columns if col.startswith("x") and df[col].dtype in [float, int]]
    df["richness"] = df[micro_cols].apply(lambda row: (row > 0).sum(), axis=1)

    resultado = df.groupby("grupo")["richness"].apply(list).reset_index()

    return resultado.to_dict(orient="records")


##
# Calcula la abundancia media por enfermedad en un sitio anatómico
# 
def calcular_abundancias_por_disease(site: str):
    query = f"SELECT * FROM {site};"
    df = pd.read_sql_query(query, engine)

    abundancias = df.filter(regex='^x')
    df_abund = pd.concat([df[['diseases']], abundancias], axis=1)

    # Convertir a formato largo
    df_largo = df_abund.melt(id_vars=["diseases"], var_name="micro", value_name="abundance")

    # Normaliza micro: quitar espacios y pasar a minúsculas (se hace antes del merge)
    df_largo["micro"] = df_largo["micro"].fillna("").astype(str).str.strip().str.lower()

    #  Si el nombre está vacío (""), intenta reconstruirlo desde el índice de columna original
    df_largo.loc[df_largo["micro"] == "", "micro"] = "unknown_micro"


    # Mapear a nombres reales
    df_mother = pd.read_sql_query("SELECT * FROM mother", engine)
    df_largo = df_largo.merge(df_mother[['codigo', 'nombre_limpio']], how='left', left_on='micro', right_on='codigo')
    df_largo['micro'] = df_largo['nombre_limpio'].fillna(df_largo['micro'])
    df_largo.drop(['codigo', 'nombre_limpio'], axis=1, inplace=True)
    df_largo["nombre_mostrado"] = df_largo["micro"]


    # Filtrar los que no se han podido mapear
    df_largo = df_largo[df_largo["micro"].notna()]

    # Agrupar por enfermedad y nombre visible (género o xNN)
    resumen = df_largo.groupby(["diseases", "nombre_mostrado"])["abundance"].mean().reset_index()
    resumen["micro"] = resumen["nombre_mostrado"].replace("", "unknown")
    resumen = resumen.rename(columns={"nombre_mostrado": "micro"})


    resumen = resumen.replace({np.nan: None})  
    return resumen.to_dict(orient="records")



    ##
# Calcula la matriz de distancias de Bray-Curtis
#   Cada celda representa cuán diferente es el microbioma de una muestra respecto a otra
#

def calcular_beta_diversity(site: str):
    print(f" Calculando diversidad beta + PCoA para {site}")

    query = f"SELECT * FROM {site};"
    df = pd.read_sql_query(query, engine)

    # Obtener sample-ids
    sample_ids = df["sample-id"].astype(str).tolist()

    cols_x = [col for col in df.columns if col.startswith("x") and df[col].dtype in [float, int]]
    abundancias = df[cols_x]

    # Eliminar filas donde todas las abundancias son 0
    filtro = (abundancias > 0).any(axis=1)
    abundancias = abundancias[filtro]
    sample_ids = df.loc[filtro, "sample-id"].astype(str).tolist()

    # Convertir a NumPy y limpiar
    abundancias_np = abundancias.to_numpy()
    abundancias_np = np.nan_to_num(abundancias_np, nan=0.0, posinf=0.0, neginf=0.0)


    if abundancias_np.shape[0] != len(sample_ids):
        print(" Hay descuadre de tamaño. Ajustando...")
        min_len = min(abundancias_np.shape[0], len(sample_ids))
        abundancias_np = abundancias_np[:min_len]
        sample_ids = sample_ids[:min_len]

    # Calcular matriz de distancias
    distance_matrix = beta_diversity("braycurtis", abundancias_np, ids=sample_ids)

    # PCoA
    ordination_result = pcoa(distance_matrix)
    pcoa_df = ordination_result.samples.iloc[:, :2]
    pcoa_df["sample-id"] = pcoa_df.index

    # Unir con enfermedades
    merged_df = pd.merge(pcoa_df, df[["sample-id", "diseases"]], on="sample-id", how="left")

    return merged_df




def calcular_abundancia_por_grupo(site: str, mapeo_enfermedad_a_grupo: dict):
    query = f"SELECT * FROM {site};"
    df = pd.read_sql_query(query, engine)

    df["grupo"] = df["diseases"].map(mapeo_enfermedad_a_grupo)
    df = df[df["grupo"].notna()]  # Elimina enfermedades sin grupo asignado

    # Elimina columnas no microbianas antes del melt
    cols_micro = [col for col in df.columns if col.startswith("x") and df[col].dtype in [float, int]]
    df_largo = df[["sample-id", "grupo"] + cols_micro].melt(
        id_vars=["sample-id", "grupo"], var_name="micro", value_name="abundance"
    )
    df_mother = pd.read_sql_query("SELECT * FROM mother", engine)
    df_largo = df_largo.merge(df_mother[['codigo', 'nombre_limpio']], how='left', left_on='micro', right_on='codigo')
    df_largo['micro'] = df_largo['nombre_limpio'].fillna(df_largo['micro'])
    df_largo['nombre_mostrado'] = df_largo['nombre_limpio'].fillna(df_largo['micro'])

    df_largo.drop(['codigo', 'nombre_limpio'], axis=1, inplace=True)

    
    # Agrupar correctamente antes de renombrar
    resumen = df_largo.groupby(["grupo", "nombre_mostrado"])["abundance"].mean().reset_index()
    resumen = resumen.rename(columns={"nombre_mostrado": "micro"})

    return resumen.to_dict(orient="records")



