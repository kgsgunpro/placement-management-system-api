from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.database.models import Student, User
from app.dependencies import get_current_user, require_roles
from app.schemas.student import NewStudent, Student as StudentSchema


router = APIRouter(prefix="/students", tags=["Students"])


@router.get("/", response_model=list[StudentSchema])
def get_students(database: Session = Depends(get_db), _: User = Depends(require_roles("admin"))):
    return database.scalars(select(Student).order_by(Student.id)).all()


@router.get("/me", response_model=StudentSchema)
def get_my_student_profile(user: User = Depends(require_roles("student"))):
    if user.student is None:
        raise HTTPException(status_code=404, detail="Student profile not found")
    return user.student


@router.get("/{student_id}", response_model=StudentSchema)
def get_student_by_id(
    student_id: int,
    user: User = Depends(get_current_user),
    database: Session = Depends(get_db),
):
    student = database.get(Student, student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    if user.role != "admin" and student.user_id != user.id:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    return student


@router.post("/", response_model=StudentSchema, status_code=status.HTTP_201_CREATED)
def create_student(
    student_data: NewStudent,
    database: Session = Depends(get_db),
    _: User = Depends(require_roles("admin")),
):
    student = Student(**student_data.model_dump())
    database.add(student)
    try:
        database.commit()
    except IntegrityError:
        database.rollback()
        raise HTTPException(status_code=409, detail="Roll number or email already exists")
    database.refresh(student)
    return student


@router.put("/{student_id}", response_model=StudentSchema)
def update_student(
    student_id: int,
    student_data: NewStudent,
    database: Session = Depends(get_db),
    _: User = Depends(require_roles("admin")),
):
    student = database.get(Student, student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    for field, value in student_data.model_dump().items():
        setattr(student, field, value)
    try:
        database.commit()
    except IntegrityError:
        database.rollback()
        raise HTTPException(status_code=409, detail="Roll number or email already exists")
    database.refresh(student)
    return student


@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(
    student_id: int,
    database: Session = Depends(get_db),
    _: User = Depends(require_roles("admin")),
):
    student = database.get(Student, student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    database.delete(student)
    database.commit()