from typing import List, Any, Dict

__all__ = ["WorkflowContext"]


class WorkflowContext:
    """Shared state container for workflow execution.  Keeps track of state
    and data throughout the workflow.

    The WorkflowContext is used to store and share data between
    workflow steps during execution. It acts as a lightweight
    in-memory data structure that enables decoupled communication
    between steps.

    Attributes:
        store (Dict[str, Any]):
            A dictionary used to hold arbitrary workflow data
            produced and consumed by steps.

        errors (List[Exception]):
            A list of exceptions collected during workflow execution.
            This allows the workflow to continue tracking failures
            without immediately crashing the system.
    """

    def __init__(self):
        self.store: Dict[str, Any] = {}
        self.errors: List[Exception] = []
