from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from geoalchemy2.shape import from_shape
from shapely.geometry import Point

from ..dependencies.db import get_db
from ..dependencies.roles import require_roles
from ..dependencies.zona import get_zona_por_punto
from ..dependencies.jwt import get_current_user

from ..utils.constantes import REGISTRADO
from ..models.ubicacion_usuario import UbicacionUsuario
from ..schemas.ubicacion_usuario import UbicacionUsuarioResponse, UbicacionUsuarioCreate, UbicacionUsuarioUpdate
from ..models.usuario import Usuario


router = APIRouter(
    prefix= "/ubicaciones",
    tags= ["Ubicaciones Usuario"],
    dependencies=[
        Depends(require_roles(REGISTRADO))  
    ]
)

@router.post("/", response_model=UbicacionUsuarioResponse, status_code=201)
def crear_ubicacion(data: UbicacionUsuarioCreate, db: Session = Depends(get_db), current_user : Usuario = Depends(get_current_user)):
    #crear un punto a partir de latitud y longitud
    punto_geografico = from_shape(Point(data.lng, data.lat), srid=4326)
    

    #verificar uy guardar la zona
    zona = get_zona_por_punto(db, punto_geografico)
    if not zona:
        raise HTTPException(
            status_code = 404,
            detail = "La ubicación proporcionada no pertenece a ninguna zona cubierta."
        )


    #si la ubicacion es la prinncipal, desmarcar las otras
    if data.es_principal:
        db.query(UbicacionUsuario).filter(UbicacionUsuario.usuario_id == current_user.usuario_id, UbicacionUsuario.es_principal == True).update({"es_principal": False})

    
    #armo la ubicacion
    ubicacion = UbicacionUsuario(
        nombre = data.nombre,
        direccion_texto = data.direccion,
        ubicacion = punto_geografico,
        es_principal = data.es_principal,
        zona_id = zona.zona_id,
        usuario_id = current_user.usuario_id
    )

    db.add(ubicacion)
    db.commit()
    db.refresh(ubicacion)

    return ubicacion


@router.get("/", response_model=list[UbicacionUsuarioResponse])
def listar_ubicaciones(db: Session = Depends(get_db), current_user : Usuario = Depends(get_current_user)):
    return db.query(UbicacionUsuario).filter(UbicacionUsuario.usuario_id == current_user.usuario_id).order_by(UbicacionUsuario.es_principal.desc(), UbicacionUsuario.created_at.asc()).all()


@router.patch("/{ubicacion_id}", response_model=UbicacionUsuarioResponse)
def actualizar_ubicacion(
    ubicacion_id : int,
    data : UbicacionUsuarioUpdate,
    db : Session = Depends(get_db),
    current_user : Usuario = Depends(get_current_user) 
):
    ubicacion = db.query(UbicacionUsuario).filter(
        UbicacionUsuario.usuario_id == current_user.usuario_id, 
        UbicacionUsuario.ubicacion_usuario_id == ubicacion_id).first()
    
    if not ubicacion: 
        raise HTTPException(
            status_code = 404,
            detail = "Ubicación de usuario no encontrada."
        )
    
    if data.es_principal is True:
        db.query(UbicacionUsuario).filter(
            UbicacionUsuario.usuario_id == current_user.usuario_id,
            UbicacionUsuario.es_principal == True,
            UbicacionUsuario.usuario_id == current_user.usuario_id
        ).update({"es_principal": False}, synchronize_session=False)

    #excluir lat y lng
    for campo, valor in data.model_dump(exclude_unset=True, exclude={"lat","lng"}).items():
        setattr(ubicacion, campo, valor)

    db.commit()
    db.refresh(ubicacion)

    return ubicacion


@router.delete("/{ubicacion_id}", status_code=204)
def eliminar_ubicacion(
    ubicacion_id : int,
    db : Session = Depends(get_db),
    current_user : Usuario = Depends(get_current_user)
):
    
    ubicacion = db.query(UbicacionUsuario).filter(
        UbicacionUsuario.usuario_id == current_user.usuario_id,
        UbicacionUsuario.ubicacion_usuario_id == ubicacion_id
    ).first()

    if not ubicacion:
        raise HTTPException(
            status_code = 404,
            detail = "Ubicación de usuario no encontrada."
        )
    

    db.delete(ubicacion)
    db.commit()




