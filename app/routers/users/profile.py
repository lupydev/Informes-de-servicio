from datetime import datetime
from typing import List
import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from db.schemas.users import UpdateUser
from db.config import get_session
from db.models.users import User
from utils.services import get_current_active_verified_user, get_user
from db.security import oauth2_scheme, validate_password


router = APIRouter(
    prefix="/api/v1/profile",
    tags=["Profile"],
)

# ruta a la cual solo deberia entrar super usuario
# @router.get("s", status_code=status.HTTP_200_OK)
# async def get_users(db: Session = Depends(get_session)) -> List[User]:
#     users = db.exec(select(User)).all()
#     return users


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=User,
)
async def get_user_id(user: User = Depends(get_current_active_verified_user)):
    return user


@router.put("", status_code=status.HTTP_200_OK, response_model=User)
async def update_user(
    update_user: UpdateUser,
    db: Session = Depends(get_session),
    user: User = Depends(get_current_active_verified_user),
):
    for field, value in update_user.model_dump(exclude_unset=True).items():
        setattr(user, field, value)
    user.updated = datetime.utcnow()

    db.commit()
    db.refresh(user)
    return user


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=User)
async def get_user_id(
    id: uuid.UUID,
    user: User = Depends(get_current_active_verified_user),
):
    if not user.id == id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have the authorization.",
        )
    return user


@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=User)
async def update_user(
    id: uuid.UUID,
    update_user: UpdateUser,
    db: Session = Depends(get_session),
    user: User = Depends(get_current_active_verified_user),
):
    if not user.id == id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have the authorization.",
        )
    for field, value in update_user.model_dump(exclude_unset=True).items():
        setattr(user, field, value)
    user.updated = datetime.utcnow()

    db.commit()
    db.refresh(user)
    return user
