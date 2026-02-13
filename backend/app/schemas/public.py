from pydantic import BaseModel, Field


class CamionPosicion(BaseModel):
    lat: float
    lng: float


class ConsultaPublica(BaseModel):
    lat : float = Field(..., description="Latitud del punto de consulta.")
    lng : float = Field(..., description="Longitud del punto de consulta.")

    
class ConsultaPublicaResponse(BaseModel):
    lat : float
    lng : float

    zona : str
    hay_recoleccion_hoy : bool
    tipo_residuo : str | None

    estado : str
    mensaje: str

    porcentaje_recorrido_total : float | None
    porcentaje_restante_hasta_usuario : float | None
    minutos_restantes : int | None

    camion_posicion : CamionPosicion | None
    