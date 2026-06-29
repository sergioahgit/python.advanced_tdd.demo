from unittest.mock import patch

from workflow_app.src.core.context import WorkflowContext
from workflow_app.src.steps.notification_steps import SendWelcomeEmailStep


@patch("builtins.print")
def test_execute_prints_welcome_email(mock_print):
    """Verify that the workflow step prints the expected welcome email message.

    The ``@patch("builtins.print")`` decorator temporarily replaces
    Python's built-in ``print()`` function with a ``Mock`` object for
    the duration of this test. The injected ``mock_print`` argument
    records calls made to ``print()`` so the test can verify the
    expected output without writing anything to the console.

    Args:
        mock_print:
            Mock object that replaces Python's built-in ``print()``
            function during the execution of this test.
    """

    context = WorkflowContext()
    context.store["cleaned_user_data"] = {
        "id": 123,
        "name": "Sergio",
        "email": "sergio@advanced_tdd.com"
    }

    step = SendWelcomeEmailStep()

    step.execute(context)

    mock_print.assert_called_once_with(
        "Sending email to user: Sergio, "
        "email: sergio@advanced_tdd.com"
    )
