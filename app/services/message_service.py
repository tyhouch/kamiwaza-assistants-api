# app/services/message_service.py

from uuid import UUID
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.repositories.message_repository import MessageRepository
from app.schemas.message import (
    MessageCreate, MessageUpdate, MessageResponse, MessageListResponse
)
from app.models.message import Message

class MessageService:
    def __init__(self, repository: MessageRepository):
        self.repository = repository

    def _to_response(self, msg: Message) -> MessageResponse:
        return MessageResponse(**msg.to_dict())

    def create_message(
        self, db: Session, thread_id: UUID, message_in: MessageCreate
    ) -> MessageResponse:
        db_msg = self.repository.create_message(db, thread_id, message_in)
        return self._to_response(db_msg)

    def list_messages(
        self,
        db: Session,
        thread_id: UUID,
        limit: int = 20,
        order: str = "desc",
        after: str = None,
        before: str = None,
        run_id: str = None
    ) -> MessageListResponse:
        db_msgs = self.repository.list_messages(
            db,
            thread_id,
            limit=limit,
            order=order,
            after=after,
            before=before,
            run_id=run_id
        )
        if not db_msgs:
            return MessageListResponse(data=[])

        data_res = [self._to_response(m) for m in db_msgs]
        first_id = str(db_msgs[0].id)
        last_id = str(db_msgs[-1].id)
        has_more = (len(db_msgs) == limit)
        return MessageListResponse(
            data=data_res,
            first_id=first_id,
            last_id=last_id,
            has_more=has_more
        )

    def get_message(self, db: Session, thread_id: UUID, message_id: UUID) -> MessageResponse:
        msg = self.repository.get_message(db, message_id)
        # Optional: check if msg.thread_id == thread_id
        if str(msg.thread_id) != str(thread_id):
            raise HTTPException(status_code=404, detail="Message not found in this thread")
        return self._to_response(msg)

    def update_message(
        self, db: Session, thread_id: UUID, message_id: UUID, update_in: MessageUpdate
    ) -> MessageResponse:
        db_msg = self.repository.update_message(db, message_id, update_in)
        # same check as above
        if str(db_msg.thread_id) != str(thread_id):
            raise HTTPException(status_code=404, detail="Message not found in this thread")
        return self._to_response(db_msg)

    def delete_message(
        self, db: Session, thread_id: UUID, message_id: UUID
    ) -> dict:
        # Ensure the message belongs to the thread
        msg = self.repository.get_message(db, message_id)
        if str(msg.thread_id) != str(thread_id):
            raise HTTPException(status_code=404, detail="Message not found in this thread")
        deleted = self.repository.delete_message(db, message_id)
        return {
            "id": str(message_id),
            "object": "thread.message.deleted",
            "deleted": deleted
        }
