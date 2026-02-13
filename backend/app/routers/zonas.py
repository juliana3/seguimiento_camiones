from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session

from ..dependencies.db import get_db
from ..dependencies.roles import require_roles
from ..utils.constantes import ADMIN, SUPERADMIN

from ..models.zona import Zona
from ..models.ruta import Ruta
from ..schemas.ruta import RutaCreate, RutaResponse
from ..schemas.zona import ZonaCreate, ZonaResponse, ZonaUpdate, ZonaListItem

from ..services.service_ruta import calcular_metricas_ruta

router = APIRouter(
    prefix="/zonas",
    tags=["Zonas"],
    dependencies=[
        Depends(require_roles(ADMIN, SUPERADMIN))
    ]
)


@router.get("/", response_model=list[ZonaListItem])
def listar_zonas(db:Session =   Depends(get_db)):
    return db.query(Zona).all()


@router.post("/", response_model=ZonaResponse, status_code=201)
def crear_zona(data: ZonaCreate, db: Session =Depends(get_db)):
    zona = Zona(**data.model_dump())
    db.add(zona)
    db.commit()
    db.refresh(zona)

    return zona


@router.patch("/{zona_id}", response_model=ZonaResponse)
def modificar_zona(
    zona_id : int,
    data : ZonaUpdate,
    db : Session = Depends(get_db)
):
    zona = db.query(Zona).get(zona_id)

    if not zona:
        raise HTTPException(
            status_code=404,
            detail="Zona no encontrada."
        )
    

    for campo, valor in data.model_dump(exclude_unset=True).items():
        setattr(zona, campo, valor)

    db.commit()
    db.refresh(zona)

    return zona


@router.post("/{zona_id}/rutas",response_model=RutaResponse,status_code=201)
def crear_ruta(
    zona_id: int,
    data: RutaCreate,
    db: Session = Depends(get_db)
):
    zona = db.query(Zona).get(zona_id)

    if not zona:
        raise HTTPException(
            status_code=404,
            detail="Zona inexistente"
        )

    ruta = Ruta(
        **data.model_dump(),
        zona_id=zona_id
    )


    db.add(ruta)
    db.flush()  # Asegura que ruta_id esté disponible para calcular métricas

    ruta = calcular_metricas_ruta(db, ruta)

    db.commit()
    db.refresh(ruta)

    return ruta