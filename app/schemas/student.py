
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class NewStudent(BaseModel):
    roll_no: str = Field(min_length=1, max_length=30)
    name: str = Field(min_length=2, max_length=100)
    passing_out_year: int = Field(ge=2020, le=2100)
    email: EmailStr
    phone: str | None = None
    branch: str = Field(min_length=2, max_length=50)
    cgpa: float = Field(ge=0, le=10)


class Student(NewStudent):
    id: int
    created_at: datetime

