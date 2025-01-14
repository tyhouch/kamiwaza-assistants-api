# app/repositories/thread_repository.py

from uuid import UUID
from typing import Optional, List
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.thread import Thread
from app.schemas.thread import ThreadCreate, ThreadUpdate

class ThreadRepository:
    def create_thread(self, db: Session, data: ThreadCreate) -> Thread:
        db_thread = Thread(
            metadata=data.metadata or {},
            tool_resources=data.tool_resources
        )
        try:
            db.add(db_thread)
            db.commit()
            db.refresh(db_thread)
            return db_thread
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=str(e))

    def get_thread(self, db: Session, thread_id: UUID) -> Thread:
        thread = db.query(Thread).filter(Thread.id == thread_id).first()
        if not thread:
            raise HTTPException(status_code=404, detail="Thread not found")
        return thread

    def update_thread(self, db: Session, thread_id: UUID, data: ThreadUpdate) -> Thread:
        db_thread = self.get_thread(db, thread_id)
        if data.metadata is not None:
            db_thread.metadata = data.metadata
        if data.tool_resources is not None:
            db_thread.tool_resources = data.tool_resources

        try:
            db.commit()
            db.refresh(db_thread)
            return db_thread
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=str(e))

    def delete_thread(self, db: Session, thread_id: UUID) -> bool:
        db_thread = self.get_thread(db, thread_id)
        try:
            db.delete(db_thread)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=str(e))

    def list_threads(self, db: Session, limit: int = 20) -> List[Thread]:
        return db.query(Thread).order_by(Thread.created_at.desc()).limit(limit).all()
