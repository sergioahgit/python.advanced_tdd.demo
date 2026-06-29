import copy

from workflow_app.src.core.step import WorkflowStep
from workflow_app.src.core.context import WorkflowContext

__all__ = ["FetchUserDataStep", "CleanDataStep", "SaveUserStep" ]


class FetchUserDataStep(WorkflowStep):
    """Retrieve user data and store it in the workflow context.

    This workflow step simulates fetching user information from an
    external source, such as a database or web service. The retrieved
    data is stored in the WorkflowContext for use by subsequent steps.

    Attributes:
        user_id (int):
            The unique identifier of the user to retrieve.
    """

    def __init__(self, user_id: int):
        """Initialize the fetch step.

        Args:
            user_id (int):
                The unique identifier of the user to retrieve.
        """
        self.user_id = user_id

    def execute(self, context: WorkflowContext) -> None:
        """Execute the user data retrieval step.

        Simulates fetching user information and stores the resulting
        data under the ``raw_user_data`` key in the WorkflowContext.

        Args:
            context (WorkflowContext):
                The shared workflow context used to store and exchange
                data between workflow steps.
        """

        print(f"Fetching data for user {self.user_id}")

        # Simulates fetching data
        context.store["raw_user_data"] = {
            "id": self.user_id,
            "name": "Sergio",
            "email": "SERGIO@ADVANCED_TDD.COM"
        }

class CleanDataStep(WorkflowStep):
    """Normalize and prepare user data for persistence.

    This workflow step retrieves the raw user data from the
    WorkflowContext, performs simple transformations, and stores the
    cleaned result for downstream processing.

    Currently, the transformation consists of converting the user's
    email address to lowercase.
    """
    def execute(self, context: WorkflowContext) -> None:
        """Execute the data cleaning step.

        Retrieves the raw user data from the WorkflowContext,
        normalizes the email address, and stores the cleaned result
        under the ``cleaned_user_data`` key.

        If no raw user data exists, the method completes without
        modifying the context.

        Args:
            context (WorkflowContext):
                The shared workflow context containing the raw user data.
        """

        print("Cleaning user data...")

        raw_data = context.store.get("raw_user_data")
        if raw_data:

            # Normalize email to lower case.
            cleaned_user_data = copy.deepcopy(raw_data)
            cleaned_user_data["email"] = cleaned_user_data["email"].lower()

            context.store["cleaned_user_data"] = cleaned_user_data

class SaveUserStep(WorkflowStep):
    """Persist cleaned user data using a repository.

    This workflow step retrieves cleaned user information from the
    WorkflowContext and delegates persistence to the injected
    repository. After a successful save, the generated user identifier
    is stored back into the workflow context.

    Attributes:
        db_repository:
            Repository responsible for persisting user data.
            The repository is expected to provide a ``save_user()``
            method.
    """

    def __init__(self, db_repository):
        """Initialize the save step.

        Args:
            db_repository:
                Repository used to persist user information.
                This dependency is injected to improve testability
                and decouple persistence from workflow behavior.
        """
        self.db_repository = db_repository

    def execute(self, context: WorkflowContext) -> None:
        """Execute the user persistence step.

        Retrieves the cleaned user data from the WorkflowContext,
        persists it using the configured repository, and stores the
        returned user identifier under ``saved_user_id``.

        Args:
            context (WorkflowContext):
                The shared workflow context containing the cleaned
                user data.

        Raises:
            ValueError:
                If ``cleaned_user_data`` is not available in the
                WorkflowContext.
        """

        cleaned_data = context.store.get("cleaned_user_data")

        if not cleaned_data:
            raise ValueError("No cleaned user data found in context")

        # Save the user and get back a new database ID.
        user_id = self.db_repository.save_user(cleaned_data)

        print(f"Updated user {user_id} entry in database.")

        # Update the context with the resulting ID.
        context.store["saved_user_id"] = user_id
