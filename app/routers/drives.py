from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.database.connection import get_db
from app.database.models import Application, Company, PlacementDrive, Student, User
from app.dependencies import get_current_user, require_roles
from app.schemas.placement import Drive as DriveSchema, DriveInput


router = APIRouter(prefix="/drives", tags=["Placement Drives"])


def _drive_query():
    return select(PlacementDrive).options(joinedload(PlacementDrive.company))


@router.get("/", response_model=list[DriveSchema])
def list_drives(database: Session = Depends(get_db), user: User = Depends(get_current_user)):
    drives = database.scalars(_drive_query().order_by(PlacementDrive.created_at.desc())).unique().all()
    if user.role != "admin":
        drives = [drive for drive in drives if drive.status == "open" and drive.application_deadline >= date.today()]
    return drives


@router.get("/{drive_id}", response_model=DriveSchema)
def get_drive(
    drive_id: int,
    database: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    drive = database.scalar(_drive_query().where(PlacementDrive.id == drive_id))
    if drive is None:
        raise HTTPException(status_code=404, detail="Placement drive not found")
    if user.role != "admin" and (drive.status != "open" or drive.application_deadline < date.today()):
        raise HTTPException(status_code=404, detail="Placement drive not found")
    return drive


@router.post("/", response_model=DriveSchema, status_code=201)
def create_drive(
    drive_data: DriveInput,
    database: Session = Depends(get_db),
    _: User = Depends(require_roles("admin")),
):
    if database.get(Company, drive_data.company_id) is None:
        raise HTTPException(status_code=404, detail="Company not found")
    drive = PlacementDrive(**drive_data.model_dump())
    database.add(drive)
    database.commit()
    database.refresh(drive)
    return database.scalar(_drive_query().where(PlacementDrive.id == drive.id))


@router.put("/{drive_id}", response_model=DriveSchema)
def update_drive(
    drive_id: int,
    drive_data: DriveInput,
    database: Session = Depends(get_db),
    _: User = Depends(require_roles("admin")),
):
    drive = database.get(PlacementDrive, drive_id)
    if drive is None:
        raise HTTPException(status_code=404, detail="Placement drive not found")
    if database.get(Company, drive_data.company_id) is None:
        raise HTTPException(status_code=404, detail="Company not found")
    for field, value in drive_data.model_dump().items():
        setattr(drive, field, value)
    database.commit()
    return database.scalar(_drive_query().where(PlacementDrive.id == drive_id))


@router.get("/{drive_id}/eligibility", response_model=bool)
def check_eligibility(
    drive_id: int,
    user: User = Depends(require_roles("student")),
    database: Session = Depends(get_db),
):
    drive = database.get(PlacementDrive, drive_id)
    student = database.scalar(select(Student).where(Student.user_id == user.id))
    if drive is None:
        raise HTTPException(status_code=404, detail="Placement drive not found")
    if student is None:
        raise HTTPException(status_code=404, detail="Student profile not found")
    return (
        student.cgpa >= drive.min_cgpa
        and student.passing_out_year == drive.passing_out_year
        and (not drive.eligible_branches or student.branch.casefold() in {branch.casefold() for branch in drive.eligible_branches})
    )


@router.delete("/{drive_id}", status_code=204)
def delete_drive(
    drive_id: int,
    database: Session = Depends(get_db),
    _: User = Depends(require_roles("admin")),
):
    drive = database.get(PlacementDrive, drive_id)
    if drive is None:
        raise HTTPException(status_code=404, detail="Placement drive not found")
    if database.scalar(select(Application.id).where(Application.drive_id == drive_id).limit(1)) is not None:
        raise HTTPException(status_code=409, detail="Cannot delete a drive with applications")
    database.delete(drive)
    database.commit()