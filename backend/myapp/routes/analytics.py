""""
    Este archivo define el endpoint `/shannon` que permite calcular el índice de Shannon
    y generar resúmenes por muestra y por enfermedad para un sitio anatómico específico
    (vagina, cervix, uterus, rectum, orine).
"""

from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from myapp.services.analytics import calcular_shannon_por_site
from myapp.services.analytics import calcular_beta_diversity
from myapp.services.analytics import cargar_abundancias
"""No lo he podido usar porque necesita que ambos grupos tengan mismo
numero de muestras y dado que esto iba a resultar dificil he opctado por Mann-Whitney U"""
from scipy.stats import wilcoxon 
from scipy.stats import mannwhitneyu
import pandas as pd
import numpy as np

router = APIRouter()

"""
    Calcula el índice de diversidad de Shannon para un sitio anatómico específico.

    @param site: Nombre del sitio (tabla en la base de datos). Debe ser uno de:
                 ['vagina', 'cervix', 'uterus', 'rectum', 'orine']
    @return JSONResponse: Objeto con:
        - resumen_muestra: Lista de muestras con su índice de Shannon.
        - resumen_enfermedad: Estadísticas por condición médica (media, std, n).
        - En caso de error, código 400 (entrada inválida) o 500 (error de servidor).
"""
@router.get("/shannon")
def calcular_shannon(site: str = Query(...)):
    print(" Entrando al endpoint /shannon con site =", site)

    tablas_validas = ["vagina", "cervix", "uterus", "rectum", "orine"]
    if site not in tablas_validas:
        print("Site no válido:", site)
        return JSONResponse(status_code=400, content={"error": "Nombre de tabla no permitido"})
    print("¿Está importado calcular_shannon_por_site?", calcular_shannon_por_site)

    try:
        print("Calculando índice de Shannon...")
        resumen_muestra, resumen_enfermedad = calcular_shannon_por_site(site)

        print("Resultado muestra (head):", resumen_muestra.head().to_dict())
        print("Resultado enfermedad (head):", resumen_enfermedad.head().to_dict())

        # Reemplazar NaN, inf, -inf por None (ya tratado)
        def limpiar_dataframe(df):
            df = df.replace([np.inf, -np.inf], np.nan)
            return df.where(pd.notnull(df), None).astype(object)

        from fastapi.encoders import jsonable_encoder

        def limpiar_nan_para_json(df):
            df = df.replace([np.inf, -np.inf], np.nan)
            df = df.where(pd.notnull(df), None)
            dict_list = df.to_dict(orient='records')

            # Recorrer cada fila y cada valor para asegurar que sea JSON compatible
            for fila in dict_list:
                for k, v in fila.items():
                    if isinstance(v, float) and (np.isnan(v) or np.isinf(v)):
                        fila[k] = None
                    elif isinstance(v, (np.integer, np.floating)):
                        fila[k] = v.item()

            return dict_list


        return JSONResponse(
            content={
                "resumen_muestra": limpiar_nan_para_json(resumen_muestra),
                "resumen_enfermedad": limpiar_nan_para_json(resumen_enfermedad)
            }
        )

    except Exception as e:
        print(" ERROR en /shannon:", str(e))  
        return JSONResponse(status_code=500, content={"error": str(e)})

"""
    Calcula la diversidad beta (distancia de Bray-Curtis) y aplica PCoA para visualización 2D.

    @param site: Nombre del sitio (por ejemplo 'vagina').
    @return JSONResponse: Lista de objetos con:
        - sample_id
        - PC1: Primera coordenada principal
        - PC2: Segunda coordenada principal
        - diseases: Enfermedad asociada a cada muestra
"""
@router.get("/beta")
def calcular_beta(site: str = Query(...)):
    try:
        tablas_validas = ["vagina", "cervix", "uterus", "rectum", "orine"]
        if site not in tablas_validas:
            return JSONResponse(status_code=400, content={"error": "Nombre de tabla no permitido"})

        print(f" Calculando diversidad beta + PCoA para {site}")
        resultado = calcular_beta_diversity(site)

        from fastapi.encoders import jsonable_encoder
        resultado_json = jsonable_encoder(resultado)

        return JSONResponse(content=resultado_json)

    except Exception as e:
        print(" ERROR en /beta:", str(e))
        return JSONResponse(status_code=500, content={"error": str(e)})


"""
     Calcula los biomarcadores diferencialmente relevantes entre dos grupos 
    usando el test estadístico de mannwhitneyu para cada microorganismo.

    @param site: Nombre del sitio anatómico .
    @return list: Lista de diccionarios, uno por cada microorganismo, con:
        - micro: nombre del microorganismo (ej. 'x1', 'x2'...)
        - mean_g1: media de abundancia en el grupo 1
        - std_g1: desviación estándar en el grupo 1
        - n_g1: número de muestras del grupo 1
        - mean_g2: media de abundancia en el grupo 2
        - std_g2: desviación estándar en el grupo 2
        - n_g2: número de muestras del grupo 2
        - p_value: valor p obtenido del test de mannwhitneyu
"""
from fastapi import Body
import traceback
@router.post("/biomarcadores")
def get_biomarcadores(
    site: str = Query(...),
    grupos: dict = Body(...)
):
    
    try:
        df = cargar_abundancias(site)
        df["grupo"] = df["diseases"].map(grupos)  # se usa el diccionario enviado

        keys_microorganismos = [col for col in df.columns if col.startswith("x")]
        resultados = []

        for micro in keys_microorganismos:
            g1 = df[df["grupo"] == 1][micro]
            g2 = df[df["grupo"] == 2][micro]

            if len(g1) > 0 and len(g2) > 0:
                stat, p = mannwhitneyu(g1, g2, alternative='two-sided')
            else:
                p = None

            resultados.append({
                "micro": micro,
                "mean_g1": g1.mean(),
                "std_g1": g1.std(),
                "n_g1": len(g1),
                "mean_g2": g2.mean(),
                "std_g2": g2.std(),
                "n_g2": len(g2),
                "p_value": p
            })

        return resultados

    except Exception as e:
        print("Error en get_biomarcadores:")
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"error": str(e)})
