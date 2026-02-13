from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session


from ..dependencies.db import get_db


from ..schemas.public import ConsultaPublica, ConsultaPublicaResponse


from ..services.service_recoleccion import determinar_recoleccion


router = APIRouter(
    prefix="/public",
    tags=["Consultas Públicas"]
)

@router.post("/consulta", response_model=ConsultaPublicaResponse)
def consulta_publica(data: ConsultaPublica, db:Session = Depends(get_db)):
    return determinar_recoleccion(db, data.lat, data.lng)


