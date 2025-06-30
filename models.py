from enum import Enum
from sqlmodel import Field, SQLModel
from datetime import datetime, timezone
from pydantic import BaseModel, field_validator, ConfigDict

# Create status enum: pending, in_progress, completed, cancelled
class TaskStatus(Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"
    cancelled = "cancelled"

# Create priority enum: low, medium, high, urgent
class TaskPriority(Enum):
    low = "low"
    medium = "medium"
    high = "high"
    urgent = "urgent"

# Create table with SQLModel
# Optional fields: description, updated_at, due_date, assigned_to
class Task(SQLModel, table = True):
    id: int | None = Field(default = None, primary_key = True)
    title: str = Field(max_length = 200)
    description: str | None = Field(default = None, max_length = 1000)
    status: TaskStatus = Field(default = TaskStatus.pending)
    priority: TaskPriority = Field(default = TaskPriority.medium)
    created_at: datetime = Field(default_factory = lambda: datetime.now(timezone.utc))
    updated_at: datetime | None = None
    due_date: datetime | None = None
    assigned_to: str | None = Field(default = None, max_length = 100)

# Create Pydantic Models

# Creation Model
class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    status: TaskStatus | None = TaskStatus.pending
    priority: TaskPriority | None = TaskPriority.medium
    updated_at: datetime | None = None
    due_date: datetime | None = None
    assigned_to: str | None = None

    @field_validator("title")
    def validate_title(cls, value: str | None) -> str | None:
        if not value.strip():
            raise ValueError("Title cannot be empty or whitespace only")
        return value

    @field_validator("due_date")
    def validate_due_date(cls, value: datetime | None) -> datetime | None:
        if value and value <= datetime.now(timezone.utc):
            raise ValueError("Due date must be in the future")
        return value

# Update Model 
class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: TaskStatus | None = None
    priority: TaskPriority | None = None
    due_date: datetime | None = None
    assigned_to: str | None = None

    @field_validator("title")
    def validate_title(cls, value: str | None) -> str | None:
        if not value.strip():
            raise ValueError("Title cannot be empty or whitespace only")
        return value

    @field_validator("due_date")
    def validate_due_date(cls, value: datetime | None) -> datetime | None:
        if value and value <= datetime.now(timezone.utc):
            raise ValueError("Due date must be in the future")
        return value

# Response Model
class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None
    status: TaskStatus
    priority: TaskPriority
    created_at: datetime
    updated_at: datetime | None
    due_date: datetime | None
    assigned_to: str | None

    model_config = ConfigDict(from_attributes=True)