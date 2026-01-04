from pydantic import BaseModel, Field, model_validator
from typing import Optional, Dict, Any
from datetime import datetime



class UbicacionUsuarioCreate(BaseModel):
    nombre: str = Field(
        ...,
        max_length=50,
        description="Nombre identificador de la ubicación",
        examples=["Casa", "Trabajo"]
    )

    lat: float = Field(
        ...,
        description="Latitud de la ubicación",
        examples=[-31.623]
    )

    lng: float = Field(
        ...,
        description="Longitud de la ubicación",
        examples=[-60.702]
    )

    direccion: Optional[str] = Field(
        None,
        description="Dirección textual de la ubicación"
    )

    es_principal: bool = Field(
        False,
        description="Indica si es la ubicación principal del usuario"
    )


class UbicacionUsuarioUpdate(BaseModel):
    nombre: Optional[str] = Field(
        None,
        max_length=50
    )

    direccion: Optional[str] = None

    es_principal: Optional[bool] = None

    @model_validator(mode="after")
    def at_least_one_field(cls, values):
        if not any(values.model_dump(exclude_none=True).values()):
            raise ValueError("Debe enviar al menos un campo para actualizar")
        return values





class UbicacionUsuarioResponse(BaseModel):
    ubicacion_id: int
    nombre: str
    direccion: Optional[str]
    es_principal: bool
    ubicacion: Dict[str, Any]   # POINT GeoJSON
    created_at: datetime

    class Config:
        from_attributes = True

        

class UbicacionUsuarioListItem(BaseModel):
    ubicacion_id: int
    nombre: str
    es_principal: bool
