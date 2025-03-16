from abc import ABC, abstractmethod


class AbstractUnitOfWork(ABC):
    @abstractmethod
    def start(self) -> None:
        pass

    @abstractmethod
    def commit(self) -> None:
        """Saves all changes to the database."""
        pass

    @abstractmethod
    def close(self) -> None:
        """Closes the session."""
        pass

    @abstractmethod
    def rollback(self) -> None:
        """Rollback the current transaction."""
        pass