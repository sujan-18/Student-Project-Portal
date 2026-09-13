from pydantic import BaseModel, HttpUrl
from datetime import datetime


class ProjectCreate(BaseModel):
    title: str
    description: str
    project_link: HttpUrl
    student_id: int


class ProjectUpdate(BaseModel):
    title: str
    description: str
    project_link: HttpUrl


class ProjectOut(BaseModel):
    id: int
    title: str
    description: str
    project_link: HttpUrl
    student_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True