import os
from datetime import date, timedelta

from sqlalchemy import select

from app.database.connection import SessionLocal
from app.database.models import Application, Company, PlacementDrive, Student, User
from app.security import hash_password


STUDENTS = (
    {
        "roll_no": "DEMO-2027-001",
        "name": "Alex Johnson",
        "passing_out_year": 2027,
        "email": "test-student@example.com",
        "phone": "9000000001",
        "branch": "CSE",
        "cgpa": 8.7,
    },
    {
        "roll_no": "DEMO-2027-002",
        "name": "Sam Patel",
        "passing_out_year": 2027,
        "email": "test-student-ineligible@example.com",
        "phone": "9000000002",
        "branch": "ECE",
        "cgpa": 6.2,
    },
)

COMPANIES = (
    {"name": "Acme Software", "website": "https://example.com", "description": "Software product company"},
    {"name": "Northstar Robotics", "website": "https://example.org", "description": "Robotics and embedded systems"},
    {"name": "Greenfield Analytics", "website": "https://example.net", "description": "Data and analytics company"},
)


def seed_demo_data() -> None:
    student_password = os.getenv("DEMO_STUDENT_PASSWORD")
    if not student_password or len(student_password) < 12:
        raise RuntimeError("Set DEMO_STUDENT_PASSWORD to a value of at least 12 characters")

    with SessionLocal() as database:
        students: dict[str, Student] = {}
        for student_data in STUDENTS:
            email = student_data["email"]
            user = database.scalar(select(User).where(User.email == email))
            if user is None:
                user = User(email=email, password_hash=hash_password(student_password), role="student")
                database.add(user)
                database.flush()
            elif user.role != "student":
                raise RuntimeError(f"Refusing to change non-student account {email}")
            else:
                user.password_hash = hash_password(student_password)

            student = database.scalar(select(Student).where(Student.roll_no == student_data["roll_no"]))
            if student is None:
                student = Student(**student_data, user_id=user.id)
                database.add(student)
            else:
                for field, value in student_data.items():
                    setattr(student, field, value)
                student.user_id = user.id
            students[email] = student
            database.flush()

        companies: dict[str, Company] = {}
        for company_data in COMPANIES:
            company = database.scalar(select(Company).where(Company.name == company_data["name"]))
            if company is None:
                company = Company(**company_data)
                database.add(company)
            else:
                for field, value in company_data.items():
                    setattr(company, field, value)
            companies[company_data["name"]] = company
            database.flush()

        drive_data = (
            {
                "company": "Acme Software",
                "title": "Graduate Software Engineer",
                "description": "Entry-level software engineering role",
                "min_cgpa": 7.0,
                "eligible_branches": ["CSE", "IT"],
                "passing_out_year": 2027,
                "application_deadline": date.today() + timedelta(days=30),
                "status": "open",
            },
            {
                "company": "Northstar Robotics",
                "title": "Embedded Engineer",
                "description": "Embedded systems graduate role",
                "min_cgpa": 7.5,
                "eligible_branches": ["ECE", "EEE"],
                "passing_out_year": 2027,
                "application_deadline": date.today() + timedelta(days=30),
                "status": "open",
            },
            {
                "company": "Greenfield Analytics",
                "title": "Data Internship 2028",
                "description": "Data analytics internship for the 2028 graduating class",
                "min_cgpa": 6.5,
                "eligible_branches": ["CSE", "IT", "DS"],
                "passing_out_year": 2028,
                "application_deadline": date.today() + timedelta(days=45),
                "status": "draft",
            },
        )
        drives: dict[str, PlacementDrive] = {}
        for values in drive_data:
            company_name = values["company"]
            title = values["title"]
            drive = database.scalar(
                select(PlacementDrive).where(
                    PlacementDrive.company_id == companies[company_name].id,
                    PlacementDrive.title == title,
                )
            )
            drive_values = {key: value for key, value in values.items() if key != "company"}
            if drive is None:
                drive = PlacementDrive(company_id=companies[company_name].id, **drive_values)
                database.add(drive)
            else:
                for field, value in drive_values.items():
                    setattr(drive, field, value)
            drives[title] = drive
            database.flush()

        sample_application = database.scalar(
            select(Application).where(
                Application.student_id == students["test-student@example.com"].id,
                Application.drive_id == drives["Graduate Software Engineer"].id,
            )
        )
        if sample_application is None:
            database.add(
                Application(
                    student_id=students["test-student@example.com"].id,
                    drive_id=drives["Graduate Software Engineer"].id,
                )
            )

        database.commit()


if __name__ == "__main__":
    seed_demo_data()
    print("Demo students, companies, drives, and application are ready")