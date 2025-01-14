# app/repositories/message_repository.py

from uuid import UUID
from typing import Optional, List
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.message import Message
from app.schemas.message import MessageCreate, MessageUpdate

class MessageRepository:
    def create_message(self, db: Session, thread_id: UUID, message_in: MessageCreate) -> Message:
        # Create DB object
        db_message = Message(
            thread_id=thread_id,
            role=message_in.role,
            content=message_in.content,  # validated in schema
            attachments=message_in.attachments,
            metadata=message_in.metadata or {}
        )
        try:
            db.add(db_message)
            db.commit()
            db.refresh(db_message)
            return db_message
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=str(e))

    def list_messages(
        self,
        db: Session,
        thread_id: UUID,
        limit: int = 20,
        order: str = "desc",
        after: Optional[str] = None,
        before: Optional[str] = None,
        run_id: Optional[str] = None
    ) -> List[Message]:
        query = db.query(Message).filter(Message.thread_id == thread_id)

        if run_id:
            query = query.filter(Message.run_id == UUID(run_id))

        if after:
            query = query.filter(Message.id > UUID(after))
        if before:
            query = query.filter(Message.id < UUID(before))

        if order == "desc":
            query = query.order_by(Message.created_at.desc())
        else:
            query = query.order_by(Message.created_at.asc())

        return query.limit(limit).all()

    def get_message(self, db: Session, message_id: UUID) -> Message:
        msg = db.query(Message).filter(Message.id == message_id).first()
        if not msg:
            raise HTTPException(status_code=404, detail="Message not found")
        return msg

    def update_message(self, db: Session, message_id: UUID, message_in: MessageUpdate) -> Message:
        db_msg = self.get_message(db, message_id)

        if message_in.metadata is not None:
            db_msg.metadata = message_in.metadata

        try:
            db.commit()
            db.refresh(db_msg)
            return db_msg
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=str(e))

    def delete_message(self, db: Session, message_id: UUID) -> bool:
        db_msg = self.get_message(db, message_id)
        try:
            db.delete(db_msg)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=str(e))
