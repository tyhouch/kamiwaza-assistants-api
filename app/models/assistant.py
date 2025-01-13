import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, Float, DateTime, JSON, Integer
from sqlalchemy.dialects.postgresql import UUID
from ..database import Base

class Assistant(Base):
    __tablename__ = "assistants"

    # Core fields (exact match to OpenAI)
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    object = Column(String, default="assistant")
    created_at = Column(Integer, default=lambda: int(datetime.utcnow().timestamp()))
    name = Column(String(256), nullable=True)
    description = Column(String(512), nullable=True)
    model = Column(String, nullable=False)
    instructions = Column(Text, nullable=True)  # max 256,000 chars
    tools = Column(JSON, default=[])
    tool_resources = Column(JSON, nullable=True)
    meta_data = Column(JSON, default={})  # renamed from metadata due to reserved word in postgres
    temperature = Column(Float, nullable=True)
    top_p = Column(Float, nullable=True)
    response_format = Column(JSON, nullable=True)

    def to_dict(self):
        """Convert to OpenAI format (renames meta_data back to metadata)"""
        return {
            "id": str(self.id),
            "object": self.object,
            "created_at": self.created_at,
            "name": self.name,
            "description": self.description,
            "model": self.model,
            "instructions": self.instructions,
            "tools": self.tools,
            "tool_resources": self.tool_resources,
            "metadata": self.meta_data if self.meta_data is not None else {},  # ensure it's always a dict
            "temperature": self.temperature,
            "top_p": self.top_p,
            "response_format": self.response_format
        }