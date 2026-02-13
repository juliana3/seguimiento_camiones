from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..dependencies.db import get_db
from ..dependencies.jwt import get_current_user
from ..schemas.notificaciones import (
    NotificacionResponse,
    NotificacionListItem,
    NotificacionMarkRead
)
from ..services.service_noti import (
    listar_notificaciones_usuario,
    marcar_como_leida)

router = APIRouter(
    prefix="/notificaciones",
    tags=["Notificaciones"],
)


@router.get("/", response_model=List[NotificacionResponse])
def listar_mis_notificaciones(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return listar_notificaciones_usuario(
        db,
        current_user.usuario_id
    )


@router.get("/resumen", response_model=List[NotificacionListItem])
def listar_resumen_notificaciones(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return listar_notificaciones_usuario(
        db,
        current_user.usuario_id
    )


@router.patch("/{notificacion_id}/leer", response_model=NotificacionResponse)
def marcar_notificacion_leida(
    notificacion_id: int,
    data: NotificacionMarkRead,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    notificacion = marcar_como_leida(
        db,
        notificacion_id,
        current_user.usuario_id
    )

    if not notificacion:
        raise HTTPException(
            status_code=404,
            detail="Notificación no encontrada."
        )

    return notificacion
