from typing import Annotated
from datetime import timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from ..models import UserModel
from ..db import User, Session
from ..utils import hash_password


auth_router = APIRouter(prefix="/authorisation", tags=["authorisation"])


@auth_router.post("/register", status_code=status.HTTP_201_CREATED)
async def registration(user: UserModel):
    with Session() as session:
        user = await session.scalar(select(User).where(User.login == user.email))
        if user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists"
            )
        hashed_password = hash_password(user.password)  

        
        new_user = User(
            name=user.name,
            login=user.email,
            password=hashed_password
        )

        session.add(new_user)
        session.commit()  

        return {"message": "User registered successfully!"}