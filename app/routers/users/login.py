from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import Session
from utils.jwt_manager import create_token
from utils.services import authenticate_user
from db.config import get_session
from db.schemas.token import Token
from db.security import oauth2_scheme

router = APIRouter(prefix="/api/v1/login", tags=["LogIn"])


@router.post(
    "",
    status_code=status.HTTP_200_OK,
)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_session),
):
    user = authenticate_user(db, form_data.username, form_data.password)

    if not user.active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User is inactive."
        )

    token_jwt = create_token(user.id, user.active, user.verified)
    token = Token(
        access_token=token_jwt,
        token_type="bearer",
    )
    return token
