from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.database.models import Student, User
from app.dependencies import get_current_user
from app.schemas.auth import StudentRegistration, Token, UserInfo
from app.security import create_access_token, hash_password, verify_password


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register/student", response_model=UserInfo, status_code=status.HTTP_201_CREATED)
def register_student(registration: StudentRegistration, database: Session = Depends(get_db)):
    student_data = registration.model_dump(exclude={"password"})
    user = User(
        email=registration.email,
        password_hash=hash_password(registration.password),
        role="student",
        student=Student(**student_data),
    )
    database.add(user)
    try:
        database.commit()
    except IntegrityError as error:
        database.rollback()
        raise HTTPException(status_code=409, detail="Email or roll number already exists") from error
    database.refresh(user)
    return user


@router.post("/login", response_model=Token)
def login(
    credentials: OAuth2PasswordRequestForm = Depends(),
    database: Session = Depends(get_db),
):
    user = database.query(User).filter(User.email == credentials.username).first()
    if user is None or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return Token(access_token=create_access_token(str(user.id)))


@router.get("/me", response_model=UserInfo)
def get_me(user: User = Depends(get_current_user)):
    return user