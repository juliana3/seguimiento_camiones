from fastapi import Depends, HTTPException, status
from ..dependencies.jwt import get_current_user
from ..models.usuario import Usuario





def require_roles(*roles: str):
    def rol_checker(usuario: Usuario = Depends(get_current_user)):
        if usuario.rol not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tenés los permisos necesarios para realizar esta acción."
            )
        
        return usuario
    return rol_checker