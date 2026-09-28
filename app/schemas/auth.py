from pydantic import BaseModel, EmailStr, Field

from app.schemas.student import NewStudent


class StudentRegistration(NewStudent):
    password: str = Field(min_length=8, max_length=128)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserInfo(BaseModel):
    id: int
    email: EmailStr
    role: str

    model_config = {"from_attributes": True}