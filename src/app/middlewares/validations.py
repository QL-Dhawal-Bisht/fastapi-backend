from pydantic import BaseModel, EmailStr, validator

class RegisterLoginSchema(BaseModel):
    email: EmailStr
    password: str
    name: str = None

    @validator('password')
    def password_length(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v
