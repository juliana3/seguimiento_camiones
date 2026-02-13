from sqlalchemy.orm import Session
from sqlalchemy import func
from geoalchemy2.shape import from_shape
from shapely.geometry import Point

from app.models.zona import Zona


#esta funcion devuelve la zona que contiene el punto dado (latitud, longitud) o None si no existe tal zona o no pertenece a ninguna zona
def get_zona_por_punto(db: Session, punto_geografico) -> Zona | None:

    return (
        db.query(Zona)
        .filter(func.ST_Contains(Zona.geom, punto_geografico))
        .first()
    )
