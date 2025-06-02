import psycopg2
import pandas as pd
from skbio.diversity.alpha import shannon
from skbio.diversity import beta_diversity
from skbio.stats.ordination import pcoa
import numpy as np
from myapp.config import engine
import logging
from sqlalchemy import text
from scipy.stats import mannwhitneyu, kruskal
from skbio.stats.distance import permanova
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
##
#   Carga los datos de abundancia microbiana desde la base de datos PostgreSQL.
#   @param site: Nombre del sitio anatómico (por ejemplo, 'cervix', 'vagina', etc.)
#   @return: DataFrame con las filas de la tabla correspondiente.
#   
def cargar_abundancias(site: str):
    query = f"SELECT * FROM {site};"
    with engine.connect() as connection:
        df = pd.read_sql_query(text(query), connection)

    return df




##
# Calcula el índice de Shannon para cada muestra en un sitio anatómico distinto
# 
def calcular_shannon_por_site(site: str):
    query = f"SELECT * FROM {site};"
    with engine.connect() as connection:
        df = pd.read_sql_query(text(query), connection)



    abundancias = df.filter(regex='^x')
    abundancias = abundancias.apply(pd.to_numeric, errors='coerce').fillna(0)
    df['shannon'] = abundancias.apply(shannon, axis=1)

    resumen_muestra = df[['sample_id', 'diseases', 'shannon']]
    resumen_enfermedad = df.groupby('diseases')['shannon'].agg(['mean', 'std', 'count']).reset_index()

    return resumen_muestra, resumen_enfermedad

def calcular_pvalor_shannon(site: str, mapeo_enfermedad_a_grupo: dict):

    df = cargar_abundancias(site)
    df["grupo"] = df["diseases"].map(mapeo_enfermedad_a_grupo)
    df = df[df["grupo"].notna()]

    abundancias = df.filter(regex='^x').apply(pd.to_numeric, errors='coerce').fillna(0)
    df["shannon"] = abundancias.apply(shannon, axis=1)

    grupos = df["grupo"].unique()
    datos_por_grupo = [df[df["grupo"] == g]["shannon"].dropna().values for g in grupos]  # 👈 dropna() clave

    try:
        if len(grupos) == 2:
            stat, p_value = mannwhitneyu(*datos_por_grupo, alternative='two-sided')
            test = "mannwhitney"
        elif len(grupos) > 2:
            stat, p_value = kruskal(*datos_por_grupo)
            test = "kruskal"
        else:
            raise ValueError("No hay suficientes grupos para el test.")
    except Exception as e:
        print(f" Error al calcular p-valor de Shannon para {site}: {e}")
        return {"p_value": None, "test": "error_during_test"}

    return {"p_value": p_value, "test": test}


def calcular_pvalor_richness(site: str, mapeo_enfermedad_a_grupo: dict):
    df = cargar_abundancias(site)
    df["grupo"] = df["diseases"].map(mapeo_enfermedad_a_grupo)
    df = df[df["grupo"].notna()]

    # Calcular índice de riqueza (número de géneros con abundancia > 0)
    abundancias = df.filter(regex='^x').apply(pd.to_numeric, errors='coerce').fillna(0)
    df["richness"] = abundancias.gt(0).sum(axis=1)  # número de géneros no nulos

    grupos = df["grupo"].unique()
    datos_por_grupo = [df[df["grupo"] == g]["richness"].dropna().values for g in grupos]

    try:
        if len(grupos) == 2:
            stat, p_value = mannwhitneyu(*datos_por_grupo, alternative='two-sided')
            test = "mannwhitney"
        elif len(grupos) > 2:
            stat, p_value = kruskal(*datos_por_grupo)
            test = "kruskal"
        else:
            raise ValueError("No hay suficientes grupos para el test.")
    except Exception as e:
        print(f"Error al calcular p-valor de Richness para {site}: {e}")
        return {"p_value": None, "test": "error_during_test"}

    return {"p_value": p_value, "test": test}


