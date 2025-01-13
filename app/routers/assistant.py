from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.assistant import (
    AssistantCreate,
    AssistantUpdate,
    AssistantResponse,
    AssistantList,
    AssistantDeleted
)
from app.repositories.assistant_repository import AssistantRepository
from app.services.assistant_service import AssistantService

router = APIRouter(
    prefix="/v1/assistants",
    tags=["Assistants"]
)

# Dependency to get the assistant service
def get_assistant_service():
    return AssistantService(AssistantRepository())

@router.post("", response_model=AssistantResponse)
async def create_assistant(
    assistant: AssistantCreate,
    db: Session = Depends(get_db),
    service: AssistantService = Depends(get_assistant_service)
):
    """Create an assistant."""
    return service.create(db, assistant)

@router.get("/{assistant_id}", response_model=AssistantResponse)
async def get_assistant(
    assistant_id: str,
    db: Session = Depends(get_db),
    service: AssistantService = Depends(get_assistant_service)
):
    """Get an assistant by ID."""
    return service.retrieve(db, assistant_id)

@router.get("", response_model=AssistantList)
async def list_assistants(
    limit: int = Query(20, ge=1, le=100),
    order: str = Query("desc", regex="^(asc|desc)$"),
    after: Optional[str] = Query(None),
    before: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    service: AssistantService = Depends(get_assistant_service)
):
    """List assistants with pagination."""
    return service.list(
        db,
        limit=limit,
        order=order,
        after=after,
        before=before
    )

@router.post("/{assistant_id}", response_model=AssistantResponse)
async def update_assistant(
    assistant_id: str,
    assistant: AssistantUpdate,
    db: Session = Depends(get_db),
    service: AssistantService = Depends(get_assistant_service)
):
    """Update an assistant."""
    return service.update(db, assistant_id, assistant)

@router.delete("/{assistant_id}", response_model=AssistantDeleted)
async def delete_assistant(
    assistant_id: str,
    db: Session = Depends(get_db),
    service: AssistantService = Depends(get_assistant_service)
):
    """Delete an assistant."""
    return service.delete(db, assistant_id)