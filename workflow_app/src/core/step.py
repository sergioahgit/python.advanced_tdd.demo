from abc import ABC, abstractmethod

from workflow_app.src.core.context import WorkflowContext

__all__ = ["WorkflowStep"]


class WorkflowStep(ABC):
    """Abstract base class for all workflow steps.  Defines the contract
    for all behavior class.

    WorkflowStep defines the interface that all concrete workflow
    steps must implement. Each step represents a single unit of
    business behavior in the workflow.
    """

    @abstractmethod
    def execute(self, context: WorkflowContext) -> None:
        """
        Subclasses must implement the execute() method, which receives
        a WorkflowContext and modifies it as needed.

        Executes the step logic using the provided WorkflowContext.

        Args:
            context (WorkflowContext):
                Shared workflow state used for reading and writing data.

        Raises:
            NotImplementedError:
                If the subclass does not implement this method.
        """
        pass
