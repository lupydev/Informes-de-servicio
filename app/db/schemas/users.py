from typing import Optional
from pydantic import EmailStr, BaseModel
from sqlmodel import Field


class CreateUser(BaseModel):
    username: Optional[str] = Field(
        nullable=False,
        min_length=2,
        unique=True,
    )
    email: EmailStr = Field(
        nullable=False,
        unique=True,
    )
    password: str


class UpdateUser(BaseModel):
    name: Optional[str] = Field(
        default=None,
    )
    surname: Optional[str] = Field(
        default=None,
    )
    username: Optional[str] = Field(
        default=None,
        min_length=2,
        unique=True,
    )
    email: EmailStr = Field(
        default=None,
        unique=True,
    )
    password: Optional[str] = Field(
        default=None,
        min_length=4,
    )
