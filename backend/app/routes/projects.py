from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Project, User
from app.schemas import ProjectCreate, ProjectUpdate, ProjectDetail
from app.auth import get_current_user

projects_router = APIRouter()

# Create a new project
@projects_router.post("/create/", response_model=ProjectDetail)
async def create_project(project_data: ProjectCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_project = Project(
        project_name=project_data.project_name,
        status=project_data.status,
        user_id=current_user.id  # Link project to the authenticated user
    )
    db.add(new_project)
    db.commit()
    db.refresh(new_project)  # Refresh the object to get the generated ID
    return new_project

# Update an existing project
@projects_router.put("/update/{project_id}", response_model=ProjectDetail)
async def update_project(
    project_id: int, 
    project_data: ProjectUpdate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    project = db.query(Project).filter(Project.id == project_id, Project.user_id == current_user.id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    project.name = project_data.name or project.name
    project.status = project_data.status or project.status
    db.commit()

    return project

# Retrieve project details
@projects_router.get("/{project_id}", response_model=ProjectDetail)
async def get_project(project_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    project = db.query(Project).filter(Project.id == project_id, Project.user_id == current_user.id).first()
    if not project:
        return []
    return project
