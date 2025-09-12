from datetime import date
from typing import Optional
from enum import Enum
from sqlmodel import SQLModel, Field


class TurnoEnum(str, Enum):
    manana = "mañana"
    tarde = "tarde" 
    noche = "noche"


class ScheduleBase(SQLModel):
    fecha: date
    turno: TurnoEnum
    empleado_id: int = Field(foreign_key="employee.id")
    task_id: Optional[int] = Field(default=None, foreign_key="task.id")


class Schedule(ScheduleBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class ScheduleCreate(ScheduleBase):
    pass


class ScheduleRead(ScheduleBase):
    id: int


class ScheduleUpdate(SQLModel):
    fecha: Optional[date] = None
    turno: Optional[TurnoEnum] = None
    empleado_id: Optional[int] = None
    task_id: Optional[int] = None