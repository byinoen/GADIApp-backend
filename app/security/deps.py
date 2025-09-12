from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session, select
from app.db import get_session
from app.models.user import User, UserPublic
from app.security.jwt import decode_token

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: Session = Depends(get_session)
) -> UserPublic:
    """Get current user from JWT token"""
    try:
        # Decode the JWT token
        payload = decode_token(credentials.credentials)
        user_id = payload.get("sub")
        
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Get user from database
        user = session.get(User, user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario no encontrado",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return UserPublic(
            id=user.id or 0,  # Handle None case
            email=user.email,
            nombre=user.nombre,
            role=user.role,
            employee_id=user.employee_id
        )
    
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )


def require_roles(*roles: str):
    """Dependency factory to require specific roles"""
    def check_roles(current_user: UserPublic = Depends(get_current_user)):
        if current_user.role.value not in roles:  # Use .value for enum
            raise HTTPException(status_code=403, detail="Permiso denegado")
        return current_user
    return check_roles