from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.database.models import Application, PlacementDrive, Student, User
from app.dependencies import get_current_user, require_roles
from app.schemas.placement import Application as ApplicationSchema, ApplicationCreate, ApplicationStatusUpdate


router = APIRouter(prefix="/applications", tags=["Applications"])

ALLOWED_TRANSITIONS = {
    "submitted": {"under_review", "rejected"},
    "under_review": {"shortlisted", "rejected"},
    "shortlisted": {"interview", "rejected"},
    "interview": {"selected", "rejected"},
    "selected": {"offered", "rejected"},
    "offered": {"accepted", "declined"},
    "accepted": set(),
    "declined": set(),
    "rejected": set(),
}


def _is_eligible(student: Student, drive: PlacementDrive) -> bool:
    return (
        student.cgpa >= drive.min_cgpa
        and student.passing_out_year == drive.passing_out_year
        and (not drive.eligible_branches or student.branch.casefold() in {branch.casefold() for branch in drive.eligible_branches})
    )


@router.post("/", response_model=ApplicationSchema, status_code=status.HTTP_201_CREATED)
def apply_to_drive(
    application_data: ApplicationCreate,
    user: User = Depends(require_roles("student")),
    database: Session = Depends(get_db),
):
    student = database.scalar(select(Student).where(Student.user_id == user.id))
    drive = database.get(PlacementDrive, application_data.drive_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student profile not found")
    if drive is None:
        raise HTTPException(status_code=404, detail="Placement drive not found")
    if drive.status != "open" or drive.application_deadline < date.today():
        raise HTTPException(status_code=409, detail="Applications are closed for this drive")
    if not _is_eligible(student, drive):
        raise HTTPException(status_code=403, detail="You do not meet this drive's eligibility criteria")
    existing = database.scalar(
        select(Application).where(Application.student_id == student.id, Application.drive_id == drive.id)
    )
    if existing is not None:
        raise HTTPException(status_code=409, detail="You have already applied to this drive")
    application = Application(student_id=student.id, drive_id=drive.id)
    database.add(application)
    try:
        database.commit()
    except IntegrityError as error:
        database.rollback()
        raise HTTPException(status_code=409, detail="You have already applied to this drive") from error
    database.refresh(application)
    return application


@router.get("/", response_model=list[ApplicationSchema])
def list_applications(
    user: User = Depends(get_current_user),
    database: Session = Depends(get_db),
):
    query = select(Application).order_by(Application.applied_at.desc())
    if user.role != "admin":
        student = database.scalar(select(Student).where(Student.user_id == user.id))
        if student is None:
            raise HTTPException(status_code=404, detail="Student profile not found")
        query = query.where(Application.student_id == student.id)
    return database.scalars(query).all()


@router.patch("/{application_id}/status", response_model=ApplicationSchema)
def update_application_status(
    application_id: int,
    update: ApplicationStatusUpdate,
    database: Session = Depends(get_db),
    _: User = Depends(require_roles("admin")),
):
    application = database.get(Application, application_id)
    if application is None:
        raise HTTPException(status_code=404, detail="Application not found")
    if update.status not in ALLOWED_TRANSITIONS[application.status]:
        raise HTTPException(
            status_code=409,
            detail=f"Cannot move an application from {application.status} to {update.status}",
        )
    application.status = update.status
    application.notes = update.notes
    database.commit()
    database.refresh(application)
    return application