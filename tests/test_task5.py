import unittest

from pydantic import ValidationError
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.database import Base
from app.models import Employee, WorkItem
from app.schemas import WorkItemCreate, WorkItemStatus, WorkItemStatusUpdate, WorkItemUpdate
from app.services import (
    create_work_item, delete_work_item, get_employee_work_summary,
    get_work_item_by_id, update_work_item, update_work_item_status,
)


class Task5ServiceTests(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)

        @event.listens_for(self.engine, "connect")
        def enable_foreign_keys(connection, _record):
            connection.execute("PRAGMA foreign_keys=ON")

        Base.metadata.create_all(self.engine)
        self.db = Session(self.engine)
        self.employee_a = Employee(
            name="Employee One", email="one@example.com", department="Engineering",
            primary_skill="Python", location="Remote", work_mode="WFH", is_active=True,
        )
        self.employee_b = Employee(
            name="Employee Two", email="two@example.com", department="Engineering",
            primary_skill="Python", location="Remote", work_mode="WFH", is_active=True,
        )
        self.db.add_all([self.employee_a, self.employee_b])
        self.db.commit()

    def tearDown(self):
        self.db.close()
        Base.metadata.drop_all(self.engine)
        self.engine.dispose()

    def make_item(self, title="Task", employee_id=None, **kwargs):
        data = WorkItemCreate(title=title, employee_id=employee_id or self.employee_a.id, **kwargs)
        return create_work_item(self.db, data)

    def test_creation_validation_and_transitions(self):
        item = self.make_item()
        self.assertEqual(item.status, "TODO")
        for value in ("IN_PROGRESS", "COMPLETED"):
            with self.assertRaises(ValueError):
                self.make_item(title="Invalid initial", status=value)
        with self.assertRaises(ValidationError):
            WorkItemCreate(title="Bad", employee_id=self.employee_a.id, status="BOGUS")
        for body in ({}, {"status": None}, {"status": "INVALID"}):
            with self.assertRaises(ValidationError):
                WorkItemStatusUpdate.model_validate(body)

        changed = update_work_item_status(self.db, item.id, "IN_PROGRESS")
        self.assertEqual(changed.status, "IN_PROGRESS")
        self.assertEqual(update_work_item_status(self.db, item.id, "IN_PROGRESS").status, "IN_PROGRESS")
        with self.assertRaises(ValueError):
            update_work_item_status(self.db, item.id, "TODO")
        self.assertEqual(update_work_item_status(self.db, item.id, "COMPLETED").status, "COMPLETED")
        with self.assertRaises(ValueError):
            update_work_item_status(self.db, item.id, "IN_PROGRESS")

    def test_put_preservation_atomicity_and_summaries(self):
        item = self.make_item(title="Initial")
        self.make_item(title="Second")
        self.assertEqual(get_employee_work_summary(self.db, self.employee_a.id), {
            "employee_id": self.employee_a.id, "total_work_items": 2,
            "todo": 2, "in_progress": 0, "completed": 0,
        })
        update_work_item(self.db, item.id, WorkItemUpdate(title="Updated"))
        self.assertEqual(get_work_item_by_id(self.db, item.id).status, "TODO")
        with self.assertRaises(ValueError):
            update_work_item(self.db, item.id, WorkItemUpdate(title="Must Roll Back", status="COMPLETED"))
        preserved = get_work_item_by_id(self.db, item.id)
        self.assertEqual((preserved.title, preserved.status), ("Updated", "TODO"))
        update_work_item_status(self.db, item.id, "IN_PROGRESS")
        self.assertEqual(get_employee_work_summary(self.db, self.employee_a.id)["in_progress"], 1)
        update_work_item(self.db, item.id, WorkItemUpdate(employee_id=self.employee_b.id))
        self.assertEqual(get_employee_work_summary(self.db, self.employee_a.id)["total_work_items"], 1)
        self.assertEqual(get_employee_work_summary(self.db, self.employee_b.id)["in_progress"], 1)
        delete_work_item(self.db, item.id)
        self.assertEqual(get_employee_work_summary(self.db, self.employee_b.id), {
            "employee_id": self.employee_b.id, "total_work_items": 0,
            "todo": 0, "in_progress": 0, "completed": 0,
        })
        self.assertIsNone(get_employee_work_summary(self.db, 9999))
        self.assertIsNone(get_work_item_by_id(self.db, 9999))


if __name__ == "__main__":
    unittest.main()
# Repository review: 2026-10-14