##
# Calcula la riqueza
#
def calcular_richness(site: str, mapeo_enfermedad_a_grupo: dict):
    query = f"SELECT * FROM {site};"
    with engine.connect() as connection:
        df = pd.read_sql_query(text(query), connection)


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
    with engine.connect() as connection:
        tablas = connection.execute(text("SELECT tablename FROM pg_tables WHERE schemaname = 'public';")).fetchall()
        df = pd.read_sql_query(text(query), connection)

   
    abundancias = df.filter(regex='^x')
   
    df_abund = pd.concat([df[['diseases']], abundancias], axis=1)

    # Convertir a formato largo
    df_largo = df_abund.melt(id_vars=["diseases"], var_name="micro", value_name="abundance")

    # Normaliza micro: quitar espacios y pasar a minúsculas (se hace antes del merge)
    df_largo["micro"] = df_largo["micro"].fillna("").astype(str).str.strip().str.lower()

    #  Si el nombre está vacío (""), intenta reconstruirlo desde el índice de columna original
    df_largo.loc[df_largo["micro"] == "", "micro"] = "unknown_micro"


    # Mapear a nombres reales
    with engine.connect() as connection:
        df_mother = pd.read_sql_query(text("SELECT * FROM mother"), connection)

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

    query = f"SELECT * FROM {site};"
    
    with engine.connect() as connection:
        df = pd.read_sql_query(text(query), connection)

    # Obtener sample_ids
    sample_ids = df["sample_id"].astype(str).tolist()

    cols_x = [col for col in df.columns if col.startswith("x") and df[col].dtype in [float, int]]
    abundancias = df[cols_x]

    # Eliminar filas donde todas las abundancias son 0
    filtro = (abundancias > 0).any(axis=1)
    abundancias = abundancias[filtro]
    sample_ids = df.loc[filtro, "sample_id"].astype(str).tolist()

    # Convertir a NumPy y limpiar
    abundancias_np = abundancias.to_numpy()
    abundancias_np = np.nan_to_num(abundancias_np, nan=0.0, posinf=0.0, neginf=0.0)


    if abundancias_np.shape[0] != len(sample_ids):
        min_len = min(abundancias_np.shape[0], len(sample_ids))
        abundancias_np = abundancias_np[:min_len]
        sample_ids = sample_ids[:min_len]

    # Calcular matriz de distancias
    # Matriz de distancias
    distance_matrix = beta_diversity("braycurtis", abundancias_np, ids=sample_ids)

    # PERMANOVA
    df_grupos = df.loc[filtro, ["sample_id", "diseases"]].copy()
    df_grupos.set_index("sample_id", inplace=True)
    permanova_result = permanova(distance_matrix, df_grupos["diseases"], permutations=999)
    p_value = permanova_result["p-value"]
    # PCoA
    ordination_result = pcoa(distance_matrix)
    pcoa_df = ordination_result.samples.iloc[:, :2]
    pcoa_df["sample_id"] = pcoa_df.index

    # Unir con enfermedades
    merged_df = pd.merge(pcoa_df, df[["sample_id", "diseases"]], on="sample_id", how="left")

    # Añadir p-valor global
    return {
        "pcoa": merged_df.to_dict(orient="records"),
        "p_value": p_value
    }

def calcular_beta_diversity_por_grupos(site: str, mapeo_enfermedad_a_grupo: dict):
    query = f"SELECT * FROM {site};"
    with engine.connect() as connection:
        df = pd.read_sql_query(text(query), connection)

    df["grupo"] = df["diseases"].map(mapeo_enfermedad_a_grupo)
    df = df[df["grupo"].notna()]
    
    sample_ids = df["sample_id"].astype(str).tolist()
    cols_x = [col for col in df.columns if col.startswith("x")]
    abundancias = df[cols_x].apply(pd.to_numeric, errors='coerce').fillna(0)

    # Eliminar filas con todo ceros
    filtro = (abundancias > 0).any(axis=1)
    abundancias = abundancias[filtro]
    df = df[filtro]
    sample_ids = df["sample_id"].tolist()

    matriz = beta_diversity("braycurtis", abundancias.to_numpy(), ids=sample_ids)
    
    df_grupos = df.set_index("sample_id")[["grupo"]]
    resultado_permanova = permanova(matriz, df_grupos["grupo"], permutations=999)
    p_value = resultado_permanova["p-value"]

    ordination = pcoa(matriz)
    coords = ordination.samples.iloc[:, :2]
    coords["sample_id"] = coords.index

    merged = pd.merge(coords, df[["sample_id", "diseases", "grupo"]], on="sample_id", how="left")

    return {
        "pcoa": merged.to_dict(orient="records"),
        "p_value": p_value
    }



