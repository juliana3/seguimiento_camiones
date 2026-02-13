from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from sqlalchemy.orm import Session
from app.models.usuario import Usuario
from app.config import settings

from .db import get_db
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")




def get_current_user(token: str =  Depends(oauth2_scheme), db: Session = Depends(get_db)) -> Usuario:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales invalidas",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM])

        user_id = payload.get("sub")
        if not user_id:
            raise credentials_exception
        
        user_id = int(user_id)

    except JWTError:
        raise credentials_exception
    
    usuario = (
        db.query(Usuario)
        .filter(Usuario.usuario_id == user_id)
        .first()
    )

    if not usuario or not usuario.esta_activo: # type: ignore
        raise credentials_exception
    
    return usuario

        