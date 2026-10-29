import os

import httpx
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from .database import create_tables, get_db
from .schemas import WorkItemCreate, WorkItemResponse
from .services import create_work_item, get_work_item, list_work_items

load_dotenv()
EMPLOYEE_SERVICE_URL = os.getenv("EMPLOYEE_SERVICE_URL", "http://localhost:8001").rstrip("/")
app = FastAPI(title="Work Item Service", version="1.0.0")


@app.on_event("startup")
def startup() -> None:
    create_tables()


@app.get("/health")
def health():
    return {"status": "ok", "service": "work-item"}


@app.get("/work-items", response_model=list[WorkItemResponse])
def get_work_items(db: Session = Depends(get_db)):
    try:
        return list_work_items(db)
    except RuntimeError as error:
        raise HTTPException(status_code=500, detail=str(error)) from error


@app.get("/work-items/{work_item_id}", response_model=WorkItemResponse)
def get_work_item_by_id(work_item_id: int, db: Session = Depends(get_db)):
    if work_item_id <= 0:
        raise HTTPException(status_code=400, detail="Work item ID must be greater than zero.")
    try:
        item = get_work_item(db, work_item_id)
    except RuntimeError as error:
        raise HTTPException(status_code=500, detail=str(error)) from error
    if item is None:
        raise HTTPException(status_code=404, detail="Work item not found")
    return item
@app.post("/work-items", response_model=WorkItemResponse, status_code=status.HTTP_201_CREATED)
def post_work_item(data: WorkItemCreate, db: Session = Depends(get_db)):
    if data.status != "TODO":
        raise HTTPException(status_code=400, detail="New work items must start with TODO.")

    try:
        response = httpx.get(
            f"{EMPLOYEE_SERVICE_URL}/employees/{data.employee_id}",
            timeout=5.0,
        )
    except httpx.TimeoutException as error:
        raise HTTPException(status_code=503, detail="Employee Service timed out.") from error
    except httpx.RequestError as error:
        raise HTTPException(status_code=503, detail="Employee Service is unavailable.") from error

    if response.status_code == 404:
        raise HTTPException(status_code=404, detail="Employee not found")
    if response.status_code != 200:
        raise HTTPException(
            status_code=503,
            detail=f"Employee Service returned unexpected status {response.status_code}.",
        )

    try:
        employee_data = response.json()
        if not isinstance(employee_data, dict) or employee_data.get("id") != data.employee_id:
            raise ValueError("Unexpected employee response.")
    except (ValueError, TypeError) as error:
        raise HTTPException(status_code=503, detail="Employee Service returned an invalid response.") from error

    try:
        return create_work_item(db, data)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    except RuntimeError as error:
        raise HTTPException(status_code=500, detail=str(error)) from error
