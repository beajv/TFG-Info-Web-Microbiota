import numpy as np
import pandas as pd
from scipy.stats import entropy

def shannon_diversity_index(abundances):
    """"
    Calcula el Índice de Shannon a partir de una lista de abundancias.
    
    Parámetro:
    - abundances (list): Lista con los valores de abundancia de cada especie en la muestra.
    
    Retorna:
    - float: Valor del Índice de Shannon
    """
    abundances = np.array(abundances)
    abundances = abundances[abundances > 0]  # Evitar valores cero para evitar problemas en log
    proportions = abundances / np.sum(abundances)  # Convertir en proporciones
    return entropy(proportions, base=np.e)  # Cálculo usando logaritmo natural


def calculate_shannon_for_samples(data_path):
    """
    Carga los datos y calcula el Índice de Shannon para cada muestra.
    
    Parámetro:
    - data_path (str): Ruta del archivo CSV con los datos.

    Retorna:
    - DataFrame con los valores del Índice de Shannon.
    """
    df = pd.read_csv(data_path)  # Cargar el archivo CSV
    sample_ids = df.columns[1:]  # Omitir la primera columna (nombres de especies)
    
    shannon_values = []
    
    for sample in sample_ids:
        abundances = df[sample].values  
        shannon_index = shannon_diversity_index(abundances)  
        shannon_values.append({"Sample": sample, "Shannon_Index": shannon_index})  
    
    return pd.DataFrame(shannon_values)  