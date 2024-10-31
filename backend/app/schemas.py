from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional, Dict, Any
from enum import Enum
from datetime import datetime


# ---------- USER SCHEMAS ----------

class UserBase(BaseModel):
    email: EmailStr

    class Config:
        from_attributes = True


# Schema for user registration input
class UserCreate(UserBase):
    email: EmailStr  # Use EmailStr for email validation
    password: str


# Schema for login input
class UserLogin(BaseModel):
    email: EmailStr
    password: str

    class Config:
        from_attributes = True


# Schema for updating user profile
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password: Optional[str] = None
    is_admin: Optional[bool] = None

    class Config:
        from_attributes = True


# Schema for returning user details from the database
class UserInDB(UserBase):
    id: int
    is_admin: bool

    class Config:
        from_attributes = True  # Required to convert ORM objects into Pydantic models


# Schema for returning the access token after successful login
class Token(BaseModel):
    access_token: str
    token_type: str


# Schema for token data (used to decode the token)
class TokenData(BaseModel):
    email: Optional[EmailStr] = None


# Schema for deleting a user
class UserDelete(BaseModel):
    id: int


# Schema for user profile details
class UserProfile(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str

    class Config:
        from_attributes = True


# ---------- PROJECT SCHEMAS ----------

# Enum for project status
class ProjectStatusEnum(str, Enum):
    draft = "draft"
    posted = "posted"
    ARCHIVED = "archived" 



# Schema for creating a project
class ProjectCreate(BaseModel):
    project_name: str
    status: Optional[ProjectStatusEnum] = ProjectStatusEnum.draft  # Default is draft

    class Config:
        from_attributes = True


# Schema for updating a project
class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    status: Optional[ProjectStatusEnum] = None

    class Config:
        from_attributes = True


# Schema for retrieving project details
class ProjectDetail(BaseModel):
    id: int
    name: str
    status: ProjectStatusEnum
    user_id: int  # The ID of the user who created the project
    created_at: str

    class Config:
        from_attributes = True


# ---------- MEDIA ASSET SCHEMAS ----------

# Enum for media asset type
class MediaTypeEnum(str, Enum):
    image = "image"
    video = "video"
    text = "text"


# Schema for creating media assets
class MediaAssetCreate(BaseModel):
    url: str
    type: MediaTypeEnum  # Image, Video, or Text

    class Config:
        from_attributes = True


# Schema for retrieving media assets
class MediaAssetDetail(BaseModel):
    id: int
    url: str
    type: MediaTypeEnum
    project_id: int

    class Config:
        from_attributes = True


# Schema for retrieving media assets list for a project
class ProjectMediaAssets(BaseModel):
    project_id: int
    media_assets: List[MediaAssetDetail]

    class Config:
        from_attributes = True


# ---------- TOKEN & AUTHENTICATION SCHEMAS ----------

# Schema for returning the access token
class Token(BaseModel):
    access_token: str
    token_type: str

# Schema for token data
class TokenData(BaseModel):
    email: Optional[EmailStr] = None


# ---------- OTHER OPTIONAL SCHEMAS ----------

# Schema for ad performance data (optional if you track performance metrics)
class AdPerformance(BaseModel):
    project_id: int
    impressions: int
    clicks: int
    conversions: int
    spend: float
    roas: Optional[float] = None  # Return on Ad Spend, optional

    class Config:
        from_attributes = True


class PromptRequest(BaseModel):
    prompt: str

class VariationDetails(BaseModel):
    variation_id: str
    goal: str
    platform: str
    content_type: str
    tone: str
    target_audience: str
    performance_metrics: Optional[dict] = None
    selected: bool = False

    model_config = {
        "json_schema_extra": {
            "example": {
                "variation_id": "123",
                "goal": "awareness",
                "platform": "Instagram",
                "content_type": "Image",
                "tone": "Professional",
                "target_audience": "Young Adults",
                "selected": False
            }
        }
    }

class PromptResponse(BaseModel):
    prompt_id: str
    timestamp: datetime
    variations: List[VariationDetails]
    user_id: Optional[str] = None

class Variation(BaseModel):
    id: str
    goal: str
    prompt: str
    details: VariationDetails


class OptimizedPromptRequest(BaseModel):
    success: bool
    prompt_id: str
    message: str
    display_data: Dict[str, Any]
