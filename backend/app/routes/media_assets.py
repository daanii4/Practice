from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import MediaAsset, Project
from app.auth import get_current_user
from app.schemas import MediaAssetCreate
import shutil
import os

media_asset_router = APIRouter()

# Media asset upload directory (adjust the path as per your project structure)
UPLOAD_DIRECTORY = "./uploads/media_assets"

# Create the directory if it doesn't exist
if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

# Upload media asset and associate it with a project
@media_asset_router.post("/upload/")
async def upload_media_asset(
    project_id: int, 
    file: UploadFile = File(...), 
    db: Session = Depends(get_db), 
    current_user: str = Depends(get_current_user)
):
    # Ensure the project exists
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project or project.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Project not found or unauthorized")

    # Save the file to the upload directory
    file_location = f"{UPLOAD_DIRECTORY}/{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    media_asset_data = MediaAssetCreate(
        url=file_location,
        type=file.content_type.split('/')[0],
        project_id=project.id
    )


    # Save the media asset to the database
    media_asset = MediaAsset(
        url=file_location,
        type=file.content_type.split('/')[0],  # type: "image" or "video"
        project_id=project.id
    )
    db.add(media_asset)
    db.commit()

    return {"message": "Media asset uploaded successfully", "file_url": file_location}
