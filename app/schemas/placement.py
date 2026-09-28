from datetime import date, datetime

from typing import Literal

from pydantic import BaseModel, Field, HttpUrl


class CompanyInput(BaseModel):
    name: str = Field(min_length=2, max_length=150)
    website: HttpUrl | None = None
    description: str | None = None


class Company(CompanyInput):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}


class DriveInput(BaseModel):
    company_id: int
    title: str = Field(min_length=2, max_length=150)
    description: str | None = None
    min_cgpa: float = Field(default=0, ge=0, le=10)
    eligible_branches: list[str] | None = None
    passing_out_year: int = Field(ge=2020, le=2100)
    application_deadline: date
    status: Literal["draft", "open", "closed"] = "draft"


class Drive(DriveInput):
    id: int
    created_at: datetime
    company: Company

    model_config = {"from_attributes": True}


class ApplicationStatusUpdate(BaseModel):
    status: Literal[
        "under_review",
        "shortlisted",
        "interview",
        "selected",
        "offered",
        "accepted",
        "declined",
        "rejected",
    ]
    notes: str | None = None


class ApplicationCreate(BaseModel):
    drive_id: int


class Application(BaseModel):
    id: int
    student_id: int
    drive_id: int
    status: str
    applied_at: datetime
    updated_at: datetime
    notes: str | None = None

    model_config = {"from_attributes": True}