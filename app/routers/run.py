# app/routers/run.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID
from typing import Optional

from app.database import get_db
from app.repositories.run_repository import RunRepository
from app.repositories.message_repository import MessageRepository
from app.services.message_service import MessageService
from app.services.run_service import RunService
from app.schemas.run import RunCreate, RunResponse, RunListResponse

router = APIRouter(
    prefix="/v1/threads/{thread_id}/runs",
    tags=["Runs"]
)

def get_run_service():
    run_repo = RunRepository()
    message_repo = MessageRepository()
    message_service = MessageService(message_repo)
    return RunService(run_repo, message_service)

@router.post("", response_model=RunResponse)
def create_run(
    thread_id: str,
    run_in: RunCreate,
    db: Session = Depends(get_db),
    service: RunService = Depends(get_run_service)
):
    """Create a run and produce an assistant message (Phase 1 placeholder)."""
    return service.create_run(db, UUID(thread_id), run_in)

@router.get("", response_model=RunListResponse)
def list_runs(
    thread_id: str,
    limit: int = 20,
    order: str = "desc",
    after: Optional[str] = None,
    before: Optional[str] = None,
    db: Session = Depends(get_db),
    service: RunService = Depends(get_run_service)
):
    """List runs in a thread."""
    return service.list_runs(db, UUID(thread_id), limit=limit, order=order, after=after, before=before)

@router.get("/{run_id}", response_model=RunResponse)
def get_run(
    thread_id: str,
    run_id: str,
    db: Session = Depends(get_db),
    service: RunService = Depends(get_run_service)
):
    """Retrieve a specific run."""
    return service.get_run(db, UUID(thread_id), UUID(run_id))

@router.post("/{run_id}", response_model=RunResponse)
def update_run(
    thread_id: str,
    run_id: str,
    metadata: dict,
    db: Session = Depends(get_db),
    service: RunService = Depends(get_run_service)
):
    """
    Update run metadata.
    If you want to update status, you'd do that in a separate endpoint or method.
    """
    return service.update_run_metadata(db, UUID(thread_id), UUID(run_id), metadata)
