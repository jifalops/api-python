from pydantic import BaseModel, EmailStr


class SignUpData(BaseModel):
    email: EmailStr
    password: str
