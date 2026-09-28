"""Create identity and placement workflow tables.

Revision ID: 0001_phase_2_to_4
Revises:
"""
from alembic import op
import sqlalchemy as sa


revision = "0001_phase_2_to_4"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    existing_tables = set(sa.inspect(bind).get_table_names())

    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("role", sa.String(length=20), nullable=False, server_default="student"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint("role IN ('admin', 'student', 'company')", name="ck_users_role"),
        sa.UniqueConstraint("email"),
    )
    if "students" not in existing_tables:
        op.create_table(
            "students",
            sa.Column("id", sa.Integer(), primary_key=True),
            sa.Column("roll_no", sa.String(length=30), nullable=False),
            sa.Column("name", sa.String(length=100), nullable=False),
            sa.Column("passing_out_year", sa.Integer(), nullable=False),
            sa.Column("email", sa.String(length=255), nullable=False),
            sa.Column("phone", sa.String(length=15), nullable=True),
            sa.Column("branch", sa.String(length=50), nullable=False),
            sa.Column("cgpa", sa.Numeric(4, 2), nullable=False),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("user_id", sa.Integer(), nullable=True),
            sa.CheckConstraint("cgpa >= 0 AND cgpa <= 10", name="ck_students_cgpa"),
            sa.ForeignKeyConstraint(["user_id"], ["users.id"], name="fk_students_user_id_users", ondelete="SET NULL"),
            sa.UniqueConstraint("email"),
            sa.UniqueConstraint("roll_no"),
            sa.UniqueConstraint("user_id", name="uq_students_user_id"),
        )
        op.create_index("ix_students_branch", "students", ["branch"], unique=False)
    elif "user_id" not in {column["name"] for column in sa.inspect(bind).get_columns("students")}:
        op.add_column("students", sa.Column("user_id", sa.Integer(), nullable=True))
        op.create_foreign_key("fk_students_user_id_users", "students", "users", ["user_id"], ["id"], ondelete="SET NULL")
        op.create_unique_constraint("uq_students_user_id", "students", ["user_id"])

    op.create_table(
        "companies",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=150), nullable=False),
        sa.Column("website", sa.String(length=255), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "placement_drives",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("company_id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=150), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("min_cgpa", sa.Numeric(4, 2), nullable=False, server_default="0"),
        sa.Column("eligible_branches", sa.JSON(), nullable=True),
        sa.Column("passing_out_year", sa.Integer(), nullable=False),
        sa.Column("application_deadline", sa.Date(), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False, server_default="draft"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint("min_cgpa >= 0 AND min_cgpa <= 10", name="ck_drives_min_cgpa"),
        sa.CheckConstraint("passing_out_year >= 2020 AND passing_out_year <= 2100", name="ck_drives_passing_year"),
        sa.CheckConstraint("status IN ('draft', 'open', 'closed')", name="ck_drives_status"),
        sa.ForeignKeyConstraint(["company_id"], ["companies.id"], ondelete="CASCADE"),
    )
    op.create_index("ix_placement_drives_company_id", "placement_drives", ["company_id"], unique=False)
    op.create_index("ix_placement_drives_status", "placement_drives", ["status"], unique=False)

    op.create_table(
        "applications",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("student_id", sa.Integer(), nullable=False),
        sa.Column("drive_id", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False, server_default="submitted"),
        sa.Column("applied_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.CheckConstraint(
            "status IN ('submitted', 'under_review', 'shortlisted', 'interview', 'selected', 'offered', 'accepted', 'declined', 'rejected')",
            name="ck_applications_status",
        ),
        sa.ForeignKeyConstraint(["drive_id"], ["placement_drives.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["student_id"], ["students.id"], ondelete="CASCADE"),
        sa.UniqueConstraint("student_id", "drive_id", name="uq_applications_student_drive"),
    )
    op.create_index("ix_applications_drive_id", "applications", ["drive_id"], unique=False)
    op.create_index("ix_applications_status", "applications", ["status"], unique=False)
    op.create_index("ix_applications_student_id", "applications", ["student_id"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_applications_student_id", table_name="applications")
    op.drop_index("ix_applications_status", table_name="applications")
    op.drop_index("ix_applications_drive_id", table_name="applications")
    op.drop_table("applications")
    op.drop_index("ix_placement_drives_status", table_name="placement_drives")
    op.drop_index("ix_placement_drives_company_id", table_name="placement_drives")
    op.drop_table("placement_drives")
    op.drop_table("companies")
    bind = op.get_bind()
    student_columns = {column["name"] for column in sa.inspect(bind).get_columns("students")}
    if "user_id" in student_columns:
        op.drop_constraint("uq_students_user_id", "students", type_="unique")
        op.drop_constraint("fk_students_user_id_users", "students", type_="foreignkey")
        op.drop_column("students", "user_id")
    op.drop_table("users")