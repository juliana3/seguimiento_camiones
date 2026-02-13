from pydantic import BaseModel, Field, model_validator
from typing import Optional, Dict, Any, Literal
from datetime import datetime


class geoJSONPoint(BaseModel):
    type: Literal["Point"]
    coordinates: tuple[float, float]  # (longitud, latitud)



class ReporteCreate(BaseModel):
    lat: float = Field(..., ge=-90, le=90)
    lng: float = Field(..., ge=-180, le=180)




class ReporteResponse(BaseModel):
    reporte_id: int
    ubicacion: geoJSONPoint
    direccion: Optional[str]
    fecha_reporte: datetime
    usuario_id: int
    camion_id: Optional[int]
    ruta_id: Optional[int]
    zona_id: int
    created_at: datetime

    
    class Config:
        from_attributes = True



class ReporteListItem(BaseModel):
    reporte_id: int = Field(
        ...,
        description="Identificador único del reporte.",
        examples=[1, 2, 3]
    )

    fecha_reporte: datetime = Field(
        ...,
        description="Fecha y hora en que se realizó el reporte.",
        examples=["2024-01-15T14:30:00Z", "2024-02-20T09:15:00Z"]
    )

    zona_id: int = Field(
        ...,
        description="Identificador de la zona asociada al reporte.",
        examples=[10, 20, 30]
    )

