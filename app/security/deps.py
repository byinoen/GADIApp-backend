from typing import List
from fastapi import Header, HTTPException, Depends
from app.models.user import UserPublic

# Mock current user storage for demo
_current_user_storage = {}


def get_current_user(
    x_demo_token: str = Header(None),
    x_demo_role: str = Header(None)
) -> UserPublic:
    if x_demo_token != "demo":
        raise HTTPException(status_code=401, detail="No autenticado")
    
    # For testing purposes, allow role override via header
    if x_demo_role and x_demo_role in ["Trabajador", "Encargado", "Administrador"]:
        return UserPublic(
            id=1,
            email="demo@example.com",
            role=x_demo_role  # type: ignore
        )
    
    # Return stored user or default
    user = _current_user_storage.get("demo_user")
    if not user:
        # Default user for testing
        user = UserPublic(
            id=1,
            email="demo@example.com", 
            role="Trabajador"
        )
    
    return user


def set_current_user(user: UserPublic):
    """Helper to set current user after login"""
    _current_user_storage["demo_user"] = user


def require_roles(*roles: str):
    """Dependency factory to require specific roles"""
    def check_roles(current_user: UserPublic = Depends(get_current_user)):
        if current_user.role not in roles:
            raise HTTPException(status_code=403, detail="Permiso denegado")
        return current_user
    return check_roles