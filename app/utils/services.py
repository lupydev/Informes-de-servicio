from typing import Annotated
import uuid
from fastapi import Depends, HTTPException, status
from sqlmodel import Session, select
from db.config import get_session
from utils.jwt_manager import decode_token
from db.security import verify_password
from db.models.users import User
from db.security import oauth2_scheme
from jose import JWTError


def get_user(db: Session, username: str):
    user = db.exec(select(User).where(User.username == username)).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


def authenticate_user(
    db: Session,
    username: str,
    plain_password: str,
):
    user = get_user(db, username)
    if not verify_password(plain_password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_user(
    db: Session = Depends(get_session), token: str = Depends(oauth2_scheme)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        decode = decode_token(token)
        user_id = decode.get("id", None)
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.exec(select(User).where(User.id == user_id)).first()

    if user is None:
        raise credentials_exception

    return user


async def get_current_active_verified_user(user: User = Depends(get_current_user)):
    if not user.active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User is inactive."
        )
    if not user.verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="user is not verified, an email was sent to verify the authenticity.",
        )
    return user
