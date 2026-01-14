from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime
from enum import Enum


class RolUsuarioEnum(str, Enum):
    PUBLICO = "publico"
    REGISTRADO = "registrado"
    ADMIN = "admin"
    SUPERADMIN = "superadmin"


class AuthProviderEnum(str, Enum):
    LOCAL = "local"
    GOOGLE = "google"


class UsuarioCreate(BaseModel):
    email: EmailStr = Field(
        ...,
        description="Email del usuario"
    )

    password: str = Field(
        ...,
        min_length=8,
        description="Contraseña en texto plano (se hashea en backend)"
    )

    nombre_completo: Optional[str] = Field(
        None,
        description="Nombre completo del usuario"
    )


class UsuarioUpdate(BaseModel):
    nombre_completo: Optional[str] = Field(
        None,
        description="Nombre completo del usuario"
    )

    notificaciones_activadas: Optional[bool] = Field(
        None,
        description="Indica si el usuario recibe notificaciones"
    )

    esta_activo: Optional[bool] = Field(
        None,
        description="Indica si el usuario está activo"
    )

    rol: Optional[RolUsuarioEnum] = Field(
        None,
        description="Rol del usuario (solo admins)"
    )


class UsuarioResponse(BaseModel):
    usuario_id: int
    email: EmailStr
    nombre_completo: Optional[str]

    auth_provider: AuthProviderEnum
    rol: RolUsuarioEnum
    esta_activo: bool
    notificaciones_activadas: bool

    created_at: datetime

    class Config:
        from_attributes = True


class UsuarioListItem(BaseModel):
    usuario_id: int
    email: EmailStr
    rol: RolUsuarioEnum
    esta_activo: bool
