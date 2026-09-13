from pydantic import BaseModel, Field
from datetime import datetime


class FeedbackCreate(BaseModel):
    teacher_id: int
    rating: int = Field(ge=1, le=5)
    comment: str


class FeedbackOut(BaseModel):
    id: int
    project_id: int
    teacher_id: int
    rating: int
    comment: str
    created_at: datetime

    class Config:
        from_attributes = True