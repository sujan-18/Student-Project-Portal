from sqlalchemy.orm import Session
from models import Project
from schemas.project import ProjectCreate, ProjectUpdate
from datetime import datetime


def create_project(db: Session, project_data: ProjectCreate):
    new_project = Project(
        title=project_data.title,
        description=project_data.description,
        project_link=str(project_data.project_link),
        student_id=project_data.student_id,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project


def get_project(db: Session, project_id: int):
    return db.query(Project).filter(Project.id == project_id).first()


def get_projects(db: Session, student_id: int = None):
    query = db.query(Project)
    if student_id is not None:
        query = query.filter(Project.student_id == student_id)
    return query.all()


def update_project(db: Session, project_id: int, project_data: ProjectUpdate, current_user):
    project = get_project(db, project_id)
    if not project:
        return None, "not_found"
    if project.student_id != current_user.id:
        return None, "forbidden"
    project.title = project_data.title
    project.description = project_data.description
    project.project_link = str(project_data.project_link)
    project.updated_at = datetime.now()
    db.commit()
    db.refresh(project)
    return project, None


def delete_project(db: Session, project_id: int, current_user):
    project = get_project(db, project_id)
    if not project:
        return None, "not_found"
    if project.student_id != current_user.id:
        return None, "forbidden"
    db.delete(project)
    db.commit()
    return project, None