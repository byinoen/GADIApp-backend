from datetime import date
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError

from app.db import get_session
from app.models.schedule import Schedule, ScheduleCreate, ScheduleRead, ScheduleUpdate
from app.security.deps import require_roles

router = APIRouter(prefix="/schedules", tags=["schedules"])


@router.post("/", response_model=ScheduleRead, status_code=201)
def create_schedule(
    schedule: ScheduleCreate,
    session: Session = Depends(get_session),
    current_user = Depends(require_roles("Encargado", "Administrador"))
):
    db_schedule = Schedule.model_validate(schedule)
    session.add(db_schedule)
    try:
        session.commit()
        session.refresh(db_schedule)
        return db_schedule
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=400, detail="Error al crear el horario")


@router.get("/", response_model=List[ScheduleRead])
def list_schedules(
    session: Session = Depends(get_session),
    empleado_id: Optional[int] = Query(None),
    fecha_from: Optional[date] = Query(None),
    fecha_to: Optional[date] = Query(None)
):
    query = select(Schedule)
    
    if empleado_id is not None:
        query = query.where(Schedule.empleado_id == empleado_id)
    
    if fecha_from is not None:
        query = query.where(Schedule.fecha >= fecha_from)
    
    if fecha_to is not None:
        query = query.where(Schedule.fecha <= fecha_to)
    
    schedules = session.exec(query).all()
    return schedules


@router.get("/{schedule_id}", response_model=ScheduleRead)
def get_schedule(schedule_id: int, session: Session = Depends(get_session)):
    schedule = session.get(Schedule, schedule_id)
    if not schedule:
        raise HTTPException(status_code=404, detail="Horario no encontrado")
    return schedule


@router.patch("/{schedule_id}", response_model=ScheduleRead)
def update_schedule(
    schedule_id: int,
    schedule_update: ScheduleUpdate,
    session: Session = Depends(get_session),
    current_user = Depends(require_roles("Encargado", "Administrador"))
):
    schedule = session.get(Schedule, schedule_id)
    if not schedule:
        raise HTTPException(status_code=404, detail="Horario no encontrado")
    
    schedule_data = schedule_update.model_dump(exclude_unset=True)
    for field, value in schedule_data.items():
        setattr(schedule, field, value)
    
    session.add(schedule)
    try:
        session.commit()
        session.refresh(schedule)
        return schedule
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=400, detail="Error al actualizar el horario")


@router.delete("/{schedule_id}")
def delete_schedule(
    schedule_id: int,
    session: Session = Depends(get_session),
    current_user = Depends(require_roles("Encargado", "Administrador"))
):
    schedule = session.get(Schedule, schedule_id)
    if not schedule:
        raise HTTPException(status_code=404, detail="Horario no encontrado")
    
    session.delete(schedule)
    session.commit()
    return {"message": "Horario eliminado exitosamente"}