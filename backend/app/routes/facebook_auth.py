# Backend/app/routes/facebook_auth.py
from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from ..utils.facebook_oauth import get_facebook_auth_url, get_facebook_access_token
from sqlalchemy.orm import Session
from ..database import get_db

facebook_auth_router = APIRouter()

# Redirect to Facebook OAuth login
@facebook_auth_router.get("/auth/facebook/login")
async def facebook_login():
    auth_url, _ = get_facebook_auth_url()
    return RedirectResponse(auth_url)

# Facebook OAuth callback
@facebook_auth_router.get("/auth/facebook/callback")
async def facebook_callback(request: Request, db: Session = Depends(get_db)):
    code = request.query_params.get("code")
    if not code:
        return {"error": "Authorization code not provided"}

    token = get_facebook_access_token(code)
    # Save the token in the database or session as needed
    return {"access_token": token}
