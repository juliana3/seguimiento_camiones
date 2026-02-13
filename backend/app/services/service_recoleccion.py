from datetime import datetime, time 
from sqlalchemy.orm import Session
from geoalchemy2.functions import ST_LineLocatePoint, ST_LineInterpolatePoint
from geoalchemy2.shape import to_shape, from_shape
from shapely.geometry import Point

from ..models import Ruta, Horario
from ..dependencies.zona import get_zona_por_punto



def mapear_dia_semana(hoy: datetime) -> int:
    #mapear el dia de la semana que devuelve datetime.weekday() al enum que esta declarado en utils/constantes.py

    dia_mapeado = (hoy.weekday() + 1) % 7 #esto hace que domingo sea 0

    return dia_mapeado





def calcular_porcentaje_recorrido(ahora, inicio, fin):
    duracion_total = (fin - inicio).total_seconds()
    if duracion_total <= 0:
        return 0

    transcurrido = (ahora- inicio).total_seconds()

    porcentaje = transcurrido / duracion_total

    porcentaje_actual = max(0, min(1, porcentaje)) #esto asegura que el porcentaje este entre 0 y 1

    return porcentaje_actual




def determinar_recoleccion(db: Session, lat: float, lng : float):
    ahora = datetime.now()
    punto_usuario = from_shape(Point(lng, lat), srid=4326)

    zona = get_zona_por_punto(db, punto_usuario)

    #hago un response base
    base_response = {
        "lat": lat,
        "lng": lng,
        "zona": zona.nombre if zona else "",
        "hay_recoleccion_hoy": False,
        "tipo_residuo": zona.tipo_residuo if zona else None,
        "estado": "",
        "mensaje": "",
        "porcentaje_recorrido_total": None,
        "porcentaje_restante_hasta_usuario": None,
        "minutos_restantes": None,
        "camion_posicion": None
    }

    if not zona:
        base_response.update({
            "estado": "FUERA_DE_ZONA",
            "mensaje": "La dirección proporcionada no se encuentra dentro de una zona de recolección."
        })
        return base_response
    
    #VERIFICAR QUE NO SEA EL DIA EXCLUIDO DE RECOLECCION
    que_dia_es_hoy = mapear_dia_semana(ahora)
    if zona.excluye_dia is not None and que_dia_es_hoy == zona.excluye_dia:
        base_response.update({
            "estado": "SIN_RECOLECCION",
            "mensaje": "Hoy no hay recolección en esta zona."
        })
        return base_response
    
    #BUSCAR EL HORARIO DE RECOLECCION PARA LA ZONA Y EL DIA DE HOY
    horario = db.query(Horario).filter(
        Horario.zona_id == zona.zona_id,
        Horario.dia_semana == que_dia_es_hoy
    ).first()

    if not horario:
        base_response.update({
            "estado": "SIN_RECOLECCION",
            "mensaje": "No hay recolección programada para esta zona hoy."
        })
        return base_response
    
    #SI HAY HORARIO, CALCULAR EL ESTADO DE LA RECOLECCION
    base_response["hay_recoleccion_hoy"] = True
    
    inicio = datetime.combine(ahora.date(), horario.hora_inicio) # type: ignore
    fin = datetime.combine(ahora.date(), horario.hora_fin) # type: ignore

    if ahora < inicio:
        base_response.update({
            "estado": "PENDIENTE",
            "mensaje": f"La recolección comenzará a las {horario.hora_inicio}."
        })
        return base_response
    
    if ahora > fin:
        base_response.update({
            "estado": "FINALIZADA",
            "mensaje": "La recolección ya ha finalizado por hoy."
        })
        return base_response
    
    #CALCULO EL PORCENTAJE ACTUAL DEL RECORRIDO
    porcentaje_actual = calcular_porcentaje_recorrido(ahora, inicio, fin)

    #tomo una ruta de la zona, asumiendo que cada zona tiene una ruta asociada
    if not zona.rutas:
        base_response.update({
            "estado": "SIN_RUTA",
            "mensaje": "No hay rutas asociadas a esta zona."
        })
        return base_response
    ruta = zona.rutas[0] 

    #Obtengo el porcentaje de recorrido en el que se encuentra la casa del usuario
    porcentaje_usuario = db.query(
        ST_LineLocatePoint(Ruta.geometria, punto_usuario)
    ).filter(
        Ruta.ruta_id == ruta.ruta_id
    ).scalar()

    if porcentaje_usuario is None:
        base_response.update({
            "estado": "FUERA_DE_RUTA",
            "mensaje": "La dirección no está sobre la ruta de recolección."
        })
        return base_response

    if porcentaje_actual >= porcentaje_usuario:
        base_response.update({
            "estado": "YA_PASO",
            "mensaje": "El camión ya pasó por tu domicilio.",
            "porcentaje_recorrido_total": round(porcentaje_actual * 100, 2)
        })
        return base_response
    
    #CALCULO EL TIEMPO RESTANTE HASAT LA CASA DEL USUARIO
    delta_porcentaje = porcentaje_usuario - porcentaje_actual
    segundos_restantes = delta_porcentaje * ((fin - inicio).total_seconds())
    minutos_restantes = int(segundos_restantes/60)

    porcentaje_restante_hasta_usuario = round(delta_porcentaje * 100, 2)

    #POsicion actual del camion
    punto_interpolado = db.query(
        ST_LineInterpolatePoint(Ruta.geometria, porcentaje_actual)).filter(
            Ruta.ruta_id == ruta.ruta_id
        ).scalar()
    
    camion_posicion = None

    if punto_interpolado:
        punto_shape = to_shape(punto_interpolado)
        lng_camion, lat_camion = list(punto_shape.coords)[0]

        camion_posicion = {
            "lat": lat_camion,
            "lng": lng_camion
        }

    base_response.update({
        "estado": "EN_CAMINO",
        "mensaje": f"El camión llegará en aproximadamente {minutos_restantes} minutos.",
        "porcentaje_recorrido_total": round(porcentaje_actual * 100, 2),
        "porcentaje_restante_hasta_usuario": porcentaje_restante_hasta_usuario,
        "minutos_restantes": minutos_restantes,
        "camion_posicion": camion_posicion
    })

    return base_response