from pydantic import BaseModel, Field, model_validator
from typing import Optional, Dict, Any
from datetime import datetime


class CamionCreate(BaseModel):

    patente : str = Field(
        ...,
        pattern="^([A-Z]{3}[0-9]{3}|[A-Z]{2}[0-9]{3}[A-Z]{2})$",
        description="Patente del camión.",
        examples=["ABC123", "AA123BB"]
    )

    zona_id : Optional[int] = Field(
        None,
        description="Identificador de la zona asignada al camión.",
        examples=[1, 2, 3]
    )

    

class CamionUpdate(BaseModel):

    patente : Optional[str] = Field(
        None,
        pattern="^([A-Z]{3}[0-9]{3}|[A-Z]{2}[0-9]{3}[A-Z]{2})$",
        description="Patente del camión.",
        examples=["ABC123", "AA123BB"]
    )

    esta_activo : Optional[bool] = Field(
        None,
        description="Indica si el camión está activo o inactivo. Está activo cuando va a recolectar basura.",
        examples=[True, False]
    )

    zona_id : Optional[int] = Field(
        None,
        description="Identificador de la zona asignada al camión.",
        examples=[1, 2, 3]
    )

    @model_validator(mode="after")
    def at_least_one_field(cls, values):
        if not any(values.model_dump(exclude_none=True).values()):
            raise ValueError("Debe enviar al menos un campo para actualizar")
        return values


class CamionResponse(BaseModel):

    camion_id: int
    patente: str
    esta_activo: bool
    zona_id: Optional[int]
    zona_nombre: Optional[str]
    created_at: datetime
    class Config:
        from_attributes = True

