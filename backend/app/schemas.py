from typing import Optional, List, Any, Dict
from pydantic import BaseModel, Field
from datetime import datetime


# Task Schemas
class TaskCreate(BaseModel):
    """Schema for creating a new task."""
    conversation_id: str
    agent_type: str
    title: str = Field(..., min_length=1, max_length=500)
    description: Optional[str] = None


class TaskUpdate(BaseModel):
    """Schema for updating a task."""
    status: Optional[str] = None
    result: Optional[Dict[str, Any]] = None
    progress: Optional[str] = None


class TaskResponse(BaseModel):
    """Schema for task response."""
    id: str
    conversation_id: str
    agent_type: str
    title: str
    description: Optional[str]
    status: str
    result: Optional[Dict[str, Any]]
    progress: str
    created_at: datetime
    completed_at: Optional[datetime]

    class Config:
        from_attributes = True


# Message Schemas
class MessageCreate(BaseModel):
    """Schema for creating a new message."""
    conversation_id: str
    role: str
    agent_type: Optional[str] = None
    content: str
    metadata: Optional[Dict[str, Any]] = None


class MessageResponse(BaseModel):
    """Schema for message response."""
    id: str
    conversation_id: str
    role: str
    agent_type: Optional[str]
    content: str
    extra_data: Optional[Dict[str, Any]]
    created_at: datetime

    class Config:
        from_attributes = True


# Conversation Schemas
class ConversationCreate(BaseModel):
    """Schema for creating a new conversation."""
    title: str = Field(..., min_length=1, max_length=500)
    user_id: str = Field(default="default_user")


class ConversationResponse(BaseModel):
    """Schema for conversation response."""
    id: str
    user_id: str
    title: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ConversationDetail(ConversationResponse):
    """Schema for detailed conversation with messages and tasks."""
    messages: List[MessageResponse] = []
    tasks: List[TaskResponse] = []


# User Preference Schemas
class PreferenceCreate(BaseModel):
    """Schema for creating a preference."""
    user_id: str = Field(default="default_user")
    key: str = Field(..., min_length=1, max_length=100)
    value: Dict[str, Any]


class PreferenceResponse(BaseModel):
    """Schema for preference response."""
    id: str
    user_id: str
    key: str
    value: Dict[str, Any]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Agent Status Schema
class AgentStatus(BaseModel):
    """Schema for agent status."""
    agent_type: str
    name: str
    description: str
    status: str  # idle, working, completed, error
    current_task: Optional[str] = None
    progress: str = "0%"
    icon: str


# Event Schemas for SSE
class TaskEvent(BaseModel):
    """Schema for task-related events."""
    event_type: str  # task:started, task:progress, task:completed, task:failed
    task_id: str
    agent_type: str
    status: str
    progress: str
    message: Optional[str] = None
    result: Optional[Dict[str, Any]] = None


class AgentEvent(BaseModel):
    """Schema for agent status events."""
    event_type: str  # agent:status
    agent_type: str
    status: str
    current_task: Optional[str] = None
    progress: str
