from pydantic import BaseModel, Field, EmailStr
from .usuario import UsuarioResponse

#LOGIN MANUAL

class LoginRequest(BaseModel):
    email: EmailStr = Field(
        ...,
        description="Email del usuario"
    )
    password: str = Field(
        ...,
        min_length=8,
        description="Contraseña del usuario"
    )


#LOGIN CON GOOGLE
class GoogleLoginRequest(BaseModel):
    id_token: str = Field(
        ...,
        description="Token de Google OAuth"
    )


class AuthResponse(BaseModel):
    access_token: str = Field(
        ...,
        description="JWT de acceso"
    )
    token_type: str = Field(
        default="bearer",
        description="Tipo de token"
    )
    usuario: UsuarioResponse