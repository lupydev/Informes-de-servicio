from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer

router = APIRouter(prefix="/api/v1/login", tags=["LogIn"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get("/")
async def login(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}
