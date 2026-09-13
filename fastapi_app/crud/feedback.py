from sqlalchemy.orm import Session
from models import Feedback
from schemas.feedback import FeedbackCreate
from datetime import datetime


def create_feedback(db: Session, project_id: int, feedback_data: FeedbackCreate):
    new_feedback = Feedback(
        project_id=project_id,
        teacher_id=feedback_data.teacher_id,
        rating=feedback_data.rating,
        comment=feedback_data.comment,
        created_at=datetime.now(),
    )
    db.add(new_feedback)
    db.commit()
    db.refresh(new_feedback)
    return new_feedback


def get_feedback_for_project(db: Session, project_id: int):
    return db.query(Feedback).filter(Feedback.project_id == project_id).all()