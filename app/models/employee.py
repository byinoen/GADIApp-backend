from typing import Optional
from enum import Enum
from sqlmodel import SQLModel, Field, UniqueConstraint
from pydantic import EmailStr


class RoleEnum(str, Enum):
    TRABAJADOR = "Trabajador"
    ENCARGADO = "Encargado"
    ADMINISTRADOR = "Administrador"


class EmployeeBase(SQLModel):
    nombre: str
    email: EmailStr
    role: RoleEnum


class Employee(EmployeeBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    
    __table_args__ = (UniqueConstraint("email"),)


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeRead(EmployeeBase):
    id: int


class EmployeeUpdate(SQLModel):
    nombre: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[RoleEnum] = None