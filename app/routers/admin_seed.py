from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.db import get_session
from app.security.deps import require_roles
from app.seed import seed_all

router = APIRouter(prefix="/admin", tags=["admin"])


@router.post("/seed")
def seed_database(
    session: Session = Depends(get_session),
    current_user = Depends(require_roles("Administrador"))
):
    """Seeds the database with realistic demo data for development/testing"""
    created_counts = seed_all(session)
    
    return {
        "ok": True,
        "created": created_counts
    }