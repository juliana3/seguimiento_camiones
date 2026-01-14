from datetime import datetime, timedelta, timezone
from typing import Optional, Union, Any

from jose import jwt 
from passlib.context import CryptContext



from app.config import settings

#CONSTANTES DE SEGURIDAD
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES  # 1 día
REFRESH_TOKEN_EXPIRE_MINUTES = settings.REFRESH_TOKEN_EXPIRE_MINUTES  # 30 días
ALGORITHM = settings.ALGORITHM
SECRET_KEY = settings.JWT_SECRET_KEY



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    #  convierte la contraseña en un hash seguro
    return pwd_context.hash(password)




def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    #crea un jwt con fecha de expiración opcional

    to_encode  = data.copy()

    expire = datetime.now(timezone.utc) + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))

    to_encode.update({"exp": expire})

    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encode_jwt


def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    #crea un jwt con fecha de expiración opcional

    to_encode  = data.copy()
    to_encode.update({"type": "refresh"})

    expire = datetime.now(timezone.utc) + (expires_delta if expires_delta else timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES))

    to_encode.update({"exp": expire})

    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encode_jwt


