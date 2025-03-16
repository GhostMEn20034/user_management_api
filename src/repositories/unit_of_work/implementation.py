from typing import Any
from sqlalchemy.orm import Session

from .abstract import AbstractUnitOfWork


class UnitOfWork(AbstractUnitOfWork):
    """
    This class manages a transactional unit of work within a database session.

    Fields:
    `session` is an instance of `Session` that manages the database transaction.
                        This session is used to interact with the database within the transaction
                        boundary. It is required to begin, commit, rollback, and close the session.
    """

    def __init__(self, session: Session):
        self._session = session

    def start(self):
        self._session.begin()

    def commit(self) -> None:
        """Saves all changes to the database."""
        self._session.commit()

    def close(self) -> None:
        """Closes the session."""
        self._session.close()

    def rollback(self) -> None:
        """Rollback the current transaction."""
        self._session.rollback()

    def __enter__(self) -> "UnitOfWork":
        """Allows the use of 'with' to manage resources."""
        return self

    def __exit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> None:
        """Handles the exit of the context manager."""
        if exc_type is not None:
            self.rollback()  # Rollback if an exception occurred

        self.close()  # Ensure the session is closed
