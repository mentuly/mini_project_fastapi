from os import getenv
from datetime import datetime, timedelta, timezone
from typing import Optional, Annotated
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.orm import Session
from jose import JWTError
import jwt

from ..models import UserModel, TokenData
from .hash import verify_password
from ..helpers import get_session


load_dotenv()

SECRET_KEY = getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl="/login")


def authenticate_user(
    username: str,
    password: str,
    session: Annotated[Session, Depends(get_session)],
):
    user = session.scalar(select(UserModel).where(UserModel.name == username))
    if not user:
        raise HTTPException(status_code=404, detail="No user with this name")
    
    if not verify_password(password, user.password):
        raise HTTPException(status_code=400, detail="Wrong password")
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(
    token: Annotated[str, Depends(OAUTH2_SCHEME)],
    session: Annotated[Session, Depends(get_session)],
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = session.scalar(
        select(UserModel).where(UserModel.name == token_data.username)
    )
    if user is None:
        raise credentials_exception
    return user
