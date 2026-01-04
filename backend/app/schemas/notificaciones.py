from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class NotificacionResponse(BaseModel):
    notificacion_id: int
    tipo: str
    titulo: Optional[str]
    mensaje: Optional[str]
    canal: str
    leida: bool
    created_at: datetime

    class Config:
        from_attributes = True


class NotificacionListItem(BaseModel):
    notificacion_id: int
    titulo: Optional[str]
    canal: str
    leida: bool
    created_at: datetime

class NotificacionMarkRead(BaseModel):
    leida: bool = True
