from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.db import get_session
from app.security.deps import require_roles
from app.seed import seed_all
from app.models.user import User
from app.config import get_settings

router = APIRouter(prefix="/admin", tags=["admin"])


@router.post("/seed")
def seed_database(session: Session = Depends(get_session)):
    """Seeds the database with realistic demo data for development/testing
    
    Only allowed in local development environment. In production, use /admin/seed-admin with authentication.
    """
    settings = get_settings()
    
    # Only allow seeding in local development environment
    if settings.APP_ENV != "local":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Seeding solo está disponible en entorno de desarrollo local. Use /admin/seed-admin con autenticación de administrador."
        )
    
    created_counts = seed_all(session)
    
    return {
        "ok": True,
        "created": created_counts
    }


@router.post("/bootstrap")
def bootstrap_database(
    bootstrap_secret: str, 
    session: Session = Depends(get_session)
):
    """Bootstrap database initialization for production deployment
    
    Requires the BOOTSTRAP_SECRET and can only be used when no users exist.
    """
    settings = get_settings()
    
    # Check if any users exist in the database
    existing_users = session.exec(select(User)).first()
    if existing_users is not None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="La base de datos ya está inicializada."
        )
    
    # In production, require bootstrap secret
    if settings.APP_ENV != "local":
        if not settings.BOOTSTRAP_SECRET or bootstrap_secret != settings.BOOTSTRAP_SECRET:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Bootstrap secret requerido para inicialización en producción."
            )
    
    created_counts = seed_all(session)
    
    return {
        "ok": True,
        "created": created_counts,
        "message": "Base de datos inicializada exitosamente"
    }


@router.post("/seed-admin")
def seed_database_admin(
    session: Session = Depends(get_session),
    current_user = Depends(require_roles("Administrador"))
):
    """Admin-only database seeding endpoint for production environments"""
    created_counts = seed_all(session)
    
    return {
        "ok": True,
        "created": created_counts
    }