from datetime import date, datetime, timezone

from sqlalchemy import CheckConstraint, Date, DateTime, ForeignKey, Integer, JSON, Numeric, String, Text, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class User(Base):
    __tablename__ = "users"
    __table_args__ = (CheckConstraint("role IN ('admin', 'student', 'company')", name="ck_users_role"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(20), default="student")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

    student: Mapped["Student | None"] = relationship(back_populates="user", uselist=False)


class Student(Base):
    __tablename__ = "students"
    __table_args__ = (
        CheckConstraint("cgpa >= 0 AND cgpa <= 10", name="ck_students_cgpa"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    roll_no: Mapped[str] = mapped_column(String(30), unique=True)
    name: Mapped[str] = mapped_column(String(100))
    passing_out_year: Mapped[int] = mapped_column(Integer)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    phone: Mapped[str | None] = mapped_column(String(15), nullable=True)
    branch: Mapped[str] = mapped_column(String(50), index=True)
    cgpa: Mapped[float] = mapped_column(Numeric(4, 2))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), unique=True, nullable=True)

    user: Mapped["User | None"] = relationship(back_populates="student")
    applications: Mapped[list["Application"]] = relationship(back_populates="student", cascade="all, delete-orphan")


class Company(Base):
    __tablename__ = "companies"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(150), unique=True)
    website: Mapped[str | None] = mapped_column(String(255), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

    drives: Mapped[list["PlacementDrive"]] = relationship(back_populates="company", cascade="all, delete-orphan")


class PlacementDrive(Base):
    __tablename__ = "placement_drives"
    __table_args__ = (
        CheckConstraint("min_cgpa >= 0 AND min_cgpa <= 10", name="ck_drives_min_cgpa"),
        CheckConstraint("passing_out_year >= 2020 AND passing_out_year <= 2100", name="ck_drives_passing_year"),
        CheckConstraint("status IN ('draft', 'open', 'closed')", name="ck_drives_status"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id", ondelete="CASCADE"), index=True)
    title: Mapped[str] = mapped_column(String(150))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    min_cgpa: Mapped[float] = mapped_column(Numeric(4, 2), default=0)
    eligible_branches: Mapped[list[str] | None] = mapped_column(JSON, nullable=True)
    passing_out_year: Mapped[int] = mapped_column(Integer)
    application_deadline: Mapped[date] = mapped_column(Date)
    status: Mapped[str] = mapped_column(String(20), default="draft", index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

    company: Mapped["Company"] = relationship(back_populates="drives")
    applications: Mapped[list["Application"]] = relationship(back_populates="drive", cascade="all, delete-orphan")


class Application(Base):
    __tablename__ = "applications"
    __table_args__ = (
        UniqueConstraint("student_id", "drive_id", name="uq_applications_student_drive"),
        CheckConstraint(
            "status IN ('submitted', 'under_review', 'shortlisted', 'interview', 'selected', 'offered', 'accepted', 'declined', 'rejected')",
            name="ck_applications_status",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id", ondelete="CASCADE"), index=True)
    drive_id: Mapped[int] = mapped_column(ForeignKey("placement_drives.id", ondelete="CASCADE"), index=True)
    status: Mapped[str] = mapped_column(String(20), default="submitted", index=True)
    applied_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    student: Mapped["Student"] = relationship(back_populates="applications")
    drive: Mapped["PlacementDrive"] = relationship(back_populates="applications")