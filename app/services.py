from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session, selectinload

from .models import Employee, WorkItem


def create_employee(
    db: Session,
    employee_data
) -> Employee:

    existing_employee = db.scalar(
        select(Employee).where(
            func.lower(Employee.email) == employee_data.email.lower()
        )
    )

    if existing_employee is not None:
        raise ValueError("Email already exists.")

    employee = Employee(
        name=employee_data.name,
        email=employee_data.email,
        department=employee_data.department,
        primary_skill=employee_data.primary_skill,
        location=employee_data.location,
        work_mode=employee_data.work_mode.value,
        is_active=employee_data.is_active,
    )

    try:
        db.add(employee)
        db.commit()
        db.refresh(employee)

    except IntegrityError:
        db.rollback()
        raise ValueError("Email already exists.")

    except SQLAlchemyError:
        db.rollback()
        raise RuntimeError("Database operation failed.")

    return employee


def get_all_employees(
    db: Session,
    search: str | None = None,
    department: str | None = None,
    work_mode: str | None = None,
    is_active: bool | None = None,
    limit: int = 10,
    offset: int = 0,
):
    try:
        query = select(Employee)

        if search:
            query = query.where(
                Employee.name.ilike(f"%{search}%")
            )

        if department:
            query = query.where(
                Employee.department == department
            )

        if work_mode:
            query = query.where(
                Employee.work_mode == work_mode
            )

        if is_active is not None:
            query = query.where(
                Employee.is_active == is_active
            )

        total = db.scalar(
            select(func.count()).select_from(
                query.subquery()
            )
        )

        query = (
            query
            .order_by(Employee.id.asc())
            .offset(offset)
            .limit(limit)
        )

        result = db.scalars(query)

        return total, result.all()

    except SQLAlchemyError:
        db.rollback()
        raise RuntimeError("Database operation failed.")


def get_employee_by_id(
    db: Session,
    employee_id: int
) -> Employee | None:

    try:
        return db.get(Employee, employee_id)

    except SQLAlchemyError:
        db.rollback()
        raise RuntimeError("Database operation failed.")


def update_employee(
    db: Session,
    employee_id: int,
    employee_data
) -> Employee | None:

    try:
        employee = get_employee_by_id(db, employee_id)

        if employee is None:
            return None

        existing_employee = db.scalar(
            select(Employee).where(
                func.lower(Employee.email) == employee_data.email.lower(),
                Employee.id != employee_id
            )
        )

        if existing_employee is not None:
            raise ValueError("Email already exists.")

        employee.name = employee_data.name
        employee.email = employee_data.email
        employee.department = employee_data.department
        employee.primary_skill = employee_data.primary_skill
        employee.location = employee_data.location
        employee.work_mode = employee_data.work_mode.value
        employee.is_active = employee_data.is_active

        db.commit()
        db.refresh(employee)

        return employee

    except ValueError:
        db.rollback()
        raise

    except IntegrityError:
        db.rollback()
        raise ValueError("Email already exists.")

    except SQLAlchemyError:
        db.rollback()
        raise RuntimeError("Database operation failed.")


def delete_employee(
    db: Session,
    employee_id: int
) -> bool:

    try:
        employee = db.get(Employee, employee_id)

        if employee is None:
            return False

        db.delete(employee)
        db.commit()

        return True

    except SQLAlchemyError:
        db.rollback()
        raise RuntimeError("Database operation failed.")


def _ensure_employee(db: Session, employee_id: int) -> None:
    if db.get(Employee, employee_id) is None:
        raise LookupError(f"Employee {employee_id} not found.")


def create_work_item(db: Session, data) -> WorkItem:
    try:
        _ensure_employee(db, data.employee_id)
        item = WorkItem(
            title=data.title,
            description=data.description,
            employee_id=data.employee_id,
            status=data.status.value,
            priority=data.priority.value,
            due_date=data.due_date,
        )
        db.add(item)
        db.commit()
        return get_work_item_by_id(db, item.id)
    except LookupError:
        db.rollback()
        raise
    except SQLAlchemyError:
        db.rollback()
        raise RuntimeError("Database operation failed.")


def get_work_item_by_id(db: Session, work_item_id: int) -> WorkItem | None:
    try:
        return db.scalar(
            select(WorkItem)
            .options(selectinload(WorkItem.assigned_employee))
            .where(WorkItem.id == work_item_id)
        )
    except SQLAlchemyError:
        db.rollback()
        raise RuntimeError("Database operation failed.")


def get_all_work_items(
    db: Session,
    search: str | None = None,
    employee_id: int | None = None,
    status: str | None = None,
    priority: str | None = None,
    limit: int = 10,
    offset: int = 0,
):
    try:
        query = select(WorkItem)
        if search:
            query = query.where(WorkItem.title.ilike(f"%{search}%"))
        if employee_id is not None:
            query = query.where(WorkItem.employee_id == employee_id)
        if status is not None:
            query = query.where(WorkItem.status == status)
        if priority is not None:
            query = query.where(WorkItem.priority == priority)

        total = db.scalar(select(func.count()).select_from(query.subquery())) or 0
        page_query = (
            query.options(selectinload(WorkItem.assigned_employee))
            .order_by(WorkItem.id.asc())
            .offset(offset)
            .limit(limit)
        )
        return total, db.scalars(page_query).all()
    except SQLAlchemyError:
        db.rollback()
        raise RuntimeError("Database operation failed.")


def update_work_item(db: Session, work_item_id: int, data) -> WorkItem | None:
    try:
        item = db.get(WorkItem, work_item_id)
        if item is None:
            return None
        changes = data.model_dump(exclude_unset=True)
        if "employee_id" in changes:
            _ensure_employee(db, changes["employee_id"])
        for key, value in changes.items():
            setattr(item, key, value.value if hasattr(value, "value") else value)
        db.commit()
        return get_work_item_by_id(db, work_item_id)
    except LookupError:
        db.rollback()
        raise
    except SQLAlchemyError:
        db.rollback()
        raise RuntimeError("Database operation failed.")


def delete_work_item(db: Session, work_item_id: int) -> bool:
    try:
        item = db.get(WorkItem, work_item_id)
        if item is None:
            return False
        db.delete(item)
        db.commit()
        return True
    except SQLAlchemyError:
        db.rollback()
        raise RuntimeError("Database operation failed.")
