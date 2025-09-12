from typing import List
from fastapi import APIRouter, HTTPException, Depends, status
from sqlmodel import Session, select
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr

from app.db import get_session
from app.models.user import User
from app.config import get_settings

router = APIRouter(prefix="/dev", tags=["dev-tools"])
settings = get_settings()

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserInfo(BaseModel):
    id: int
    email: EmailStr
    nombre: str
    role: str
    employee_id: int | None


class ResetPasswordRequest(BaseModel):
    email: EmailStr
    new_password: str


def check_dev_mode():
    """Check if we're in development mode, raise 403 if in production"""
    if settings.APP_ENV == "prod":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Endpoint no disponible en producción"
        )


@router.get("/users", response_model=List[UserInfo])
def list_users(session: Session = Depends(get_session)):
    """List all users (development only)"""
    check_dev_mode()
    
    users = session.exec(select(User)).all()
    return [
        UserInfo(
            id=user.id or 0,
            email=user.email,
            nombre=user.nombre,
            role=user.role.value,
            employee_id=user.employee_id
        )
        for user in users
    ]


@router.post("/reset-password")
def reset_password(
    reset_request: ResetPasswordRequest,
    session: Session = Depends(get_session)
):
    """Reset user password (development only)"""
    check_dev_mode()
    
    # Find user by email
    user = session.exec(
        select(User).where(User.email == reset_request.email)
    ).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    # Hash new password and update
    new_password_hash = pwd_context.hash(reset_request.new_password)
    user.password_hash = new_password_hash
    
    session.add(user)
    session.commit()
    
    return {"ok": True}