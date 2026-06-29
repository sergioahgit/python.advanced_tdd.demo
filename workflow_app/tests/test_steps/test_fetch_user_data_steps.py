import pytest
from workflow_app.src.core.context import WorkflowContext
from workflow_app.src.steps.users_steps import FetchUserDataStep


def test_fetch_user_data_populates_context():
    """Verify that FetchUserDataStep correctly populates raw user data in context.

    This test ensures that the FetchUserDataStep simulates retrieving user data
    and stores the expected structured result in the WorkflowContext.

    It validates that:
    - The step uses the provided user_id correctly
    - The full user payload is created as expected
    - The result is stored under 'raw_user_data' in the context

    This test confirms the correctness of the initial data-fetching step in the
    workflow pipeline.
    """

    context = WorkflowContext()

    step = FetchUserDataStep(user_id=123)

    step.execute(context)

    assert context.store["raw_user_data"] == {
        "id": 123,
        "name": "Sergio",
        "email": "SERGIO@ADVANCED_TDD.COM"
    }
