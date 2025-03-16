from typing import Tuple, Sequence
from sqlalchemy.exc import IntegrityError

from .abstract import AbstractUserService
from src.exceptions.user import UserNotFoundError
# Repositories
from src.repositories.unit_of_work.abstract import AbstractUnitOfWork
from src.repositories.user.abstract import AbstractUserRepository
# DTOS
from src.schemes.dtos.pagination import PaginationParams, PaginationResponse
from src.schemes.dtos.user import CreateUserRequestBody, UpdateUserRequestBody

from src.models.user import User


class UserServiceImplementation(AbstractUserService):
    def __init__(self, uow: AbstractUnitOfWork, user_repository: AbstractUserRepository):
        self._uow = uow
        self._user_repository = user_repository

    def get_user_list(self, pagination_params: PaginationParams) -> Tuple[Sequence[User], PaginationResponse]:
        items, total_count = self._user_repository.get_paginated_user_list(pagination_params)
        total_pages = pagination_params.get_total_pages(total_count)

        pagination_response = PaginationResponse(
            current_page=pagination_params.page,
            page_size=pagination_params.page_size,
            total_pages=total_pages,
            total_items=total_count,
        )

        return items, pagination_response

    def get_user_details(self, user_id: int) -> User:
        user = self._user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundError(user_id)

        return user

    def create_user(self, payload: CreateUserRequestBody) -> User:
        with self._uow:
            user_to_create = User(
                name=payload.name,
                email=payload.email,
            )
            try:
                created_user = self._user_repository.add(user_to_create)
                self._uow.commit()
            except IntegrityError:
                self._uow.rollback()
                raise ValueError("A user with this name already exists.")

            return created_user

    def update_user(self, user_id: int, payload: UpdateUserRequestBody) -> User:
        with self._uow:
            user_to_update = self._user_repository.get_by_id(user_id)
            if not user_to_update:
                raise UserNotFoundError(user_id)

            try:
                user_to_update.email = payload.email
                user_to_update.name = payload.name

                self._user_repository.update(user_to_update)
                self._uow.commit()
            except IntegrityError:
                self._uow.rollback()
                raise ValueError("A user with this name already exists.")

            return user_to_update

    def delete_user(self, user_id: int):
        with self._uow:
            user_to_delete = self._user_repository.get_by_id(user_id)
            if not user_to_delete:
                raise UserNotFoundError(user_id)

            self._user_repository.delete(user_to_delete)
            self._uow.commit()
