from sqlalchemy import func, and_
from sqlalchemy.orm import Session
from shapely.geometry import Point, mapping
from geoalchemy2.shape import from_shape, to_shape
from geoalchemy2.functions import ST_LineLocatePoint

from ..models import Reporte, Ruta
from ..dependencies.zona import get_zona_por_punto
from ..services.service_noti import crear_notificacion

#funcion auxiliar para convertir geometria a geojson, se puede usar en el endpoint de reportes para devolver la ubicacion del reporte en formato geojson
def geometry_to_geojson(geometry):
    if geometry is None:
        return None

    shape = to_shape(geometry)
    return mapping(shape)



def crear_reporte(db: Session, lat: float, lng: float, usuario_id: int):

    punto = from_shape(Point(lng, lat), srid=4326)

    zona = get_zona_por_punto(db, punto)

    if not zona:
        return None, "La ubicación no pertenece a una zona cubierta."

    ruta_id = None

    # Intentar asociar ruta si cae sobre alguna
    for ruta in zona.rutas:
        distancia = db.query(
            func.ST_Distance(
                func.Geography(Ruta.geometria),
                func.Geography(punto)
            )
        ).filter(
            Ruta.ruta_id == ruta.ruta_id
        ).scalar()

        if distancia is not None and distancia < 30:  # 30 metros de tolerancia
            ruta_id = ruta.ruta_id
            break

    reporte = Reporte(
        ubicacion=punto,
        usuario_id=usuario_id,
        zona_id=zona.zona_id,
        ruta_id=ruta_id
    )

    db.add(reporte)
    db.commit()
    db.refresh(reporte)

    crear_notificacion(
        db=db,
        usuario_id=usuario_id,
        tipo="reporte_creado",
        titulo="Reporte registrado",
        mensaje="Tu reporte fue registrado correctamente.",
        canal="in_app"
    )


    reporte_geojson = geometry_to_geojson(reporte.ubicacion)

    return {
        "reporte_id": reporte.reporte_id,
        "ubicacion": reporte_geojson,
        "direccion": reporte.direccion,
        "fecha_reporte": reporte.fecha_reporte,
        "usuario_id": reporte.usuario_id,
        "camion_id": reporte.camion_id,
        "ruta_id": reporte.ruta_id,
        "zona_id": reporte.zona_id,
        "created_at": reporte.created_at
    }, None


def serializar_reporte(reporte: Reporte):
    return {
        "reporte_id": reporte.reporte_id,
        "ubicacion": mapping(to_shape(reporte.ubicacion)) if reporte.ubicacion else None, #type: ignore
        "direccion": reporte.direccion,
        "fecha_reporte": reporte.fecha_reporte,
        "usuario_id": reporte.usuario_id,
        "camion_id": reporte.camion_id,
        "ruta_id": reporte.ruta_id,
        "zona_id": reporte.zona_id,
        "created_at": reporte.created_at
    }


def listar_reportes_usuario(db: Session, usuario_id: int):
    reportes = (
        db.query(Reporte)
        .filter(Reporte.usuario_id == usuario_id)
        .order_by(Reporte.fecha_reporte.desc())
        .all()
    )

    return [serializar_reporte(r) for r in reportes]


def listar_reportes_admin(
    db: Session,
    zona_id: int | None = None,
    fecha_desde=None,
    fecha_hasta=None
):
    query = db.query(Reporte)

    filtros = []

    if zona_id:
        filtros.append(Reporte.zona_id == zona_id)

    if fecha_desde:
        filtros.append(Reporte.fecha_reporte >= fecha_desde)

    if fecha_hasta:
        filtros.append(Reporte.fecha_reporte <= fecha_hasta)

    if filtros:
        query = query.filter(and_(*filtros))

    reportes = query.order_by(Reporte.fecha_reporte.desc()).all()

    return [serializar_reporte(r) for r in reportes]