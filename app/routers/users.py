from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from passlib.context import CryptContext

from app.db import get_session
from app.models.user import User, UserCreate, UserRead, UserUpdate
from app.security.deps import get_current_user, require_roles

router = APIRouter(prefix="/api/v1/users", tags=["users"])

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.get("/", response_model=List[UserRead])
def list_users(
    session: Session = Depends(get_session),
    current_user = Depends(require_roles("Administrador"))
):
    """List all users (Admin only)"""
    users = session.exec(select(User)).all()
    return [
        UserRead(
            id=user.id or 0,
            email=user.email,
            nombre=user.nombre,
            role=user.role,
            employee_id=user.employee_id
        )
        for user in users
    ]


@router.get("/{user_id}", response_model=UserRead)
def get_user(
    user_id: int,
    session: Session = Depends(get_session),
    current_user = Depends(require_roles("Administrador"))
):
    """Get user by ID (Admin only)"""
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    return UserRead(
        id=user.id or 0,
        email=user.email,
        nombre=user.nombre,
        role=user.role,
        employee_id=user.employee_id
    )


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(
    user_data: UserCreate,
    session: Session = Depends(get_session),
    current_user = Depends(require_roles("Administrador"))
):
    """Create new user (Admin only)"""
    # Check if email already exists
    existing_user = session.exec(
        select(User).where(User.email == user_data.email)
    ).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El correo ya está registrado"
        )
    
    # Hash password
    hashed_password = pwd_context.hash(user_data.password)
    
    # Create user
    db_user = User(
        email=user_data.email,
        nombre=user_data.nombre,
        role=user_data.role,
        employee_id=user_data.employee_id,
        password_hash=hashed_password
    )
    
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    
    return UserRead(
        id=db_user.id or 0,
        email=db_user.email,
        nombre=db_user.nombre,
        role=db_user.role,
        employee_id=db_user.employee_id
    )


@router.patch("/{user_id}", response_model=UserRead)
def update_user(
    user_id: int,
    user_update: UserUpdate,
    session: Session = Depends(get_session),
    current_user = Depends(require_roles("Administrador"))
):
    """Update user (Admin only)"""
    # Get existing user
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    # Check for duplicate email if email is being updated
    if user_update.nombre is not None:
        user.nombre = user_update.nombre
    
    if user_update.role is not None:
        user.role = user_update.role
    
    if user_update.employee_id is not None:
        user.employee_id = user_update.employee_id
    
    # Hash new password if provided
    if user_update.password is not None:
        user.password_hash = pwd_context.hash(user_update.password)
    
    session.add(user)
    session.commit()
    session.refresh(user)
    
    return UserRead(
        id=user.id or 0,
        email=user.email,
        nombre=user.nombre,
        role=user.role,
        employee_id=user.employee_id
    )


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    session: Session = Depends(get_session),
    current_user = Depends(require_roles("Administrador"))
):
    """Delete user (Admin only)"""
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    session.delete(user)
    session.commit()
    
    return None