def calcular_abundancia_por_grupo(site: str, mapeo_enfermedad_a_grupo: dict):
    
    query = f"SELECT * FROM {site};"
    

    with engine.connect() as connection:
        df = pd.read_sql_query(text(query), connection)


    df["grupo"] = df["diseases"].map(mapeo_enfermedad_a_grupo)
    df = df[df["grupo"].notna()]  # Elimina enfermedades sin grupo asignado

    # Elimina columnas no microbianas antes del melt
    cols_micro = [col for col in df.columns if col.startswith("x")]
    df[cols_micro] = df[cols_micro].apply(pd.to_numeric, errors='coerce')

    df_largo = df[["sample_id", "grupo"] + cols_micro].melt(
        id_vars=["sample_id", "grupo"], var_name="micro", value_name="abundance"
    )
    with engine.connect() as connection:
        df_mother = pd.read_sql_query(text("SELECT * FROM mother"), connection)

    df_largo = df_largo.merge(df_mother[['codigo', 'nombre_limpio']], how='left', left_on='micro', right_on='codigo')
    df_largo['micro'] = df_largo['nombre_limpio'].fillna(df_largo['micro'])
    df_largo['nombre_mostrado'] = df_largo['nombre_limpio'].fillna(df_largo['micro'])

    df_largo.drop(['codigo', 'nombre_limpio'], axis=1, inplace=True)

    
    # Agrupar correctamente antes de renombrar
    resumen = (
        df_largo
        .groupby(["grupo", "nombre_mostrado"], dropna=False)["abundance"]
        .mean()
        .reset_index()
    )

    resumen = resumen.rename(columns={"nombre_mostrado": "micro"})

    # Sustituye NaN en todas las columnas (especialmente 'abundance') por None
    resumen = resumen.fillna(value={"abundance": 0.0})  # Evita los NaN en la media
    resumen = resumen.where(pd.notnull(resumen), None)  # Asegura que no quedan otros NaN

    return resumen.to_dict(orient="records")



def calcular_biomarcadores(site: str, mapeo_enfermedad_a_grupo: dict):
    query = f"SELECT * FROM {site};"
    with engine.connect() as connection:
        df = pd.read_sql_query(text(query), connection)


    df["grupo"] = df["diseases"].map(mapeo_enfermedad_a_grupo)
    df = df[df["grupo"].notna()]

    micro_cols = [col for col in df.columns if col.startswith("x")]
    df[micro_cols] = df[micro_cols].apply(pd.to_numeric, errors='coerce').fillna(0)

    grupos_unicos = sorted(df["grupo"].unique())
    n_grupos = len(grupos_unicos)

    resultado = []
    tipo_test = "mannwhitney" if n_grupos == 2 else "kruskalwallis"

    for micro in micro_cols:
        grupos = [df[df["grupo"] == g][micro].values for g in grupos_unicos]

        # Saltar si todas las abundancias son cero
        if all((g == 0).all() for g in grupos):
            continue

        try:
            if n_grupos == 2:
                _, p_value = mannwhitneyu(grupos[0], grupos[1], alternative='two-sided')
            else:
                _, p_value = kruskal(*grupos)
        except Exception:
            p_value = None

        fila = {
            "micro": micro,
            "p_value": p_value,
            "test": tipo_test
        }

        # Añadir media, std y conteo por grupo
        for idx, g in enumerate(grupos_unicos):
            valores = df[df["grupo"] == g][micro].values
            total_muestras = len(df[df["grupo"] == g])
            n_muestras_con_micro = (valores > 0).sum()

            fila[f"mean_g{idx+1}"] = float(valores.mean())
            fila[f"std_g{idx+1}"] = float(valores.std())
            fila[f"n_g{idx+1}"] = int(n_muestras_con_micro)
            fila[f"total_g{idx+1}"] = int(total_muestras)

        resultado.append(fila)

        # Mapeo de nombres limpios
        with engine.connect() as connection:
            df_mother = pd.read_sql_query(text("SELECT * FROM mother"), connection)

        nombre_dict = df_mother.set_index("codigo")["nombre_limpio"].to_dict()

        for fila in resultado:
            cod = fila["micro"].lower()
            fila["micro"] = nombre_dict.get(cod, cod)

    return resultado

