from abc import abstractmethod, ABC
from typing import Optional, Tuple, Sequence

from sqlalchemy import select, func, desc

from src.models.user import User
from src.repositories.base.abstract import AbstractGenericRepository

from src.schemes.dtos.pagination import PaginationParams


class AbstractUserRepository(AbstractGenericRepository[User], ABC):

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        raise NotImplementedError()

    @abstractmethod
    def get_paginated_user_list(self, pagination_params: PaginationParams) -> Tuple[Sequence[User], int]:
        """
        :param pagination_params: Pagination params like current page, items per page, etc.
        :return: Sequence of users, in the specified amount and total number of users.
        """
        raise NotImplementedError()