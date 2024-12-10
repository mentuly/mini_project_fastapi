from typing import Optional
from pydantic import BaseModel, EmailStr


class User_create(BaseModel):
    name: str
    email: EmailStr
    password: str


class User_login(BaseModel):
    email: EmailStr
    password: str
