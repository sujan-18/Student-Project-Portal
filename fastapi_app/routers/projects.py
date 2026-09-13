from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas.project import ProjectCreate, ProjectUpdate, ProjectOut
from dependencies import get_current_user
from models import User
import crud.project as project_crud

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.post("/", response_model=ProjectOut)
def add_project(
    project: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "student":
        raise HTTPException(status_code=403, detail="Only students can create projects")
    if project.student_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can only create projects for yourself")
    return project_crud.create_project(db, project)


@router.get("/", response_model=list[ProjectOut])
def list_projects(student_id: int = None, db: Session = Depends(get_db)):
    return project_crud.get_projects(db, student_id)


@router.get("/{project_id}", response_model=ProjectOut)
def get_project_detail(project_id: int, db: Session = Depends(get_db)):
    project = project_crud.get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.put("/{project_id}", response_model=ProjectOut)
def edit_project(
    project_id: int,
    project: ProjectUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    updated, error = project_crud.update_project(db, project_id, project, current_user)
    if error == "not_found":
        raise HTTPException(status_code=404, detail="Project not found")
    if error == "forbidden":
        raise HTTPException(status_code=403, detail="You don't own this project")
    return updated


@router.delete("/{project_id}")
def remove_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    deleted, error = project_crud.delete_project(db, project_id, current_user)
    if error == "not_found":
        raise HTTPException(status_code=404, detail="Project not found")
    if error == "forbidden":
        raise HTTPException(status_code=403, detail="You don't own this project")
    return {"message": f"Project {project_id} deleted successfully"}