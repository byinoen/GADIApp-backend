from typing import Optional
from pydantic import BaseModel, EmailStr
from sqlmodel import SQLModel, Field
from app.models.employee import RoleEnum


class UserBase(SQLModel):
    email: EmailStr = Field(unique=True)
    nombre: str
    role: RoleEnum
    employee_id: Optional[int] = Field(default=None, foreign_key="employee.id")


class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    password_hash: str


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int


class UserUpdate(SQLModel):
    nombre: Optional[str] = None
    role: Optional[RoleEnum] = None
    employee_id: Optional[int] = None
    password: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    id: int
    email: EmailStr
    nombre: str
    role: RoleEnum
    employee_id: Optional[int] = None


class UserRegister(BaseModel):
    email: EmailStr
    nombre: str
    role: RoleEnum
    password: str
    employee_id: Optional[int] = None


class UserBootstrap(BaseModel):
    email: EmailStr
    nombre: str
    password: str