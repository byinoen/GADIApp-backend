from fastapi import APIRouter, HTTPException, Depends, status
from sqlmodel import Session, select
from passlib.context import CryptContext

from app.db import get_session
from app.models.user import User, UserLogin, UserPublic, UserRegister, UserBootstrap
from app.models.employee import RoleEnum
from app.security.jwt import create_access_token
from app.security.deps import get_current_user, require_roles
from app.config import get_settings

router = APIRouter(prefix="/auth", tags=["auth"])
settings = get_settings()

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)


@router.post("/register")
def register(
    user_data: UserRegister,
    session: Session = Depends(get_session),
    current_user: UserPublic = Depends(require_roles("Administrador"))
):
    """Register a new user (Admin only)"""
    # Check if user already exists
    existing_user = session.exec(
        select(User).where(User.email == user_data.email)
    ).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El usuario ya existe"
        )
    
    # Create new user with hashed password
    hashed_password = get_password_hash(user_data.password)
    db_user = User(
        email=user_data.email,
        nombre=user_data.nombre,
        role=user_data.role,
        password_hash=hashed_password,
        employee_id=user_data.employee_id
    )
    
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    
    return UserPublic(
        id=db_user.id or 0,
        email=db_user.email,
        nombre=db_user.nombre,
        role=db_user.role,
        employee_id=db_user.employee_id
    )


@router.post("/login")
def login(user_login: UserLogin, session: Session = Depends(get_session)):
    """Login with email and password"""
    # Find user by email
    user = session.exec(
        select(User).where(User.email == user_login.email)
    ).first()
    
    if not user or not verify_password(user_login.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserPublic(
            id=user.id or 0,
            email=user.email,
            nombre=user.nombre,
            role=user.role,
            employee_id=user.employee_id
        )
    }


@router.get("/me", response_model=UserPublic)
def get_current_user_info(current_user: UserPublic = Depends(get_current_user)):
    """Get current user information"""
    return current_user


@router.post("/bootstrap")
def bootstrap_first_admin(payload: dict, session: Session = Depends(get_session)):
    # Works ONLY when there are zero users
    total = len(session.exec(select(User)).all())
    if total and total > 0:
        raise HTTPException(status_code=409, detail="Bootstrap no disponible")

    email = payload.get("email")
    nombre = payload.get("nombre")
    password = payload.get("password")
    if not email or not nombre or not password:
        raise HTTPException(status_code=400, detail="email, nombre y password son obligatorios")

    hashed = pwd_context.hash(password)
    user = User(email=email, nombre=nombre, role=RoleEnum.ADMINISTRADOR, password_hash=hashed, employee_id=None)
    session.add(user)
    session.commit()
    session.refresh(user)
    return {"ok": True, "user": {"id": user.id, "email": user.email, "nombre": user.nombre, "role": user.role}}