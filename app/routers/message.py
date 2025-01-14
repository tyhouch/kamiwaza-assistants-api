# app/routers/message.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID
from typing import Optional

from app.database import get_db
from app.repositories.message_repository import MessageRepository
from app.services.message_service import MessageService
from app.schemas.message import (
    MessageCreate, MessageUpdate, MessageResponse, MessageListResponse
)

router = APIRouter(
    prefix="/v1/threads/{thread_id}/messages",
    tags=["Messages"]
)

def get_message_service():
    return MessageService(MessageRepository())

@router.post("", response_model=MessageResponse)
def create_message(
    thread_id: str,
    message_in: MessageCreate,
    db: Session = Depends(get_db),
    service: MessageService = Depends(get_message_service)
):
    """Create a new message in a thread."""
    return service.create_message(db, UUID(thread_id), message_in)

@router.get("", response_model=MessageListResponse)
def list_messages(
    thread_id: str,
    limit: int = 20,
    order: str = "desc",
    after: Optional[str] = None,
    before: Optional[str] = None,
    run_id: Optional[str] = None,
    db: Session = Depends(get_db),
    service: MessageService = Depends(get_message_service)
):
    """List messages in a thread."""
    return service.list_messages(
        db,
        UUID(thread_id),
        limit=limit,
        order=order,
        after=after,
        before=before,
        run_id=run_id
    )

@router.get("/{message_id}", response_model=MessageResponse)
def get_message(
    thread_id: str,
    message_id: str,
    db: Session = Depends(get_db),
    service: MessageService = Depends(get_message_service)
):
    """Retrieve a specific message in a thread."""
    return service.get_message(db, UUID(thread_id), UUID(message_id))

@router.post("/{message_id}", response_model=MessageResponse)
def update_message(
    thread_id: str,
    message_id: str,
    update_in: MessageUpdate,
    db: Session = Depends(get_db),
    service: MessageService = Depends(get_message_service)
):
    """Update a message (metadata or content)."""
    return service.update_message(db, UUID(thread_id), UUID(message_id), update_in)

@router.delete("/{message_id}")
def delete_message(
    thread_id: str,
    message_id: str,
    db: Session = Depends(get_db),
    service: MessageService = Depends(get_message_service)
):
    """Delete a message from a thread."""
    return service.delete_message(db, UUID(thread_id), UUID(message_id))
