from pydantic import BaseModel, Field, model_validator
from typing import Optional, Dict, Any
from datetime import datetime

class ZonaCreate(BaseModel):
    codigo : str = Field(
        ..., 
        max_length=50,
        description="Código único que identifica la zona.",
        examples=["BARRIO_CANDIOTI", "BARRIO_SUR"]
    )
    
    nombre : str = Field(
        ...,
        max_length=100,
        description="Nombre descriptivo de la zona.",
        examples=["Barrio Candioti", "Barrio Sur"]
    )

    descripcion : Optional[str] = Field(
        None,
        description="Descripción detallada de la zona. Especialmente de los limites.",
        examples=["Zona ubicada al norte de la ciudad, delimitada por..."]
    )

    color : Optional[str] = Field(
        "#FF5733",
        pattern="^#([A-Fa-f0-9]{6})$",
        description="Color representativo de la zona en formato hexadecimal.",
        examples=["#FF5733", "#33FF57"]
    )

    #GEOJson pegado por el admin

    geometria : Dict[str, Any] = Field(
        ...,
        description="Geometría de la zona en formato GeoJSON.",
        examples=[{
            "type": "MultiPolygon",
            "coordinates": [
                [
                    [
                        [-58.443, -34.599],
                        [-58.442, -34.598],
                        [-58.441, -34.599],
                        [-58.443, -34.599]
                    ]
                ]
            ]
        }]
    )

    @model_validator(mode="after")
    def validate_geojson(cls, values):
        if values.geometria.get("type") != "MultiPolygon":
            raise ValueError("La geometría debe ser de tipo MultiPolygon")
        return values




class ZonaUpdate(BaseModel):

    nombre : Optional[str] = Field(
        None,
        max_length=100,
        description="Nombre descriptivo de la zona.",
        examples=["Barrio Candioti", "Barrio Sur"]
    )

    descripcion : Optional[str] = Field(
        None,
        description="Descripción detallada de la zona. Especialmente de los limites.",
        examples=["Zona ubicada al norte de la ciudad, delimitada por..."]
    )

    color : Optional[str] = Field(
        None,
        pattern="^#([A-Fa-f0-9]{6})$",
        description="Color representativo de la zona en formato hexadecimal.",
        examples=["#FF5733", "#33FF57"]
    )

    geometria : Optional[Dict[str, Any]] = Field(
        None,
        description="Geometría de la zona en formato GeoJSON.",
        examples=[{
            "type": "MultiPolygon",
            "coordinates": [
                [
                    [
                        [-58.443, -34.599],
                        [-58.442, -34.598],
                        [-58.441, -34.599],
                        [-58.443, -34.599]
                    ]
                ]
            ]
        }]
    )

    @model_validator(mode="after")
    def at_least_one_field(cls, values):
        if not any(values.model_dump(exclude_none=True).values()):
            raise ValueError("Debe enviar al menos un campo para actualizar")
        return values

    @model_validator(mode="after")
    def validate_geojson(cls, values):
        if values.geometria is not None:
            if values.geometria.get("type") != "MultiPolygon":
                raise ValueError("La geometría debe ser de tipo MultiPolygon")
        return values



class ZonaResponse(BaseModel):
    zona_id: int
    codigo: str
    nombre: str
    descripcion: Optional[str]
    color: Optional[str]
    geometria: Dict[str, Any]
    created_at: datetime

    class Config:
        from_attributes = True

    




class ZonaListItem(BaseModel):
    zona_id : int = Field(
        ...,
        description="Identificador único de la zona.",
        examples=[1, 2, 3]
    )

    codigo : str = Field(
        ...,
        max_length=50,
        description="Código único que identifica la zona.",
        examples=["BARRIO_CANDIOTI", "BARRIO_SUR"]
    )

    nombre : str = Field(
        ...,
        max_length=100,
        description="Nombre descriptivo de la zona.",
        examples=["Barrio Candioti", "Barrio Sur"]
    )