from typing import Optional, List, Dict
from uuid import UUID
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.repositories.assistant_repository import AssistantRepository
from app.schemas.assistant import (
    AssistantCreate,
    AssistantUpdate,
    AssistantResponse,
    AssistantList
)

class AssistantService:
    def __init__(self, repository: AssistantRepository):
        self.repository = repository

    def _convert_to_response(self, assistant) -> AssistantResponse:
        """Convert database model to response model."""
        assistant_dict = assistant.to_dict()
        return AssistantResponse(**assistant_dict)

    def create(self, db: Session, assistant_data: AssistantCreate) -> AssistantResponse:
        """Create a new assistant."""
        assistant = self.repository.create_assistant(db, assistant_data)
        return self._convert_to_response(assistant)

    def retrieve(self, db: Session, assistant_id: str) -> AssistantResponse:
        """Retrieve an assistant by ID."""
        try:
            assistant = self.repository.get_assistant(db, UUID(assistant_id))
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid assistant ID format")
        return self._convert_to_response(assistant)

    def list(
        self,
        db: Session,
        limit: int = 20,
        order: str = "desc",
        after: Optional[str] = None,
        before: Optional[str] = None
    ) -> AssistantList:
        """List assistants with pagination."""
        assistants = self.repository.list_assistants(
            db=db,
            limit=limit,
            order=order,
            after=after,
            before=before
        )
        
        # Convert to response models
        assistant_list = [
            self._convert_to_response(assistant)
            for assistant in assistants
        ]
        
        # Get first and last IDs for pagination
        first_id = str(assistants[0].id) if assistants else None
        last_id = str(assistants[-1].id) if assistants else None
        
        return AssistantList(
            object="list",
            data=assistant_list,
            first_id=first_id,
            last_id=last_id,
            has_more=len(assistant_list) == limit
        )

    def update(
        self,
        db: Session,
        assistant_id: str,
        assistant_data: AssistantUpdate
    ) -> AssistantResponse:
        """Update an assistant."""
        try:
            assistant = self.repository.update_assistant(
                db,
                UUID(assistant_id),
                assistant_data
            )
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid assistant ID format")
        return self._convert_to_response(assistant)

    def delete(self, db: Session, assistant_id: str) -> Dict[str, any]:
        """Delete an assistant."""
        try:
            deleted = self.repository.delete_assistant(db, UUID(assistant_id))
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid assistant ID format")
            
        if deleted:
            return {
                "id": assistant_id,
                "object": "assistant.deleted",
                "deleted": True
            }
        return {
            "id": assistant_id,
            "object": "assistant.deleted",
            "deleted": False
        }