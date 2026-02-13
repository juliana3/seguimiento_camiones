from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies.db import get_db
from app.schemas.auth import LoginRequest, GoogleLoginRequest, AuthResponse
from app.models.usuario import Usuario
from app.utils.jwt import (create_access_token, create_refresh_token)
from app.utils.security import (verify_password)




router = APIRouter(prefix="/auth", tags=["Auth"])

"""
    * BUSCA USUARIO POR EMAIL
    * VERIFICA LA CONTRASEÑA
    * FERIFICA QUE EL USUARIO ESTE ACTIVO
    * GENERA EL JWT
    * DEVUELVE EL AUTHRESPONSE
"""


#LOGIN MANUAL
@router.post("/login", response_model=AuthResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    usuario = (db.query(Usuario).filter(Usuario.email == data.email).first())

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales invalidas"
        )
    
    if usuario.auth_provider != "local": # type: ignore
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Este usuario debe iniciar sesión con Google"
        )
    
    if not usuario.password_hash or not verify_password(data.password, usuario.password_hash): # type: ignore
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales invalidas"
        )
    
    if not usuario.esta_activo: # type: ignore
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario desactivado"
        )
    

    access_token = create_access_token(data={"sub": str(usuario.usuario_id)})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "usuario": usuario
    }



#LOGIN CON GOOGLE
@router.post("/google", response_model=AuthResponse)
def google_login(data: GoogleLoginRequest, db:Session = Depends(get_db)):
    #CODIGO BASE ---> REVISSAR DESPUES

    google_payload = {
        "email": "usuario@gmail.com",
        "sub": "google-uique-id"
    }

    email = google_payload["email"]
    google_id = google_payload["sub"]


    usuario = (db.query(Usuario).filter(Usuario.email == email).first())

    if not usuario:
        usuario = Usuario(
            email=email,
            google_id=google_id,
            auth_provider="google",
            rol="registrado"
        )

        db.add(usuario)
        db.commit()
        db.refresh(usuario)

    
    if not usuario.esta_activo: # type: ignore
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario desactivado"
        )
    

    access_token = create_access_token(data={"sub": str(usuario.usuario_id)})

    return{
        "access_token": access_token,
        "token_type": "bearer",
        "usuario": usuario
    }


