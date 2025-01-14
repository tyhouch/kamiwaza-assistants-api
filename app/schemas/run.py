# app/schemas/run.py
from typing import Optional, Dict, Any, List, Union
from pydantic import BaseModel, Field, validator
from uuid import UUID

class RunCreate(BaseModel):
    """Schema for creating a run (call the model with an assistant)."""
    assistant_id: str
    model: Optional[str] = None
    instructions: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

    # placeholders for future expansions
    # e.g. additional_instructions, additional_messages, tools, etc.

    @validator("assistant_id")
    def validate_assistant_id(cls, v):
        if not v:
            raise ValueError("assistant_id is required")
        return v

    @validator("metadata")
    def validate_metadata(cls, v):
        if v is not None:
            if len(v) > 16:
                raise ValueError("Maximum of 16 metadata key-value pairs allowed")
            for key, value in v.items():
                if len(key) > 64:
                    raise ValueError("Metadata keys must be <= 64 characters")
                if len(str(value)) > 512:
                    raise ValueError("Metadata values must be <= 512 characters")
        return v

class RunResponse(BaseModel):
    """Schema for returning a run object."""
    id: str
    object: str = "thread.run"
    created_at: int
    assistant_id: str
    thread_id: str
    status: str
    started_at: Optional[int] = None
    completed_at: Optional[int] = None
    cancelled_at: Optional[int] = None
    failed_at: Optional[int] = None
    expires_at: Optional[int] = None

    model: Optional[str] = None
    instructions: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

class RunListResponse(BaseModel):
    """Schema for listing runs in a thread."""
    object: str = "list"
    data: List[RunResponse]
    first_id: Optional[str] = None
    last_id: Optional[str] = None
    has_more: bool = False
