from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, EmailStr, field_validator


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

    @field_validator("name", "department", "primary_skill", "location")
    @classmethod
    def validate_required_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("This field cannot be empty or whitespace only.")
        return value

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: EmailStr) -> str:
        return str(value).lower()


class EmployeeResponse(EmployeeCreate):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
