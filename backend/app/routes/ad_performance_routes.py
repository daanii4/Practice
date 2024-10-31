# Backend/app/routes/ad_performance_routes.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.utils.facebook_analytics import fetch_facebook_ad_performance
from app.database import get_db

ad_performance_router = APIRouter()

@ad_performance_router.get("/analytics/{project_id}")
def get_ad_performance(project_id: int, db: Session = Depends(get_db)):
    return fetch_facebook_ad_performance(project_id, db)
