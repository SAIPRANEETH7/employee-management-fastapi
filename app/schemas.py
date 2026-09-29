from datetime import date, datetime
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
    
class EmployeeListResponse(BaseModel):
    total: int
    limit: int
    offset: int
    items: list[Employee]


class WorkItemStatus(str, Enum):
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"


class WorkItemPriority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class WorkItemCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str | None = None
    employee_id: int = Field(gt=0)
    status: WorkItemStatus = WorkItemStatus.TODO
    priority: WorkItemPriority = WorkItemPriority.MEDIUM
    due_date: date | None = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Title cannot be empty or whitespace only.")
        return value


class WorkItemUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = None
    employee_id: int | None = Field(default=None, gt=0)
    status: WorkItemStatus | None = None
    priority: WorkItemPriority | None = None
    due_date: date | None = None

    @field_validator("title", "employee_id", "status", "priority", mode="before")
    @classmethod
    def validate_non_nullable_fields(cls, value):
        if value is None:
            raise ValueError("This field cannot be null when provided.")
        return value

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str | None) -> str | None:
        value = value.strip()
        if not value:
            raise ValueError("Title cannot be empty or whitespace only.")
        return value


class AssignedEmployee(BaseModel):
    id: int
    name: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class WorkItemResponse(BaseModel):
    id: int
    title: str
    description: str | None
    employee_id: int
    status: WorkItemStatus
    priority: WorkItemPriority
    due_date: date | None
    created_at: datetime
    assigned_employee: AssignedEmployee

    model_config = ConfigDict(from_attributes=True)


class WorkItemListResponse(BaseModel):
    total: int
    limit: int
    offset: int
    items: list[WorkItemResponse]
