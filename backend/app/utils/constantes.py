#ROLES
from enum import IntEnum


PUBLICO = "publico"
REGISTRADO = "registrado"
ADMIN = "admin"
SUPERADMIN = "superadmin"


#dias de la semana
class DiaSemanaEnum(IntEnum):
    DOMINGO = 0
    LUNES = 1
    MARTES = 2
    MIERCOLES = 3
    JUEVES = 4
    VIERNES = 5
    SABADO = 6

#tipos de residuo
class TipoResiduoEnum(IntEnum):
    HUMEDOS = 1
    SECOS = 2


#estados de recoleccion
class EstadoRecoleccionEnum(IntEnum):
    PENDIENTE = 1
    EN_CURSO = 2
    FINALIZADA = 3
    SIN_RECOLECCION = 4