from datetime import datetime
from enum import Enum

from pydantic import BaseModel, EmailStr, Field


class WorkMode(str, Enum):
    WFH = "WFH"
    WFO = "WFO"


class EmployeeCreate(BaseModel):
    name: str
    email: EmailStr
    department: str
    primary_skill: str
    location: str
    work_mode: WorkMode
    is_active: bool = True


class Employee(EmployeeCreate):
    id: int = Field(gt=0)
    created_at: datetime