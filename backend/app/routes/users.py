from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.schemas import UserProfile, UserUpdate, UserCreate, UserInDB
from app.auth import get_current_user
from typing import List

users_router = APIRouter()

# ---------- Common Routes ----------

# Route to get the current user's profile
@users_router.get("/me/", response_model=UserProfile)
async def get_current_user_profile(current_user: User = Depends(get_current_user)):
    return current_user


# Route to update the current user's profile
@users_router.put("/me/update", response_model=UserProfile)
async def update_current_user_profile(
    user_data: UserUpdate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    # Update first name, last name, and optionally password
    current_user.first_name = user_data.first_name or current_user.first_name
    current_user.last_name = user_data.last_name or current_user.last_name
    if user_data.password:
        current_user.hashed_password = hash_password(user_data.password)  # Ensure password is hashed
    db.commit()
    return current_user


# ---------- Admin Only Routes ----------

# Utility to check if the current user is an admin
def admin_required(current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized")
    return current_user


# Admin Route: List all users (requires admin access)
@users_router.get("/admin/users", response_model=List[UserProfile])
async def list_all_users(db: Session = Depends(get_db), current_user: User = Depends(admin_required)):
    users = db.query(User).all()
    return users


# Admin Route: Create a new user (requires admin access)
@users_router.post("/admin/users/", response_model=UserInDB)
async def create_user(user: UserCreate, db: Session = Depends(get_db), current_user: User = Depends(admin_required)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = User(email=user.email, hashed_password=user.password)  # Hashing should be added
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# Admin Route: Deactivate (or delete) a user
@users_router.delete("/admin/users/{user_id}")
async def deactivate_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(admin_required)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)  # Logic for deleting the user
    db.commit()
    return {"message": "User deactivated successfully"}


# Admin Route: Get the profile of another user (requires admin access)
@users_router.get("/admin/users/{user_id}", response_model=UserProfile)
async def get_user_profile(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(admin_required)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# Admin Route: Update user role (e.g., promote to admin)
@users_router.patch("/admin/users/{user_id}", response_model=UserInDB)
async def update_user_role(user_id: int, user: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(admin_required)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.is_admin = user.is_admin if user.is_admin is not None else db_user.is_admin
    db.commit()
    return db_user

