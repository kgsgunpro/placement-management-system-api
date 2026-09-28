import getpass
import sys

from sqlalchemy import select

from app.database.connection import SessionLocal
from app.database.models import User
from app.security import hash_password


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python -m app.create_admin <email>")

    email = sys.argv[1].strip().lower()
    password = getpass.getpass("Admin password (minimum 12 characters): ")
    if len(password) < 12:
        raise SystemExit("Admin password must be at least 12 characters")

    with SessionLocal() as database:
        if database.scalar(select(User).where(User.email == email)) is not None:
            raise SystemExit("A user with that email already exists")
        database.add(User(email=email, password_hash=hash_password(password), role="admin"))
        database.commit()
    print(f"Created admin user {email}")


if __name__ == "__main__":
    main()