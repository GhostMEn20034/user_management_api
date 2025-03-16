from abc import ABC, abstractmethod
from typing import Tuple, Sequence

from src.models.user import User
from src.schemes.dtos.pagination import PaginationParams, PaginationResponse
from src.schemes.dtos.user import CreateUserRequestBody


class AbstractUserService(ABC):

    @abstractmethod
    def get_user_list(self, pagination_params: PaginationParams) -> Tuple[Sequence[User], PaginationResponse]:
        """
        :param pagination_params: Pagination params like current page, items per page, etc.
        :return: Sequence of users, in the specified amount and pagination metadata.
        """
        raise NotImplementedError()

    @abstractmethod
    def create_user(self, payload: CreateUserRequestBody) -> User:
        """
        :param payload: Users data like name, email, etc.
        :return: Created user
        """
        pass
