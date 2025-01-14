# app/models/thread.py

import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, JSON, Integer
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base

class Thread(Base):
    __tablename__ = "threads"

    # Unique identifier (UUID)
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    object = Column(String, default="thread")
    created_at = Column(Integer, default=lambda: int(datetime.utcnow().timestamp()))
    meta_data = Column(JSON, default={})
    tool_resources = Column(JSON, nullable=True)

    def to_dict(self):
        return {
            "id": str(self.id),
            "object": self.object,
            "created_at": self.created_at,
            "metadata": self.meta_data if self.meta_data is not None else {},
            "tool_resources": self.tool_resources
        }
