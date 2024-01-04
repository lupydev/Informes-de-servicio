from sqlmodel import Field, SQLModel
from typing import Optional
from db.models.abstact import AbstractBase


class User(AbstractBase, table=True):
    name: Optional[str] = Field(
        default=None,
    )
    surname: Optional[str] = Field(
        default=None,
    )
    username: Optional[str] = Field(
        nullable=False,
        min_length=2,
        unique=True,
    )
    email: str = Field(
        nullable=False,
        unique=True,
    )
    password: str
