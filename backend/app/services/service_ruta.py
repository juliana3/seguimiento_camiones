#aca la logica para calcular y guaardar el largo en metros y la duracion estimada en minutos en la tabla ruta
from sqlalchemy import func
from sqlalchemy.orm import Session
from geoalchemy2.functions import ST_Length

from ..models import Ruta


def calcular_metricas_ruta(db: Session, ruta: Ruta):

    # Calcular largo real en metros
    largo_metros = db.query(
        func.ST_Length(func.Geography(ruta.geometria))
    ).scalar()


    ruta.largo_metros = round(largo_metros, 2)

    db.commit()
    db.refresh(ruta)

    return ruta
