from datetime import date, timedelta
from sqlmodel import Session, select
from app.models.employee import Employee, RoleEnum
from app.models.schedule import Schedule, TurnoEnum


def seed_all(session: Session):
    """Seeds the database with realistic demo data for development/testing"""
    
    # Clear existing data for idempotent seeding
    # Delete schedules first to avoid FK constraint issues
    existing_schedules = session.exec(select(Schedule)).all()
    for schedule in existing_schedules:
        session.delete(schedule)
    
    existing_employees = session.exec(select(Employee)).all()
    for employee in existing_employees:
        session.delete(employee)
    
    session.commit()
    
    # Create employees with realistic Spanish names
    employees_data = [
        {"nombre": "Ana García", "email": "ana.garcia@example.com", "role": RoleEnum.ENCARGADO},
        {"nombre": "Luis Martínez", "email": "luis.martinez@example.com", "role": RoleEnum.TRABAJADOR},
        {"nombre": "Carmen López", "email": "carmen.lopez@example.com", "role": RoleEnum.TRABAJADOR},
        {"nombre": "Diego Torres", "email": "diego.torres@example.com", "role": RoleEnum.TRABAJADOR},
        {"nombre": "Marta Ruiz", "email": "marta.ruiz@example.com", "role": RoleEnum.ADMINISTRADOR}
    ]
    
    created_employees = []
    for emp_data in employees_data:
        employee = Employee(**emp_data)
        session.add(employee)
        created_employees.append(employee)
    
    session.commit()
    
    # Refresh employees to get their IDs
    for employee in created_employees:
        session.refresh(employee)
    
    # Tasks (tareas) for future implementation - storing as list for now
    tareas = [
        "Riego viñedo",
        "Poda", 
        "Control de plagas",
        "Cosecha",
        "Mantenimiento tractor"
    ]
    
    # Create schedules for next 2 weeks with varied shifts
    today = date.today()
    turnos = [TurnoEnum.manana, TurnoEnum.tarde, TurnoEnum.noche]
    schedules_data = []
    
    # Create schedules across 14 days (2 weeks) with varied employees and shifts
    for day in range(1, 15):  # Days 1-14
        if day % 2 == 1:  # Odd days: more schedules
            for i in range(2):  # 2 schedules per odd day
                employee_idx = (day + i) % len(created_employees)
                turno_idx = (day + i) % len(turnos)
                schedules_data.append({
                    "empleado_id": created_employees[employee_idx].id,
                    "fecha": today + timedelta(days=day),
                    "turno": turnos[turno_idx]
                })
        else:  # Even days: 1 schedule
            employee_idx = day % len(created_employees)
            turno_idx = day % len(turnos)
            schedules_data.append({
                "empleado_id": created_employees[employee_idx].id,
                "fecha": today + timedelta(days=day),
                "turno": turnos[turno_idx]
            })
    
    created_schedules = []
    for schedule_data in schedules_data:
        schedule = Schedule(**schedule_data)
        session.add(schedule)
        created_schedules.append(schedule)
    
    session.commit()
    
    return {
        "employees": len(created_employees),
        "schedules": len(created_schedules)
    }