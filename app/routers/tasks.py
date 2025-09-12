from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError

from app.db import get_session
from app.models.task import Task, TaskCreate, TaskRead, TaskUpdate
from app.security.deps import require_roles

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/", response_model=List[TaskRead])
def list_tasks(session: Session = Depends(get_session)):
    """List all tasks"""
    tasks = session.exec(select(Task)).all()
    return tasks


@router.get("/{task_id}", response_model=TaskRead)
def get_task(task_id: int, session: Session = Depends(get_session)):
    """Get a specific task by ID"""
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return task


@router.post("/", response_model=TaskRead, status_code=201)
def create_task(
    task: TaskCreate,
    session: Session = Depends(get_session),
    current_user = Depends(require_roles("Encargado", "Administrador"))
):
    """Create a new task (requires Encargado or Administrador role)"""
    db_task = Task.model_validate(task)
    session.add(db_task)
    try:
        session.commit()
        session.refresh(db_task)
        return db_task
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=400, detail="Error al crear la tarea")


@router.patch("/{task_id}", response_model=TaskRead)
def update_task(
    task_id: int,
    task_update: TaskUpdate,
    session: Session = Depends(get_session),
    current_user = Depends(require_roles("Encargado", "Administrador"))
):
    """Update a task (requires Encargado or Administrador role)"""
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    
    task_data = task_update.model_dump(exclude_unset=True)
    for field, value in task_data.items():
        setattr(task, field, value)
    
    session.add(task)
    try:
        session.commit()
        session.refresh(task)
        return task
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=400, detail="Error al actualizar la tarea")


@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    session: Session = Depends(get_session),
    current_user = Depends(require_roles("Administrador"))
):
    """Delete a task (requires Administrador role only)"""
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    
    session.delete(task)
    session.commit()
    return {"message": "Tarea eliminada exitosamente"}