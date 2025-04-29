# routes/search.py

from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from myapp.services.analytics import cargar_abundancias 

router = APIRouter()

@router.get("/search_abundancia")
def get_abundancia_bacteria(columna_micro: str = Query(...), site: str = Query(...)):
    df = cargar_abundancias(site)  

    if columna_micro not in df.columns:
        return []

    df = df[["diseases", columna_micro]]
    df_grouped = df.groupby("diseases")[columna_micro].mean().reset_index()
    df_grouped.columns = ["disease", "abundancia"]
    return df_grouped.to_dict(orient="records")
