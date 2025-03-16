from typing import Optional, Tuple, Sequence

from sqlalchemy import select, func, desc
from sqlalchemy.orm import Session

from src.models.user import User
from src.repositories.base.implementation import GenericRepositoryImplementation
from src.repositories.user.abstract import AbstractUserRepository
from src.schemes.dtos.pagination import PaginationParams


class UserRepositoryImplementation(GenericRepositoryImplementation[User], AbstractUserRepository):
    def __init__(self, session: Session) -> None:
        super().__init__(session, User)

    def get_by_email(self, email: str) -> Optional[User]:
        stmt = select(User).where(User.email == email)
        result = self._session.execute(stmt)
        return result.first()

    def get_paginated_user_list(self, pagination_params: PaginationParams) -> Tuple[Sequence[User], int]:
        offset, limit = pagination_params.get_offset_and_limit()

        stmt = select(User, func.count().over().label("total_count"), )

        # ORDER BY → OFFSET → LIMIT
        stmt = (
            stmt
            .order_by(desc(User.created_at))
            .offset(offset)
            .limit(limit)
        )

        result = self._session.execute(stmt)
        rows = result.all()

        if rows:
            paginated_items = [row[0] for row in rows]  # Extract User objects
            total_count = rows[0][1]  # Extract total_count from the first row
        else:
            paginated_items = []
            total_count = 0

        return paginated_items, total_count