from sqlalchemy.orm import Session

# services
from src.services.user.abstract import AbstractUserService
from src.services.user.implementation import UserServiceImplementation
# Repositories + Unit of work
from src.repositories.unit_of_work.implementation import UnitOfWork
from src.repositories.user.implementation import UserRepositoryImplementation


def get_user_service(db_session: Session) -> AbstractUserService:
    uow = UnitOfWork(db_session)
    user_repository = UserRepositoryImplementation(db_session)

    return UserServiceImplementation(
        uow=uow,
        user_repository=user_repository,
    )
