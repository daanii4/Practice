from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.auth import create_access_token
from app.database import get_db
from app.models import User
import os
import time
import random
import string
from google.oauth2 import id_token
from google.auth.transport import requests
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import Optional
from app.schemas import Token  # Updated import

load_dotenv()
auth_router = APIRouter()
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
FIREBASE_CLIENT_ID = "222309474137-h35hgkeb4ikn5d6a93s0h8u72jboj34n.apps.googleusercontent.com"
ADMIN_EMAIL = "danielemojevbe@gmail.com"

class GoogleCredential(BaseModel):
    credential: str

def generate_random_name(length=8):
    """Generate a random name of fixed length."""
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(length))

@auth_router.post("/callback")
async def google_auth_callback(google_cred: GoogleCredential, db: Session = Depends(get_db)):
    try:
        # Try verifying with Firebase client ID first
        try:
            idinfo = id_token.verify_oauth2_token(
                google_cred.credential, 
                requests.Request(), 
                FIREBASE_CLIENT_ID
            )
        except ValueError:
            # If Firebase verification fails, try with regular Google client ID
            idinfo = id_token.verify_oauth2_token(
                google_cred.credential, 
                requests.Request(), 
                GOOGLE_CLIENT_ID
            )

        # Verify token is not expired
        if idinfo['exp'] < int(time.time()):
            raise ValueError('Token has expired')

        # Extract user information
        email: Optional[str] = idinfo.get('email')
        user_name: Optional[str] = idinfo.get('name')
        google_id: Optional[str] = idinfo.get('sub')

        # Print user information or None if not available
        print(f"Email found: {email if email else 'None'}")
        print(f"User name found: {user_name if user_name else 'None'}")
        print(f"Google ID found: {google_id if google_id else 'None'}")

        # Check if the user already exists
        user = db.query(User).filter(User.email == email).first() if email else None
        if not user:
            # Create a new user if they don't exist
            is_admin = email == ADMIN_EMAIL if email else False
            # Assign a random name if user_name is not provided
            name_to_use = user_name if user_name else generate_random_name()

            user = User(
                email=email,
                name=name_to_use,
                google_id=google_id,
                is_admin=is_admin
            )
            db.add(user)
            db.commit()
            db.refresh(user)

        # Generate a JWT token for the user
        access_token = create_access_token(
            {"sub": user.email, "is_admin": user.is_admin} if user else {}
        )

        return Token(access_token=access_token, token_type="bearer")

    except ValueError as e:
        print(f"Token verification failed: {str(e)}")
        raise HTTPException(
            status_code=422,
            detail=f"Invalid token: {str(e)}"
        )
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )
