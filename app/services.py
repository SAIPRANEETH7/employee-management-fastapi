from datetime import datetime, timezone

from .schemas import Employee, EmployeeCreate


employees: list[Employee] = []


def get_next_id() -> int:
    if not employees:
        return 1

    return max(employee.id for employee in employees) + 1


def create_employee(employee_data: EmployeeCreate) -> Employee:
    employee = Employee(
        id=get_next_id(),
        created_at=datetime.now(timezone.utc),
        **employee_data.model_dump()
    )

    employees.append(employee)

    return employee

def get_all_employees() -> list[Employee]:
    return employees


def get_employee_by_id(employee_id: int) -> Employee | None:
    for employee in employees:
        if employee.id == employee_id:
            return employee

    return None

def update_employee(
    employee_id: int,
    employee_data: EmployeeCreate
) -> Employee | None:

    employee = get_employee_by_id(employee_id)

    if employee is None:
        return None

    employee.name = employee_data.name
    employee.email = employee_data.email
    employee.department = employee_data.department
    employee.primary_skill = employee_data.primary_skill
    employee.location = employee_data.location
    employee.work_mode = employee_data.work_mode
    employee.is_active = employee_data.is_active

    return employee


def delete_employee(employee_id: int) -> bool:
    employee = get_employee_by_id(employee_id)

    if employee is None:
        return False

    employees.remove(employee)

    return True