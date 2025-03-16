from abc import ABC, abstractmethod
from typing import Generic, Optional, TypeVar, List
from src.models.base import BaseModel


T = TypeVar("T", bound=BaseModel)


class AbstractGenericRepository(Generic[T], ABC):
    """
    Provides basic generic DB operations:
    Get by id, Create, Read List of items, Update, Delete
    """

    @abstractmethod
    def get_by_id(self, id: int) -> Optional[T]:
        """
        Get a single record by id.

        :param id: (int): Record id.
        """
        raise NotImplementedError()

    @abstractmethod
    def list(self, **filters) -> List[T]:
        """
        Gets a list of records

        :param filters: Filter conditions, several criteria are linked with a logical 'and'.

         Raises:
            ValueError: Invalid filter condition.
        """
        raise NotImplementedError()

    @abstractmethod
    def add(self, record: T) -> T:
        """
        Creates a new record.

        :param record: The record to be created.
        """
        raise NotImplementedError()

    @abstractmethod
    def update(self, record: T) -> T:
        """
        Updates an existing record.

        :param record: The record to be updated incl. record id.
        """
        raise NotImplementedError()

    @abstractmethod
    def delete(self, record: T) -> None:
        """
        Deletes a record by id.

        :param record: (int): Record id.
        """
        raise NotImplementedError()