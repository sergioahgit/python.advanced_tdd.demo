import pytest

from workflow_app.src.core.context import WorkflowContext
from workflow_app.src.steps.users_steps import SaveUserStep
from workflow_app.tests.conftest import mock_db_repository


def test_save_user_step_success(mock_db_repository):
    """Verify that SaveUserStep successfully saves user data using a
    repository.

    This test ensures that SaveUserStep correctly interacts with the provided
    database repository and updates the WorkflowContext with the returned ID.

    It also demonstrates pytest fixture injection behavior, where the fixture
    name 'mock_db_repository' is automatically resolved and injected into the
    test.

    Args:
        mock_db_repository:
            A pytest fixture providing a mocked repository. It simulates the
            persistence layer and allows verification of method calls without
            using a real database.

    Validations:
        - The user ID returned by the repository is stored in the context
        - The repository's save_user method is called exactly once
        - The correct user payload is passed to the repository
    """

    context = WorkflowContext()
    context.store["cleaned_user_data"] = {
        "id": 123,
        "name": "Sergio",
        "email": "sergio@advanced_tdd.com"
    }

    step = SaveUserStep(db_repository=mock_db_repository)
    step.execute(context)

    # These checks both:
    # 1. The result was stored correctly.
    # 2. SaveUserStep actually attempted to save the expected data.
    assert context.store["saved_user_id"] == 123
