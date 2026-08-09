
from fastapi import APIRouter, HTTPException
from psycopg.errors import UniqueViolation

from app.database.connection import student_db
from app.schemas.student import NewStudent, Student


router = APIRouter(
    prefix="/students",
    tags=["Students"],
)


# -------------------------
# GET ALL STUDENTS
# -------------------------

@router.get("/", response_model=list[Student])
async def get_students():

    with student_db.cursor() as cur:

        cur.execute(
            """
            SELECT *
            FROM students
            ORDER BY id;
            """
        )

        students = cur.fetchall()

    return students


# -------------------------
# GET STUDENT BY ID
# -------------------------

@router.get("/{id}", response_model=Student)
async def get_student_by_id(id: int):

    with student_db.cursor() as cur:

        cur.execute(
            """
            SELECT *
            FROM students
            WHERE id = %s;
            """,
            (id,),
        )

        student = cur.fetchone()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found",
        )

    return student


# -------------------------
# CREATE STUDENT
# -------------------------

@router.post("/", response_model=Student, status_code=201)
async def create_student(student: NewStudent):

    try:

        with student_db.cursor() as cur:

            cur.execute(
                """
                INSERT INTO students (
                    roll_no,
                    name,
                    passing_out_year,
                    email,
                    phone,
                    branch,
                    cgpa
                )
                VALUES (
                    %(roll_no)s,
                    %(name)s,
                    %(passing_out_year)s,
                    %(email)s,
                    %(phone)s,
                    %(branch)s,
                    %(cgpa)s
                )
                RETURNING *;
                """,
                student.model_dump(),
            )

            new_student = cur.fetchone()

        student_db.commit()

        return new_student

    except UniqueViolation:

        student_db.rollback()

        raise HTTPException(
            status_code=409,
            detail="Roll number or email already exists",
        )


# -------------------------
# UPDATE STUDENT
# -------------------------

@router.put("/{id}", response_model=Student)
async def update_student(
    id: int,
    student: NewStudent,
):

    try:

        with student_db.cursor() as cur:

            cur.execute(
                """
                UPDATE students
                SET
                    roll_no = %(roll_no)s,
                    name = %(name)s,
                    passing_out_year = %(passing_out_year)s,
                    email = %(email)s,
                    phone = %(phone)s,
                    branch = %(branch)s,
                    cgpa = %(cgpa)s
                WHERE id = %(id)s
                RETURNING *;
                """,
                {
                    **student.model_dump(),
                    "id": id,
                },
            )

            updated_student = cur.fetchone()

        if updated_student is None:

            student_db.rollback()

            raise HTTPException(
                status_code=404,
                detail="Student not found",
            )

        student_db.commit()

        return updated_student

    except UniqueViolation:

        student_db.rollback()

        raise HTTPException(
            status_code=409,
            detail="Roll number or email already exists",
        )


# -------------------------
# DELETE STUDENT
# -------------------------

@router.delete("/{id}", status_code=204)
async def delete_student(id: int):

    with student_db.cursor() as cur:

        cur.execute(
            """
            DELETE FROM students
            WHERE id = %s
            RETURNING id;
            """,
            (id,),
        )

        deleted_student = cur.fetchone()

    if deleted_student is None:

        student_db.rollback()

        raise HTTPException(
            status_code=404,
            detail="Student not found",
        )

    student_db.commit()

    return None
