from typing import Optional
from sqlmodel import SQLModel, Field


class TaskBase(SQLModel):
    nombre: str
    descripcion: Optional[str] = None
    activo: bool = True


class Task(TaskBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class TaskCreate(TaskBase):
    pass


class TaskRead(TaskBase):
    id: int


class TaskUpdate(SQLModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    activo: Optional[bool] = None