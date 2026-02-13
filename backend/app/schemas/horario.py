from enum import Enum, IntEnum
from pydantic import BaseModel, Field, model_validator
from typing import Optional, Dict, Any
from datetime import datetime, time

from ..utils.constantes import DiaSemanaEnum, TipoResiduoEnum






class HorarioCreate(BaseModel):

    zona_id: int = Field(
        ...,
        description="ID de la zona asociada al horario")
    
    dia_semana: DiaSemanaEnum = Field( 
        ...,
        description="Día de la semana (0=Domingo, 6=Sábado)")
    
    hora_inicio: time = Field(
        ...,
        description="Hora de inicio del turno"
    )

    hora_fin: time = Field(
        ...,
        description="Hora de fin del turno"
    )
    
    tipo_residuo: TipoResiduoEnum = Field(
        ...,
        description="Tipo de residuo que se recoge en este horario y en este dia"
    )

    @model_validator(mode="after")
    def validate_horas(cls, values):
        if values.hora_inicio >= values.hora_fin:
            raise ValueError("La hora de inicio debe ser anterior a la hora de fin")
        return values

    


class HorarioUpdate(BaseModel):
    
    dia_semana: Optional[DiaSemanaEnum] = Field(
        None,
        description="Día de la semana (0=Domingo, 6=Sábado)")
    
    hora_inicio: Optional[time] = Field(
        None,
        description="Hora de inicio del turno"
    )

    hora_fin: Optional[time] = Field(
        None,
        description="Hora de fin del turno"
    )

    tipo_residuo: Optional[TipoResiduoEnum] = Field(
        None,
        description="Tipo de residuo que se recoge en este horario y en este dia"
    )

    @model_validator(mode="after")
    def at_least_one_field(cls, values):
        if not any(values.model_dump(exclude_none=True).values()):
            raise ValueError("Debe enviar al menos un campo para actualizar")
        return values

    @model_validator(mode="after")
    def validate_horas(cls, values):
        if values.hora_inicio and values.hora_fin:
            if values.hora_inicio >= values.hora_fin:
                raise ValueError("La hora de inicio debe ser anterior a la hora de fin")
        return values




class HorarioResponse(BaseModel):

    horario_id: int
    zona_id: int
    nombre_zona: Optional[str]
    dia_semana: DiaSemanaEnum
    hora_inicio: time
    hora_fin: time
    tipo_residuo: TipoResiduoEnum
    created_at: datetime

    class Config:
        from_attributes = True

