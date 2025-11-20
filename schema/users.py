from pydantic import BaseModel, EmailStr
import uuid

class UserBase(BaseModel):
    full_name: str
    email: EmailStr
    role: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: uuid.UUID
    hashed_password: str