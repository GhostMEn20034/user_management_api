from abc import ABC
from typing import TypeVar, Type, Optional, Sequence
from sqlalchemy.orm import Session
from sqlalchemy.sql import select
from sqlalchemy.sql import and_

from src.models.base import BaseModel
from .abstract import AbstractGenericRepository


T = TypeVar("T", bound=BaseModel)


class GenericRepositoryImplementation(AbstractGenericRepository[T], ABC):
    """
    Provides basic generic DB operations:
    Get by id, Create, Read List of items, Update, Delete
    """
    def __init__(self, session: Session, model_cls: Type[T]) -> None:
        """
        :param session: SQLAlchemy Session.
        :param model_cls: SQLAlchemy model class type.
        """
        self._session = session
        self._model_cls = model_cls

    def _construct_get_stmt(self, id: int):
        """Creates a SELECT query for retrieving a single record."""
        return select(self._model_cls).where(self._model_cls.id == id)

    def get_by_id(self, id: int) -> Optional[T]:
        stmt = self._construct_get_stmt(id)
        result = self._session.execute(stmt)
        return result.scalars().first()

    def _construct_list_stmt(self, **filters):
        """Creates a SELECT query for retrieving multiple records."""
        stmt = select(self._model_cls)
        where_clauses = []
        for c, v in filters.items():
            if not hasattr(self._model_cls, c):
                raise ValueError(f"Invalid column name {c}")
            where_clauses.append(getattr(self._model_cls, c) == v)

        if where_clauses:
            stmt = stmt.where(and_(*where_clauses))
        return stmt

    def list(self, **filters) -> Sequence[T]:
        stmt = self._construct_list_stmt(**filters)
        result = self._session.execute(stmt)
        return result.scalars().all()

    def add(self, record: T) -> T:
        self._session.add(record)
        self._session.commit()
        self._session.refresh(record)
        return record

    def update(self, record: T) -> T:
        self._session.add(record)
        self._session.commit()
        self._session.refresh(record)
        return record

    def delete(self, record: T) -> None:
        if record is not None:
            self._session.delete(record)
            self._session.commit()
