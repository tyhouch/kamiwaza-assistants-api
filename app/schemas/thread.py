# app/schemas/thread.py
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field, validator

class ThreadCreate(BaseModel):
    """Schema for creating a thread, optionally with initial messages."""
    messages: Optional[list] = Field(
        default=None,
        description="A list of messages to create with the thread."
    )
    tool_resources: Optional[dict] = None
    metadata: Optional[Dict[str, Any]] = None

    @validator("metadata")
    def validate_metadata(cls, v):
        # Ensure at most 16 key-value pairs, etc.
        if v is not None:
            if len(v) > 16:
                raise ValueError("Maximum of 16 metadata key-value pairs allowed")
            for key, value in v.items():
                if len(key) > 64:
                    raise ValueError("Metadata keys must be <= 64 characters")
                if len(str(value)) > 512:
                    raise ValueError("Metadata values must be <= 512 characters")
        return v

class ThreadUpdate(BaseModel):
    """Schema for updating a thread (metadata or tool_resources)."""
    tool_resources: Optional[dict] = None
    metadata: Optional[Dict[str, Any]] = None

    @validator("metadata")
    def validate_metadata(cls, v):
        # Same logic as above
        if v is not None:
            if len(v) > 16:
                raise ValueError("Maximum of 16 metadata key-value pairs allowed")
            for key, value in v.items():
                if len(key) > 64:
                    raise ValueError("Metadata keys must be <= 64 characters")
                if len(str(value)) > 512:
                    raise ValueError("Metadata values must be <= 512 characters")
        return v



class ThreadResponse(BaseModel):
    """Schema for returning a single thread object."""
    id: str
    object: str = "thread"
    created_at: int
    metadata: Dict[str, Any] = {}
    tool_resources: Optional[dict] = None

    class Config:
        from_attributes = True