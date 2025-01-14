# app/routers/thread.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID

from app.database import get_db
from app.schemas.thread import ThreadCreate, ThreadUpdate, ThreadResponse
from app.services.thread_service import ThreadService
from app.repositories.thread_repository import ThreadRepository
from app.repositories.message_repository import MessageRepository
from app.services.message_service import MessageService

router = APIRouter(
    prefix="/v1/threads",
    tags=["Threads"]
)

def get_thread_service():
    thread_repo = ThreadRepository()
    message_repo = MessageRepository()
    message_service = MessageService(message_repo)
    return ThreadService(thread_repo, message_service)

@router.post("", response_model=ThreadResponse)
def create_thread(
    thread_in: ThreadCreate,
    db: Session = Depends(get_db),
    service: ThreadService = Depends(get_thread_service)
):
    """Create a new thread."""
    return service.create_thread(db, thread_in)

@router.get("/{thread_id}", response_model=ThreadResponse)
def get_thread(
    thread_id: str,
    db: Session = Depends(get_db),
    service: ThreadService = Depends(get_thread_service)
):
    """Retrieve a thread by ID."""
    return service.get_thread(db, UUID(thread_id))

@router.post("/{thread_id}", response_model=ThreadResponse)
def update_thread(
    thread_id: str,
    data: ThreadUpdate,
    db: Session = Depends(get_db),
    service: ThreadService = Depends(get_thread_service)
):
    """Modify a thread's metadata or tool_resources."""
    return service.update_thread(db, UUID(thread_id), data)

@router.delete("/{thread_id}")
def delete_thread(
    thread_id: str,
    db: Session = Depends(get_db),
    service: ThreadService = Depends(get_thread_service)
):
    """Delete a thread."""
    return service.delete_thread(db, UUID(thread_id))
