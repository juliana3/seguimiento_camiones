from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session

from ..dependencies.db import get_db
from ..dependencies.roles import require_roles
from ..utils.constantes import ADMIN, SUPERADMIN

from ..models.horario import Horario
from ..schemas.horario import HorarioCreate, HorarioUpdate, HorarioResponse
from ..models.zona import Zona

router = APIRouter(
    prefix="/horarios",
    tags=["Horarios"],
    dependencies=[
        Depends(require_roles(ADMIN, SUPERADMIN))
    ]
)

#listar horarios
@router.get("/", response_model=list[HorarioResponse])
def listar_horarios(db: Session = Depends(get_db)):
    return db.query(Horario).all()


#crear horario
@router.post("/", response_model=HorarioResponse, status_code=201)
def crear_horario(data: HorarioCreate, db : Session = Depends(get_db)):

    #validar que la zona existe
    zona = db.query(Zona).get(data.zona_id)
    if not zona:
        raise HTTPException(
            status_code=404,
            detail="Zona no encontrada."
        )
    
    #validar que no exista un horario para la zona en ese diaa
    existe_horario = db.query(Horario).filter(
        Horario.zona_id == data.zona_id,
        Horario.dia_semana == data.dia_semana
    ).first()

    if existe_horario:
        raise HTTPException(
            status_code=400,
            detail="Ya existe un horario para esa zona en ese día."
        )
    
    #validar la exclusion de sabados / domingos
    if zona.excluye_dia is not None:
        if data.dia_semana == zona.excluye_dia:
            raise HTTPException(
                status_code=400,
                detail=f"No se pueden crear horarios para {data.dia_semana.name} en la zona {zona.nombre}."
            )
    

    #ccrear el horario
    horario = Horario(**data.model_dump())
    db.add(horario)
    db.commit()
    db.refresh(horario)

    return horario



#modificar horario
@router.patch("/{horario_id}", response_model=HorarioResponse)
def modificar_horario(horario_id : int, data: HorarioUpdate, db : Session = Depends(get_db)):
    horario = db.query(Horario).get(horario_id)

    if not horario:
        raise HTTPException(
            status_code=404,
            detail="Horario no encontrado."
        )
    
    for campo, valor in data.model_dump(exclude_unset=True).items():
        setattr(horario,campo,valor)

    db.commit()
    db.refresh(horario)

    return horario


#eliminar horario
@router.delete("/{horario_id}", status_code=204)
def eliminar_horario(horario_id : int, db : Session = Depends(get_db)):
    horario = db.query(Horario).get(horario_id)

    if not horario:
        raise HTTPException(
            status_code=404,
            detail="Horario no encontrado."
        )
    
    db.delete(horario)
    db.commit()