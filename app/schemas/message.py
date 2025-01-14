# app/schemas/message.py
from typing import Optional, List, Any, Dict, Union
from pydantic import BaseModel, Field, validator
from uuid import UUID

class MessageContentBlock(BaseModel):
    """Represents a single block of content, e.g. text, image, etc."""
    type: str = Field(..., description="The type of content block, e.g. 'text'.")
    text: Optional[Dict[str, Any]] = None
    # If you want images or other block types, define them similarly

class MessageCreate(BaseModel):
    """Schema for creating a new message in a thread."""
    role: str
    content: Union[str, List[MessageContentBlock]] = Field(
        ..., description="Either a string or array of content blocks."
    )
    attachments: Optional[List[Any]] = None
    metadata: Optional[Dict[str, Any]] = None

    @validator("role")
    def validate_role(cls, v):
        if v not in ("user", "assistant"):
            raise ValueError("role must be either 'user' or 'assistant'")
        return v

    @validator("content")
    def validate_content(cls, v):
        # If user passes a string, we can transform it into a single text block
        if isinstance(v, str):
            return [
                {
                    "type": "text",
                    "text": {"value": v, "annotations": []}
                }
            ]
        return v

    @validator("metadata")
    def validate_metadata(cls, v):
        # up to 16 key-value pairs
        if v is not None:
            if len(v) > 16:
                raise ValueError("Maximum of 16 metadata key-value pairs allowed")
            for key, value in v.items():
                if len(key) > 64:
                    raise ValueError("Metadata keys must be <= 64 characters")
                if len(str(value)) > 512:
                    raise ValueError("Metadata values must be <= 512 characters")
        return v


class MessageUpdate(BaseModel):
    """Schema for updating a message (only metadata or content typically)."""
    metadata: Optional[Dict[str, Any]] = None

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

class MessageResponse(BaseModel):
    """Schema for returning a single message."""
    id: str
    object: str = "thread.message"
    created_at: int
    assistant_id: Optional[str] = None
    thread_id: str
    run_id: Optional[str] = None
    role: str
    content: List[Any] = Field(default_factory=list)
    attachments: List[Any] = Field(default_factory=list)
    status: str = "completed"
    incomplete_details: Optional[Dict[str, Any]] = None
    completed_at: Optional[int] = None
    incomplete_at: Optional[int] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

class MessageListResponse(BaseModel):
    """Schema for listing messages in a thread."""
    object: str = "list"
    data: List[MessageResponse]
    first_id: Optional[str] = None
    last_id: Optional[str] = None
    has_more: bool = False
