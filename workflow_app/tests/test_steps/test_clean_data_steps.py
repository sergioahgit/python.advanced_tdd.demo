from workflow_app.src.core.context import WorkflowContext
from workflow_app.src.steps.users_steps import CleanDataStep

def test_clean_data_creates_cleaned_user_data():
    """Verify that CleanDataStep correctly creates normalized user data.

    This test ensures that CleanDataStep transforms raw user data into a
    cleaned version stored in the WorkflowContext.

    It validates that:
    - Raw user data is read from 'raw_user_data'
    - Email addresses are normalized to lowercase
    - The result is stored under 'cleaned_user_data'
    - The transformation preserves all existing user fields

    This test confirms the correctness of the data cleaning transformation
    step in the workflow pipeline.
    """
    context = WorkflowContext()

    context.store["raw_user_data"] = {
        "id": 123,
        "name": "Sergio",
        "email": "SERGIO@ADVANCED_TDD.COM"
    }

    CleanDataStep().execute(context)

    assert context.store["cleaned_user_data"]["email"] == (
        "sergio@advanced_tdd.com"
    )
