from datetime import datetime
from sqlmodel import Field, SQLModel
import uuid


class AbstractBase(SQLModel):
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        index=True,
    )
    created: datetime = Field(default_factory=datetime.utcnow)
    updated: datetime = Field(default_factory=datetime.utcnow)
    active: bool = Field(default=True)
    verified: bool = Field(default=False)
