from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


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

    @field_validator(
        "name",
        "department",
        "primary_skill",
        "location"
    )
    @classmethod
    def validate_required_strings(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("This field cannot be empty or whitespace only.")

        return value

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: EmailStr) -> str:
        return str(value).lower()


class Employee(EmployeeCreate):
    id: int = Field(gt=0)
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)