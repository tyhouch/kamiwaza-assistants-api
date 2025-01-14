# app/services/run_service.py

from uuid import UUID
from sqlalchemy.orm import Session
from fastapi import HTTPException
import time

from app.repositories.run_repository import RunRepository
from app.schemas.run import RunCreate, RunResponse, RunListResponse
from app.models.run import Run, RunStatus
from app.services.message_service import MessageService
from app.schemas.message import MessageCreate

class RunService:
    def __init__(self, run_repo: RunRepository, message_service: MessageService):
        self.run_repo = run_repo
        self.message_service = message_service

    def _to_response(self, run: Run) -> RunResponse:
        return RunResponse(**run.to_dict())

    def create_run(self, db: Session, thread_id: UUID, run_in: RunCreate) -> RunResponse:
        # 1) create run in "queued" or "in_progress" status
        db_run = self.run_repo.create_run(db, thread_id, run_in)
        db_run = self.run_repo.update_run_status(db, db_run.id, RunStatus.in_progress)

        # 2) For Phase 1: placeholder logic -> Insert a dummy "assistant" message
        msg_create = MessageCreate(
            role="assistant",
            content="This is a placeholder response from the run.",
        )
        self.message_service.create_message(db, thread_id, msg_create)

        # 3) Mark run as completed
        db_run = self.run_repo.update_run_status(db, db_run.id, RunStatus.completed)
        return self._to_response(db_run)

    def list_runs(self, db: Session, thread_id: UUID, limit=20, order="desc", after=None, before=None) -> RunListResponse:
        runs = self.run_repo.list_runs(db, thread_id, limit=limit, order=order, after=after, before=before)
        if not runs:
            return RunListResponse(data=[])

        data_res = [self._to_response(r) for r in runs]
        first_id = str(runs[0].id)
        last_id = str(runs[-1].id)
        has_more = (len(runs) == limit)
        return RunListResponse(
            data=data_res,
            first_id=first_id,
            last_id=last_id,
            has_more=has_more
        )

    def get_run(self, db: Session, thread_id: UUID, run_id: UUID) -> RunResponse:
        db_run = self.run_repo.get_run(db, run_id)
        if str(db_run.thread_id) != str(thread_id):
            raise HTTPException(status_code=404, detail="Run not found in this thread")
        return self._to_response(db_run)

    def update_run_metadata(self, db: Session, thread_id: UUID, run_id: UUID, metadata: dict) -> RunResponse:
        db_run = self.run_repo.get_run(db, run_id)
        if str(db_run.thread_id) != str(thread_id):
            raise HTTPException(status_code=404, detail="Run not found in this thread")

        db_run = self.run_repo.update_run_metadata(db, run_id, metadata)
        return self._to_response(db_run)
