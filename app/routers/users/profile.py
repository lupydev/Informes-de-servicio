import uuid
from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from db.config import get_session
from db.models.users import User
from utils.services import get_user_id
from db.security import oauth2_scheme


router = APIRouter(
    prefix="/api/v1/profile",
    tags=["Profile"],
)


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=User)
async def get_user(
    id: uuid.UUID,
    db: Session = Depends(get_session),
    token: Session = Depends(oauth2_scheme),
):
    return get_user_id(db, id)
