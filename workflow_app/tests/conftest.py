"""This code is intended to define a reusable pytest fixture that
provides a mocked database repository."""

import pytest
from unittest.mock import Mock

__all__ = ["mock_db_repository"]


@pytest.fixture
def mock_db_repository():
    """
    A pytest fixture is a function that provides setup objects for tests.
    In this case, this fixture should create a mock object that behaves
    like a database repository.  Providing a reusable mock database
    repository for step tests.

    In tests, you usually don't want to connect to a real database.
    A mock lets you:
        1. control return values
        2. simulate failures
        3. verify method calls
        4. keep tests fast and isolated
    """

    # A Mock object will automatically create mock attributes and methods
    # when you access them.
    mock = Mock()

    # During test, we don't care about actually saving a user. You just want
    # to return a predictable value.  This will ensure the code under test
    # behaves as if the database returned user ID 123.
    mock.save_user.return_value = 123

    return mock
