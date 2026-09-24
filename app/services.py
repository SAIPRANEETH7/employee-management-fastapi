from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from .models import Employee


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