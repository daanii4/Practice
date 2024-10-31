from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime, Float, Boolean, Enum as SqlEnum
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import Optional
from datetime import datetime
from app.database import Base
from enum import Enum as PyEnum
from app.schemas import ProjectStatusEnum  # Import the enum from schemas.py


# Define the ProjectStatus Enum
class ProjectStatus(PyEnum):
    DRAFT = "draft"
    POSTED = "posted"
    ARCHIVED = "archived"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=False)  # Should be 'hashed_password' for security reasons
    is_admin = Column(Boolean, default=False, nullable=False, comment='True if the user is an administrator')
    projects = relationship("Project", back_populates="owner")
    audit_logs = relationship("AuditLog", back_populates="user")

    def __repr__(self):
        return f"<User id={self.id} email={self.email} is_admin={self.is_admin}>"

class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, index=True)
    project_name = Column(String, index=True)
    status = Column(SqlEnum(ProjectStatusEnum), default=ProjectStatusEnum.draft, comment='Status of the project')
    user_id = Column(Integer, ForeignKey("users.id"))
    
    owner = relationship("User", back_populates="projects")
    media_assets = relationship("MediaAsset", back_populates="project")
    ad_copy = Column(Text)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    ctr = Column(Float, default=0.0)  # Click-Through Rate
    cpa = Column(Float, default=0.0)  # Cost Per Acquisition
    roas = Column(Float, default=0.0)  # Return on Ad Spend
    engagement_rate = Column(Float, default=0.0)  # Engagement Rate
    conversions = Column(Integer, default=0)

class MediaAsset(Base):
    __tablename__ = "media_assets"
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String)
    type = Column(String)  # "image" or "video"
    project_id = Column(Integer, ForeignKey("projects.id"))
    project = relationship("Project", back_populates="media_assets")

class DeletedProject(Base):
    __tablename__ = "deleted_projects"
    id = Column(Integer, primary_key=True, index=True)
    project_name = Column(String)
    user_id = Column(Integer)

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # Link to the user who made the change
    action = Column(String)  # Describe the action (e.g., "created", "updated", "deleted")
    table_name = Column(String)  # Name of the table affected
    row_id = Column(Integer)  # ID of the row affected
    timestamp = Column(DateTime, default=datetime.utcnow)  # When the action occurred
    details = Column(String)  # Optional: More details about the action

    user = relationship("User", back_populates="audit_logs")


# Schema for ad generation details
class AdDetailsModel(Base):
    __tablename__ = "ad_details"

    id: Mapped[int] = mapped_column(primary_key=True)
    product_service: Mapped[str] = mapped_column(String)
    target_audience: Mapped[str] = mapped_column(String)
    ad_goal: Mapped[str] = mapped_column(String)
    call_to_action: Mapped[str] = mapped_column(String)
    top_feature_to_highlight: Mapped[str] = mapped_column(String)
    brand_name: Mapped[str] = mapped_column(String)
    platform: Mapped[str] = mapped_column(String)
    content_type: Mapped[str] = mapped_column(String)
    image_dimensions: Mapped[str] = mapped_column(String)
    tone: Mapped[str] = mapped_column(String)
    key_message: Mapped[str] = mapped_column(String)
    tone_of_voice: Mapped[str] = mapped_column(String)
    optimized_prompt: Mapped[Optional[str]] = mapped_column(String, default="")
