import psycopg2
import pandas as pd
from skbio.diversity.alpha import shannon
from skbio.diversity import beta_diversity
from skbio.stats.ordination import pcoa
##
#   Carga los datos de abundancia microbiana desde la base de datos PostgreSQL.
#   @param site: Nombre del sitio anatómico (por ejemplo, 'cervix', 'vagina', etc.)
#   @return: DataFrame con las filas de la tabla correspondiente.
#   
def cargar_abundancias(site: str):
    
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432"
    )
    query = f"SELECT * FROM {site};"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

##
# Calcula el índice de Shannon para cada muestra en un sitio anatómico distinto
# 
def calcular_shannon_por_site(site: str):
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432"
    )

    query = f"SELECT * FROM {site};"
    df = pd.read_sql_query(query, conn)
    conn.close()

    abundancias = df.filter(regex='^x')
    df['shannon'] = abundancias.apply(shannon, axis=1)

    resumen_muestra = df[['sample_id', 'diseases', 'shannon']]
    resumen_enfermedad = df.groupby('diseases')['shannon'].agg(['mean', 'std', 'count']).reset_index()

    return resumen_muestra, resumen_enfermedad

##
# Calcula la abundancia media por enfermedad en un sitio anatómico
# 
def calcular_abundancias_por_disease(site: str):
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432"
    )
    query = f"SELECT * FROM {site};"
    df = pd.read_sql_query(query, conn)
    conn.close()

    abundancias = df.filter(regex='^x')
    df_abund = pd.concat([df[['diseases']], abundancias], axis=1)

    resumen = df_abund.groupby('diseases').mean().reset_index()
    return resumen.to_dict(orient='records')  #para pasar al frontend como JSON
##
# Calcula la matriz de distancias de Bray-Curtis
#   Cada celda representa cuán diferente es el microbioma de una muestra respecto a otra
#
def calcular_beta_diversity(site: str):
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="postgres", 
        host="localhost",
        port="5432"
    )

    query = f"SELECT * FROM {site};"
    df = pd.read_sql_query(query, conn)
    conn.close()

    abundancias = df.filter(regex='^x')
    sample_ids = df['sample_id'].astype(str).tolist()

    distance_matrix = beta_diversity(metric='braycurtis', counts=abundancias.values, ids=sample_ids)
    
    #return distance_matrix

    # Aplica PCoA a la matriz de distancias
    ordination_result = pcoa(distance_matrix)

    # Extrae las primeras dos coordenadas principales
    pcoa_df = ordination_result.samples.iloc[:, :2]  # PCoA1 y PCoA2
    pcoa_df['sample_id'] = pcoa_df.index

    # Fusiona con enfermedades si quieres añadir etiquetas por grupo
    merged_df = pd.merge(pcoa_df, df[['sample_id', 'diseases']], on='sample_id', how='left')

    return merged_df


def calcular_abundancia_por_grupo(site: str, mapeo_enfermedad_a_grupo: dict):
    import psycopg2
    import pandas as pd

    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432"
    )
    query = f"SELECT * FROM {site};"
    df = pd.read_sql_query(query, conn)
    conn.close()

    df["grupo"] = df["diseases"].map(mapeo_enfermedad_a_grupo)
    df = df[df["grupo"].notna()]  # Elimina enfermedades sin grupo asignado

    micro_cols = [col for col in df.columns if col.startswith("x")]
    resultado = df.groupby("grupo")[micro_cols].mean().reset_index()

    return resultado.to_dict(orient="records")

# Código de prueba
#if __name__ == "__main__":
 #   resultado = calcular_abundancias_por_disease("vagina")
  #  from pprint import pprint
    #pprint(resultado[:3])  # Solo los 3 primeros grupos para no saturar

#if __name__ == "__main__":
    from pprint import pprint

    # Prueba la matriz de distancias con un site (ej. vagina)
    matriz = calcular_beta_diversity("vagina")
    print("Matriz de distancias Bray-Curtis (5x5 ejemplo):")
    pprint(matriz.to_data_frame().iloc[:5, :5])  # solo mostramos 5x5 para no saturar

if __name__ == "__main__":
    print(" Probando análisis de diversidad beta + PCoA")

    resultado = calcular_beta_diversity("vagina")  # Puedes cambiar el sitio si quieres

    print("\nPrimeras filas del resultado final:")
    print(resultado.head())

    print("\n Número total de muestras analizadas:", resultado.shape[0])
    print(" Columnas disponibles:", resultado.columns.tolist())
