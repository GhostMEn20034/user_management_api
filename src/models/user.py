from datetime import datetime, UTC
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import Integer, String, TIMESTAMP

from .base import BaseModel


class User(BaseModel):
    __tablename__ = 'user'

    id: Mapped[int | None] = mapped_column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    created_at: Mapped[datetime | None] = mapped_column(
        TIMESTAMP,
        default=lambda: datetime.now(UTC),
        nullable=False,
        index=True, # Decided to index it, because I sort user list by created at field
    )
