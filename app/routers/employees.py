from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError

from app.db import get_session
from app.models.employee import Employee, EmployeeCreate, EmployeeRead, EmployeeUpdate
from app.security.deps import require_roles

router = APIRouter(prefix="/employees", tags=["employees"])


@router.post("/", response_model=EmployeeRead, status_code=201)
def create_employee(
    employee: EmployeeCreate,
    session: Session = Depends(get_session),
    current_user = Depends(require_roles("Encargado", "Administrador"))
):
    db_employee = Employee.model_validate(employee)
    session.add(db_employee)
    try:
        session.commit()
        session.refresh(db_employee)
        return db_employee
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=409, detail="El correo ya está registrado")


@router.get("/", response_model=List[EmployeeRead])
def list_employees(session: Session = Depends(get_session)):
    employees = session.exec(select(Employee)).all()
    return employees


@router.get("/{employee_id}", response_model=EmployeeRead)
def get_employee(employee_id: int, session: Session = Depends(get_session)):
    employee = session.get(Employee, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    return employee


@router.patch("/{employee_id}", response_model=EmployeeRead)
def update_employee(
    employee_id: int,
    employee_update: EmployeeUpdate,
    session: Session = Depends(get_session),
    current_user = Depends(require_roles("Encargado", "Administrador"))
):
    employee = session.get(Employee, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    
    employee_data = employee_update.model_dump(exclude_unset=True)
    for field, value in employee_data.items():
        setattr(employee, field, value)
    
    session.add(employee)
    try:
        session.commit()
        session.refresh(employee)
        return employee
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=409, detail="El correo ya está registrado")


@router.delete("/{employee_id}")
def delete_employee(
    employee_id: int,
    session: Session = Depends(get_session),
    current_user = Depends(require_roles("Encargado", "Administrador"))
):
    employee = session.get(Employee, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    
    session.delete(employee)
    session.commit()
    return {"message": "Empleado eliminado exitosamente"}