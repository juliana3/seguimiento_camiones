from pydantic import BaseModel, Field, model_validator
from typing import Optional, Dict, Any
from datetime import datetime

class RutaCreate(BaseModel):

    nombre : str =  Field(
        ...,
        description="Nombre de la ruta.",
        max_length=50,
        examples=["Ruta_1_Barrio_Sur", "Ruta_2_Centro"]
    )

    direccion : Optional[str] = Field(
        None,
        description="Sentido cardinal de la ruta.",
        examples=["Norte-Sur", "Este-Oeste"]
    )

    geometria : Dict[str, Any] = Field(
        ...,
        description="Geometría de la ruta en formato GeoJSON (LINESTRING).",
        examples=[{
            "type": "LineString",
            "coordinates": [
                [-58.443, -34.599],
                [-58.442, -34.598],
                [-58.441, -34.599]
            ]
        }]
    )

   #Largo en metros y  duracion estimada en minutos  se calculan segun la ruta qque es cargada, no son campos que completa el admin
    descripcion : Optional[str] = Field(
        None,
        description="Descripción adicional de la ruta.",
        examples=["Ruta que conecta el barrio Sur con el centro de la ciudad."]
    )

    @model_validator(mode="after")
    def validate_geojson(cls, values):
        if values.geometria.get("type") != "LineString":
            raise ValueError("La geometría debe ser de tipo LineString")
        return values


class RutaUpdate(BaseModel):

    nombre : Optional[str] =  Field(
        None,
        description="Nombre de la ruta.",
        max_length=50,
        examples=["Ruta_1_Barrio_Sur", "Ruta_2_Centro"]
    )

    direccion : Optional[str] = Field(
        None,
        description="Sentido cardinal de la ruta.",
        examples=["Norte-Sur", "Este-Oeste"]
    )

    geometria : Optional[Dict[str, Any]] = Field(
        None,
        description="Geometría de la ruta en formato GeoJSON (LINESTRING).",
        examples=[{
            "type": "LineString",
            "coordinates": [
                [-58.443, -34.599],
                [-58.442, -34.598],
                [-58.441, -34.599]
            ]
        }]
    )

    descripcion : Optional[str] = Field(
        None,
        description="Descripción adicional de la ruta.",
        examples=["Ruta que conecta el barrio Sur con el centro de la ciudad."]
    )

    @model_validator(mode="after")
    def at_least_one_field(cls, values):
        if not any(values.model_dump(exclude_none=True).values()):
            raise ValueError("Debe enviar al menos un campo para actualizar")
        return values

    @model_validator(mode="after")
    def validate_geojson(cls, values):
        geojson = values.geometria
        if geojson and geojson.get("type") != "LineString":
            raise ValueError("La geometría debe ser de tipo LineString")
        return values


class RutaResponse(BaseModel):
    ruta_id: int
    nombre: str
    direccion: Optional[str]
    geometria: Dict[str, Any]
    largo_metros: Optional[int]
    duracion_estimada_minutos: Optional[int]
    zona_id: int 
    created_at: datetime

    class Config:
        from_attributes = True


class RutaListItem(BaseModel):
    ruta_id: int = Field(
        ...,
        description="Identificador único de la ruta.",  
        examples=[1, 2, 3]
    )

    nombre: str = Field(
        ...,
        description="Nombre de la ruta.",
        max_length=50,
        examples=["Ruta_1_Barrio_Sur", "Ruta_2_Centro"]
    )

    direccion: Optional[str] = Field(
        None,
        description="Sentido cardinal de la ruta.",
        examples=["Norte-Sur", "Este-Oeste"]
    )


