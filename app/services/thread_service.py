# app/services/thread_service.py

from uuid import UUID
from sqlalchemy.orm import Session
from app.repositories.thread_repository import ThreadRepository
from app.schemas.thread import ThreadCreate, ThreadUpdate, ThreadResponse
from app.schemas.message import MessageCreate  # you'll define this
from app.services.message_service import MessageService  # you'll define this
from app.models.thread import Thread

class ThreadService:
    def __init__(self, thread_repo: ThreadRepository, message_service: MessageService):
        self.thread_repo = thread_repo
        self.message_service = message_service

    def create_thread(self, db: Session, thread_in: ThreadCreate) -> ThreadResponse:
        # Create the thread
        db_thread = self.thread_repo.create_thread(db, thread_in)

        # If initial messages are provided, create them
        if thread_in.messages:
            for msg in thread_in.messages:
                message_create = MessageCreate(**msg)
                self.message_service.create_message(db, db_thread.id, message_create)
        
        return self._to_response(db_thread)

    def get_thread(self, db: Session, thread_id: UUID) -> ThreadResponse:
        db_thread = self.thread_repo.get_thread(db, thread_id)
        return self._to_response(db_thread)

    def update_thread(self, db: Session, thread_id: UUID, data: ThreadUpdate) -> ThreadResponse:
        db_thread = self.thread_repo.update_thread(db, thread_id, data)
        return self._to_response(db_thread)

    def delete_thread(self, db: Session, thread_id: UUID) -> dict:
        deleted = self.thread_repo.delete_thread(db, thread_id)
        return {
            "id": str(thread_id),
            "object": "thread.deleted",
            "deleted": deleted
        }

    def _to_response(self, db_thread: Thread) -> ThreadResponse:
        return ThreadResponse(
            id=str(db_thread.id),
            object=db_thread.object,
            created_at=db_thread.created_at,
            metadata=db_thread.metadata or {},
            tool_resources=db_thread.tool_resources
        )
