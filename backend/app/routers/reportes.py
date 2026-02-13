from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional

from ..dependencies.db import get_db
from ..dependencies.jwt import get_current_user
from ..schemas.reporte import ReporteCreate, ReporteResponse
from ..services.service_reporte import crear_reporte, listar_reportes_admin, listar_reportes_usuario

from ..dependencies.roles import require_roles
from ..utils.constantes import ADMIN, SUPERADMIN, REGISTRADO

router = APIRouter(
    prefix="/reportes",
    tags=["Reportes"],
    dependencies=[Depends(require_roles(ADMIN, SUPERADMIN, REGISTRADO))]
)


@router.post("/", response_model=ReporteResponse, status_code=201)
def crear_reporte_endpoint(
    data: ReporteCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    reporte, error = crear_reporte(
        db=db,
        lat=data.lat,
        lng=data.lng,
        usuario_id=current_user.usuario_id
    )

    if error:
        raise HTTPException(status_code=400, detail=error)

    return reporte



@router.get("/mis-reportes", response_model=list[ReporteResponse])
def mis_reportes(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return listar_reportes_usuario(db, current_user.usuario_id)


@router.get("/", response_model=list[ReporteResponse])
def listar_reportes(
    zona_id: Optional[int] = None,
    fecha_desde: Optional[datetime] = None,
    fecha_hasta: Optional[datetime] = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Solo admin y superadmin pueden usar filtros generales
    if current_user.rol not in [ADMIN, SUPERADMIN]:
        raise HTTPException(status_code=403, detail="No autorizado.")

    return listar_reportes_admin(
        db=db,
        zona_id=zona_id,
        fecha_desde=fecha_desde,
        fecha_hasta=fecha_hasta
    )
