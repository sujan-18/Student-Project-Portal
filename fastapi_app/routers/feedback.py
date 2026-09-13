from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas.feedback import FeedbackCreate, FeedbackOut
from dependencies import get_current_user
from models import User
import crud.feedback as feedback_crud
import crud.project as project_crud

router = APIRouter(prefix="/projects", tags=["Feedback"])


@router.post("/{project_id}/feedback", response_model=FeedbackOut)
def add_feedback(
    project_id: int,
    feedback: FeedbackCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    project = project_crud.get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if current_user.role != "teacher":
        raise HTTPException(status_code=403, detail="Only teachers can give feedback")
    if feedback.teacher_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can only submit feedback as yourself")
    return feedback_crud.create_feedback(db, project_id, feedback)


@router.get("/{project_id}/feedback", response_model=list[FeedbackOut])
def list_feedback(project_id: int, db: Session = Depends(get_db)):
    project = project_crud.get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return feedback_crud.get_feedback_for_project(db, project_id)