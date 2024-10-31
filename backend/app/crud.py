from sqlalchemy.orm import Session
from app.models import User, Project, MediaAsset
from app.schemas import UserCreate, ProjectCreate, ProjectUpdate, MediaAssetCreate

# ---------- USER CRUD OPERATIONS ----------

def create_user(db: Session, user: UserCreate):
    db_user = User(email=user.email, hashed_password=user.password)  # Store hashed password
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def update_user(db: Session, user_id: int, user_data: UserCreate):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.email = user_data.email
        user.hashed_password = user_data.password  # Update the hashed password
        db.commit()
        db.refresh(user)
    return user

def delete_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
    return user

# ---------- PROJECT CRUD OPERATIONS ----------

def create_project(db: Session, project: ProjectCreate, user_id: int):
    db_project = Project(project_name=project.name, user_id=user_id)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

def get_project(db: Session, project_id: int):
    return db.query(Project).filter(Project.id == project_id).first()

def get_projects(db: Session, user_id: int):
    return db.query(Project).filter(Project.user_id == user_id).all()

def update_project(db: Session, project_id: int, project_data: ProjectUpdate):
    project = db.query(Project).filter(Project.id == project_id).first()
    if project:
        if project_data.name:
            project.project_name = project_data.name
        if project_data.status:
            project.status = project_data.status
        db.commit()
        db.refresh(project)
    return project

def delete_project(db: Session, project_id: int):
    project = db.query(Project).filter(Project.id == project_id).first()
    if project:
        db.delete(project)
        db.commit()
    return project

# ---------- MEDIA ASSET CRUD OPERATIONS ----------

def create_media_asset(db: Session, media_asset: MediaAssetCreate, project_id: int):
    db_media_asset = MediaAsset(url=media_asset.url, type=media_asset.type, project_id=project_id)
    db.add(db_media_asset)
    db.commit()
    db.refresh(db_media_asset)
    return db_media_asset

def get_media_asset(db: Session, media_asset_id: int):
    return db.query(MediaAsset).filter(MediaAsset.id == media_asset_id).first()

def get_media_assets_by_project(db: Session, project_id: int):
    return db.query(MediaAsset).filter(MediaAsset.project_id == project_id).all()

def update_media_asset(db: Session, media_asset_id: int, media_asset_data: MediaAssetCreate):
    media_asset = db.query(MediaAsset).filter(MediaAsset.id == media_asset_id).first()
    if media_asset:
        media_asset.url = media_asset_data.url
        media_asset.type = media_asset_data.type
        db.commit()
        db.refresh(media_asset)
    return media_asset

def delete_media_asset(db: Session, media_asset_id: int):
    media_asset = db.query(MediaAsset).filter(MediaAsset.id == media_asset_id).first()
    if media_asset:
        db.delete(media_asset)
        db.commit()
    return media_asset
