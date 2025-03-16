from typing import List

import pytest

from src.models.user import User


@pytest.fixture
def prepopulated_users(test_db_session) -> List[User]:
    users = [
        User(
            name="John Doe",
            email="someemail@example.com",
        ),
        User(
            name="John Wick",
            email="someemail2@example.com",
        ),
        User(
            name="Undefined person",
            email="undefined@somedomain.com",
        )
    ]

    for user in users:
        test_db_session.add(user)


    test_db_session.commit()

    for user in users:
        test_db_session.refresh(user)


    return users
