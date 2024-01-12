from datetime import datetime, time
from typing import Optional
import uuid
from sqlmodel import Field, SQLModel
from db.models.users import User


def currente_date_format():
    return datetime.utcnow().strftime("%Y/%m/%d")


class Report(SQLModel, table=True):
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        index=True,
    )
    user_id: uuid.UUID = Field(foreign_key="user.id")
    date: Optional[datetime] = Field(default_factory=currente_date_format)
    hours: time = Field(default="00:00")
    publications: Optional[int] = Field(default=0)
    videos: Optional[int] = Field(default=0)
    return_visits: Optional[int] = Field(default=0)
    bible_studies: Optional[int] = Field(default=0)
