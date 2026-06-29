from workflow_app.src.core.step import WorkflowStep
from workflow_app.src.core.context import WorkflowContext

__all__ = ["SendWelcomeEmailStep"]


class SendWelcomeEmailStep(WorkflowStep):
    """Simulate sending a welcome email to a newly saved user.

    This workflow step retrieves the cleaned user information from the
    WorkflowContext and simulates sending a welcome email by printing a
    message to the console.

    In a production application, this step would typically invoke an email
    service or messaging provider instead of using a print statement.
    """

    def execute(self, context: WorkflowContext) -> None:
        """Execute the welcome email step.

        Retrieves the cleaned user data from the workflow context and
        simulates sending a welcome email.

        Args:
            context (WorkflowContext):
                The shared workflow context containing the cleaned user
                information produced by previous workflow steps.

        Raises:
            KeyError:
                If the required ``cleaned_user_data`` entry is not present
                in the workflow context.
        """
        cleaned_data = context.store["cleaned_user_data"]

        # Simulate sending a welcome email.
        print(
            f"Sending email to user: {cleaned_data['name']}, "
            f"email: {cleaned_data['email']}"
        )
