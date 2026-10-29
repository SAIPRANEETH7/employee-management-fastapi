from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from .models import WorkItem
from .schemas import WorkItemCreate


def create_work_item(db: Session, data: WorkItemCreate) -> WorkItem:
    if data.status != "TODO":
        raise ValueError("New work items must start with TODO.")
    item = WorkItem(
        title=data.title,
        description=data.description,
        employee_id=data.employee_id,
        status="TODO",
        priority=data.priority.value,
        due_date=data.due_date,
    )
    try:
        db.add(item)
        db.commit()
        db.refresh(item)
        return item
    except SQLAlchemyError as error:
        db.rollback()
        raise RuntimeError("Database operation failed.") from error


def list_work_items(db: Session) -> list[WorkItem]:
    try:
        return list(db.scalars(select(WorkItem).order_by(WorkItem.id.asc())).all())
    except SQLAlchemyError as error:
        db.rollback()
        raise RuntimeError("Database operation failed.") from error


def get_work_item(db: Session, work_item_id: int) -> WorkItem | None:
    try:
        return db.get(WorkItem, work_item_id)
    except SQLAlchemyError as error:
        db.rollback()
        raise RuntimeError("Database operation failed.") from error
