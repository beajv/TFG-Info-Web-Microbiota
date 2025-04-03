from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from myapp.services.analytics import calcular_shannon_por_site

import pandas as pd
import numpy as np

router = APIRouter()

@router.get("/shannon")
def calcular_shannon(site: str = Query(...)):
    print("🔍 Entrando al endpoint /shannon con site =", site)

    tablas_validas = ["vagina", "cervix", "uterus", "rectum", "orine"]
    if site not in tablas_validas:
        print("❌ Site no válido:", site)
        return JSONResponse(status_code=400, content={"error": "Nombre de tabla no permitido"})
    print("🧠 ¿Está importado calcular_shannon_por_site?", calcular_shannon_por_site)

    try:
        print("✅ Calculando índice de Shannon...")
        resumen_muestra, resumen_enfermedad = calcular_shannon_por_site(site)

        print("🧪 Resultado muestra (head):", resumen_muestra.head().to_dict())
        print("🧪 Resultado enfermedad (head):", resumen_enfermedad.head().to_dict())

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
        print("❌ ERROR en /shannon:", str(e))  # 👈 MUY IMPORTANTE
        return JSONResponse(status_code=500, content={"error": str(e)})
