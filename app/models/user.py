from typing import Literal
from pydantic import BaseModel, EmailStr


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    id: int
    email: EmailStr
    role: Literal["Trabajador", "Encargado", "Administrador"]