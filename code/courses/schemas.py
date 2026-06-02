"""Pydantic Schemas untuk App Courses"""

from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


# =============================================================================
# INPUT SCHEMAS
# =============================================================================

class CourseCreateSchema(BaseModel):
    """Schema untuk POST /api/courses (buat course baru)"""
    title:        str
    description:  Optional[str] = ""
    price:        Optional[int] = 0
    level:        Optional[str] = "beginner"   # beginner | intermediate | advanced
    is_published: Optional[bool] = True


class CourseUpdateSchema(BaseModel):
    """Schema untuk PATCH /api/courses/{id} (update sebagian field)"""
    title:        Optional[str]  = None
    description:  Optional[str]  = None
    price:        Optional[int]  = None
    level:        Optional[str]  = None
    is_published: Optional[bool] = None


# =============================================================================
# FILTER / QUERY PARAMS
# =============================================================================

class CourseFilterSchema(BaseModel):
    """Query params untuk GET /api/courses?level=beginner&max_price=100000"""
    level:     Optional[str] = None
    max_price: Optional[int] = None
    min_price: Optional[int] = None
    search:    Optional[str] = None   # cari di title
    page:      int = 1
    page_size: int = 10


# =============================================================================
# OUTPUT SCHEMAS
# =============================================================================

class InstructorOut(BaseModel):
    id:       int
    username: str
    email:    str


class CourseOut(BaseModel):
    """Response untuk satu course"""
    id:           int
    title:        str
    description:  str
    price:        int
    level:        str
    is_published: bool
    instructor:   InstructorOut
    created_at:   datetime

    class Config:
        from_attributes = True


class CourseListOut(BaseModel):
    """Response untuk list course dengan pagination"""
    total:    int
    page:     int
    per_page: int
    results:  List[CourseOut]


class MessageOut(BaseModel):
    message: str
