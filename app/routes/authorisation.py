from typing import Annotated
from datetime import timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from ..models import UserModel, TokenData
from ..db import User
from ..utils import (
    hash_password,
    authenticate_user,
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)
from ..helpers import get_session


auth_router = APIRouter(prefix="/authorisation", tags=["authorisation"])


@auth_router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Annotated[Session, Depends(get_session)],
) -> TokenData:
    """
    Login for access token (first register):

    - **username (name)**: username
    - **password**: password
    - **scope**: optional
    - **client id**: id of client - optional
    - **client secret**: secret of client - optional
    """
    user = authenticate_user(form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.name}, expires_delta=access_token_expires
    )
    return TokenData(access_token=access_token, token_type="bearer")


@auth_router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: UserModel,
    session: Annotated[Session, Depends(get_session)],
    
):
    """
    Register a new user.

    - **name**: your name
    - **email**: valid email (should not be already registered)
    - **password**: your secure password
    """
    existing_user = session.scalar(select(User).where(User.login == user_data.email))
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(user_data.password)

    new_user = User(
        name=user_data.name, login=user_data.email, password=hashed_password
    )

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return {"message": "User registered successfully!", "user_id": new_user.id}
