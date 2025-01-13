from typing import Optional, List
from uuid import UUID
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.assistant import Assistant
from app.schemas.assistant import AssistantCreate, AssistantUpdate

class AssistantRepository:
    def create_assistant(self, db: Session, assistant: AssistantCreate) -> Assistant:
        """Create a new assistant in the database."""
        db_assistant = Assistant(
            name=assistant.name,
            description=assistant.description,
            model=assistant.model,
            instructions=assistant.instructions,
            tools=assistant.tools,
            tool_resources=assistant.tool_resources,
            metadata=assistant.metadata,
            temperature=assistant.temperature,
            top_p=assistant.top_p,
            response_format=assistant.response_format
        )
        
        try:
            db.add(db_assistant)
            db.commit()
            db.refresh(db_assistant)
            return db_assistant
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=str(e))

    def get_assistant(self, db: Session, assistant_id: UUID) -> Optional[Assistant]:
        """Retrieve an assistant by ID."""
        assistant = db.query(Assistant).filter(Assistant.id == assistant_id).first()
        if not assistant:
            raise HTTPException(status_code=404, detail="Assistant not found")
        return assistant

    def list_assistants(
        self, 
        db: Session, 
        limit: int = 20, 
        order: str = "desc", 
        after: Optional[str] = None, 
        before: Optional[str] = None
    ) -> List[Assistant]:
        """List assistants with pagination."""
        query = db.query(Assistant)
        
        # Handle pagination
        if after:
            query = query.filter(Assistant.id > UUID(after))
        if before:
            query = query.filter(Assistant.id < UUID(before))
            
        # Handle ordering
        if order == "desc":
            query = query.order_by(Assistant.created_at.desc())
        else:
            query = query.order_by(Assistant.created_at.asc())
            
        return query.limit(limit).all()

    def update_assistant(
        self, 
        db: Session, 
        assistant_id: UUID, 
        assistant_update: AssistantUpdate
    ) -> Assistant:
        """Update an existing assistant."""
        db_assistant = self.get_assistant(db, assistant_id)
        
        update_data = assistant_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_assistant, field, value)
            
        try:
            db.commit()
            db.refresh(db_assistant)
            return db_assistant
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=str(e))

    def delete_assistant(self, db: Session, assistant_id: UUID) -> bool:
        """Delete an assistant."""
        db_assistant = self.get_assistant(db, assistant_id)
        
        try:
            db.delete(db_assistant)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=str(e))

    def delete_all_assistants(self, db: Session) -> bool:
        """Delete all assistants (mainly for testing purposes)."""
        try:
            db.query(Assistant).delete()
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=str(e))