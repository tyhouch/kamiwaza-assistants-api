from typing import Optional, List, Union, Dict, Any
from pydantic import BaseModel, Field, validator
from datetime import datetime

class ToolFunction(BaseModel):
    """Schema for function tool configuration."""
    name: str
    description: Optional[str] = None
    parameters: Dict[str, Any] = Field(default_factory=dict)

class Tool(BaseModel):
    """Schema for assistant tools."""
    type: str = Field(..., description="Type of tool: code_interpreter, file_search, or function")
    function: Optional[ToolFunction] = None

class AssistantCreate(BaseModel):
    """Schema for creating a new assistant."""
    name: Optional[str] = Field(None, max_length=256)
    description: Optional[str] = Field(None, max_length=512)
    model: str
    instructions: Optional[str] = Field(None, max_length=32768)  # 32K chars max
    tools: List[Tool] = Field(default_factory=list)
    tool_resources: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, str]] = Field(
        None,
        description="Metadata key-value pairs. Keys max length 64 chars, values max length 512 chars"
    )
    temperature: Optional[float] = Field(None, ge=0, le=2)
    top_p: Optional[float] = Field(None, ge=0, le=1)
    response_format: Optional[Union[str, Dict[str, Any]]] = Field(default="auto")

    @validator('metadata')
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

class AssistantUpdate(BaseModel):
    """Schema for updating an existing assistant."""
    name: Optional[str] = Field(None, max_length=256)
    description: Optional[str] = Field(None, max_length=512)
    model: Optional[str] = None
    instructions: Optional[str] = Field(None, max_length=32768)
    tools: Optional[List[Tool]] = None
    tool_resources: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, str]] = Field(
        None,
        description="Metadata key-value pairs. Keys max length 64 chars, values max length 512 chars"
    )
    temperature: Optional[float] = Field(None, ge=0, le=2)
    top_p: Optional[float] = Field(None, ge=0, le=1)
    response_format: Optional[Union[str, Dict[str, Any]]] = None

    @validator('metadata')
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

class AssistantResponse(BaseModel):
    """Schema for assistant responses."""
    id: str
    object: str = "assistant"
    created_at: int
    name: Optional[str] = None
    description: Optional[str] = None
    model: str
    instructions: Optional[str] = None
    tools: List[Tool] = Field(default_factory=list)
    tool_resources: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, str]] = None
    temperature: Optional[float] = None
    top_p: Optional[float] = None
    response_format: Union[str, Dict[str, Any]] = "auto"

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: int(v.timestamp())
        }

class AssistantList(BaseModel):
    """Schema for paginated list of assistants."""
    object: str = "list"
    data: List[AssistantResponse]
    first_id: Optional[str] = None
    last_id: Optional[str] = None
    has_more: bool = False

class AssistantDeleted(BaseModel):
    """Schema for assistant deletion response."""
    id: str
    object: str = "assistant.deleted"
    deleted: bool = True