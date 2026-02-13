from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session

from ..dependencies.db import get_db
from ..db.session import SessionLocal
from ..dependencies.roles import require_roles
from ..utils.constantes import ADMIN, SUPERADMIN

from ..models.camion import Camion
from ..schemas.camion import CamionCreate, CamionUpdate, CamionResponse

router = APIRouter(
    prefix="/camiones", 
    tags=["Camiones"],
    dependencies=[
        Depends(require_roles(ADMIN, SUPERADMIN))
    ])



@router.get("/",  response_model=list[CamionResponse])
def listar_camiones(db: Session = Depends(get_db)):
    return db.query(Camion).all()

@router.post("/", response_model=CamionResponse, status_code=201)
def crear_camion(data : CamionCreate, db: Session = Depends(get_db)):
    camion = Camion(**data.model_dump())
    db.add(camion)
    db.commit()
    db.refresh(camion)

    return camion


@router.patch("/{camion_id}", response_model=CamionResponse)
def modificar_camion(
    camion_id : int, 
    data: CamionUpdate, 
    db: Session = Depends(get_db)):

    camion = db.query(Camion).get(camion_id)

    if not camion:
        raise HTTPException(
            status_code=404,
            detail="Camión no encontrado."
        )
    
    for campo, valor in data.model_dump(exclude_unset=True).items():
        setattr(camion,campo,valor)



    db.commit()
    db.refresh(camion)

    return camion

    