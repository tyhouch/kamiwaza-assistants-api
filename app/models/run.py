# app/models/run.py

import uuid
from datetime import datetime
from sqlalchemy import (
    Column, String, Integer, JSON, Enum, ForeignKey
)
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base
import enum

class RunStatus(str, enum.Enum):
    queued = "queued"
    in_progress = "in_progress"
    requires_action = "requires_action"
    cancelling = "cancelling"
    cancelled = "cancelled"
    failed = "failed"
    completed = "completed"
    incomplete = "incomplete"
    expired = "expired"

class Run(Base):
    __tablename__ = "runs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    object = Column(String, default="thread.run")
    created_at = Column(Integer, default=lambda: int(datetime.utcnow().timestamp()))

    # references
    thread_id = Column(UUID(as_uuid=True), ForeignKey("threads.id"), nullable=False)
    assistant_id = Column(UUID(as_uuid=True), ForeignKey("assistants.id"), nullable=False)

    # track run status
    status = Column(Enum(RunStatus), default=RunStatus.queued)
    
    # optional for future expansions
    model = Column(String, nullable=True)      # override model
    instructions = Column(String, nullable=True)    # override instructions
    # you can store additional_instructions in a separate column, or in metadata
    # usage tokens or placeholders
    meta_data = Column(JSON, default={})

    # Timestamps for lifecycle
    started_at = Column(Integer, nullable=True)
    completed_at = Column(Integer, nullable=True)
    cancelled_at = Column(Integer, nullable=True)
    failed_at = Column(Integer, nullable=True)
    expires_at = Column(Integer, nullable=True)

    def to_dict(self):
        return {
            "id": str(self.id),
            "object": self.object,
            "created_at": self.created_at,
            "assistant_id": str(self.assistant_id),
            "thread_id": str(self.thread_id),
            "status": self.status.value,
            "started_at": self.started_at,
            "expires_at": self.expires_at,
            "cancelled_at": self.cancelled_at,
            "failed_at": self.failed_at,
            "completed_at": self.completed_at,
            "model": self.model,
            "instructions": self.instructions,
            # placeholders for incomplete_details, tools, usage, etc.
            "metadata": self.meta_data if self.meta_data else {}
        }
