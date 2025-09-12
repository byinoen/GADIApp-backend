from datetime import date, timedelta
from sqlmodel import Session, select
from passlib.context import CryptContext
from app.models.employee import Employee, RoleEnum
from app.models.schedule import Schedule, TurnoEnum
from app.models.task import Task
from app.models.user import User

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def seed_all(session: Session):
    """Seeds the database with realistic demo data for development/testing"""
    
    # Clear existing data for idempotent seeding (except users)
    # Delete in order to avoid FK constraint issues: schedules -> employees -> tasks
    existing_schedules = session.exec(select(Schedule)).all()
    for schedule in existing_schedules:
        session.delete(schedule)
    
    existing_employees = session.exec(select(Employee)).all()
    for employee in existing_employees:
        session.delete(employee)
    
    existing_tasks = session.exec(select(Task)).all()
    for task in existing_tasks:
        session.delete(task)
    
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
    
    # Create tasks (tareas) using the Task model
    tareas_data = [
        {"nombre": "Riego viñedo", "descripcion": "Riego de las plantas del viñedo", "activo": True},
        {"nombre": "Poda", "descripcion": "Poda de ramas y hojas de las vides", "activo": True},
        {"nombre": "Control de plagas", "descripcion": "Inspección y tratamiento contra plagas", "activo": True},
        {"nombre": "Cosecha", "descripcion": "Recolección de uvas maduras", "activo": True},
        {"nombre": "Mantenimiento tractor", "descripcion": "Revisión y mantenimiento de maquinaria", "activo": True}
    ]
    
    created_tasks = []
    for task_data in tareas_data:
        task = Task(**task_data)
        session.add(task)
        created_tasks.append(task)
    
    session.commit()
    
    # Refresh tasks to get their IDs
    for task in created_tasks:
        session.refresh(task)
    
    # Create users mapped to some employees (idempotent - skip if email exists)
    users_data = [
        {
            "email": "ana.garcia@example.com",
            "nombre": "Ana García", 
            "role": RoleEnum.ENCARGADO,
            "password": "1234",
            "employee_id": created_employees[0].id  # Ana García
        },
        {
            "email": "luis.martinez@example.com",
            "nombre": "Luis Martínez",
            "role": RoleEnum.TRABAJADOR, 
            "password": "1234",
            "employee_id": created_employees[1].id  # Luis Martínez
        },
        {
            "email": "marta.ruiz@example.com",
            "nombre": "Marta Ruiz",
            "role": RoleEnum.ADMINISTRADOR,
            "password": "1234", 
            "employee_id": created_employees[4].id  # Marta Ruiz
        },
        {
            "email": "admin@gadi.com",
            "nombre": "Administrador Sistema",
            "role": RoleEnum.ADMINISTRADOR,
            "password": "admin123",
            "employee_id": None  # System admin without employee link
        }
    ]
    
    created_users = []
    for user_data in users_data:
        # Check if user already exists (idempotent)
        existing_user = session.exec(
            select(User).where(User.email == user_data["email"])
        ).first()
        
        if existing_user:
            created_users.append(existing_user)
            continue
            
        # Hash the password and create new user
        password_hash = pwd_context.hash(user_data["password"])
        
        user = User(
            email=user_data["email"],
            nombre=user_data["nombre"],
            role=user_data["role"],
            password_hash=password_hash,
            employee_id=user_data["employee_id"]
        )
        session.add(user)
        created_users.append(user)
    
    session.commit()
    
    # Refresh users to get their IDs
    for user in created_users:
        session.refresh(user)
    
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
        "schedules": len(created_schedules),
        "tasks": len(created_tasks),
        "users": len(created_users)
    }