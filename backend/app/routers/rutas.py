from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session

from ..dependencies.db import get_db
from ..dependencies.roles import require_roles
from ..utils.constantes import ADMIN, SUPERADMIN

from ..models.ruta import Ruta
from ..models.zona import Zona
from ..schemas.ruta import RutaCreate, RutaResponse, RutaUpdate, RutaListItem

router =  APIRouter(
    prefix="/rutas",
    tags=["Rutas"],
    dependencies=[
        Depends(require_roles(ADMIN, SUPERADMIN))
    ]
)


@router.get("/", response_model=list[RutaListItem])
def listar_rutas(db :Session = Depends(get_db)):
    return db.query(Ruta).all()


@router.get("/{ruta_id}", response_model=RutaResponse)
def obtener_ruta(ruta_id: int, db: Session = Depends(get_db)):
    ruta = db.query(Ruta).get(ruta_id)

    if not ruta:
        raise HTTPException(status_code=404, detail="Ruta no encontrada")

    return ruta




