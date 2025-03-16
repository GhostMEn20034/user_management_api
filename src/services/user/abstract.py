from abc import ABC, abstractmethod
from typing import Tuple, Sequence

from src.models.user import User
from src.schemes.dtos.pagination import PaginationParams, PaginationResponse
from src.schemes.dtos.user import CreateUserRequestBody, UpdateUserRequestBody


class AbstractUserService(ABC):

    @abstractmethod
    def get_user_list(self, pagination_params: PaginationParams) -> Tuple[Sequence[User], PaginationResponse]:
        """
        :param pagination_params: Pagination params like current page, items per page, etc.
        :return: Sequence of users, in the specified amount and pagination metadata.
        """
        raise NotImplementedError()

    @abstractmethod
    def get_user_details(self, user_id: int) -> User:
        """
        :param user_id: User's identifier
        :return: The user if exists
        """
        raise NotImplementedError()

    @abstractmethod
    def create_user(self, payload: CreateUserRequestBody) -> User:
        """
        :param payload: Users data like name, email, etc.
        :return: Created user
        """
        raise NotImplementedError()

    @abstractmethod
    def update_user(self, user_id: int, payload: UpdateUserRequestBody) -> User:
        """
        :param user_id: The identifier of the user that need to be to updated
        :param payload: Data need to be to applied
        :return: Updated user
        """
        raise NotImplementedError()

    @abstractmethod
    def delete_user(self, user_id: int):
        """
        :param user_id: The identifier of the user that need to be to deleted
        :return: Nothing
        """
        raise NotImplementedError()
