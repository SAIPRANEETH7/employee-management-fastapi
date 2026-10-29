from datetime import date, datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, field_validator


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


class WorkItemResponse(BaseModel):
    id: int
    title: str
    description: str | None
    employee_id: int
    status: WorkItemStatus
    priority: WorkItemPriority
    due_date: date | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
