# app/repositories/run_repository.py
from uuid import UUID
from typing import Optional, List
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.run import Run, RunStatus
from app.schemas.run import RunCreate

class RunRepository:
    def create_run(self, db: Session, thread_id: UUID, run_in: RunCreate) -> Run:
        db_run = Run(
            thread_id=thread_id,
            assistant_id=UUID(run_in.assistant_id),
            model=run_in.model,
            instructions=run_in.instructions,
            metadata=run_in.metadata or {}
        )
        try:
            db.add(db_run)
            db.commit()
            db.refresh(db_run)
            return db_run
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=str(e))

    def get_run(self, db: Session, run_id: UUID) -> Run:
        run = db.query(Run).filter(Run.id == run_id).first()
        if not run:
            raise HTTPException(status_code=404, detail="Run not found")
        return run

    def list_runs(
        self,
        db: Session,
        thread_id: UUID,
        limit: int = 20,
        order: str = "desc",
        after: Optional[str] = None,
        before: Optional[str] = None
    ) -> List[Run]:
        query = db.query(Run).filter(Run.thread_id == thread_id)

        if after:
            query = query.filter(Run.id > UUID(after))
        if before:
            query = query.filter(Run.id < UUID(before))

        if order == "desc":
            query = query.order_by(Run.created_at.desc())
        else:
            query = query.order_by(Run.created_at.asc())

        return query.limit(limit).all()

    def update_run_metadata(self, db: Session, run_id: UUID, metadata: dict) -> Run:
        db_run = self.get_run(db, run_id)
        merged = db_run.metadata or {}
        merged.update(metadata)
        db_run.metadata = merged

        try:
            db.commit()
            db.refresh(db_run)
            return db_run
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=str(e))

    def update_run_status(self, db: Session, run_id: UUID, status: RunStatus) -> Run:
        db_run = self.get_run(db, run_id)
        db_run.status = status
        if status == RunStatus.in_progress:
            db_run.started_at = db_run.started_at or int(__import__("time").time())
        elif status == RunStatus.completed:
            db_run.completed_at = int(__import__("time").time())
        elif status == RunStatus.cancelling:
            # you can set db_run.cancelled_at or just a different status flow
            pass

        try:
            db.commit()
            db.refresh(db_run)
            return db_run
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=str(e))
