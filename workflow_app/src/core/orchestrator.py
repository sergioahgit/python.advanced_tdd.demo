from typing import List

from workflow_app.src.core.context import WorkflowContext
from workflow_app.src.core.step import WorkflowStep
from workflow_app.src.utils.logger import logger

__all__ = ["BaseWorkflow"]


class BaseWorkflow:
    """Orchestrates execution of a sequence of workflow steps.

    The BaseWorkflow class is responsible for executing a list of
    WorkflowStep instances in order. It provides centralized control
    over execution flow, error handling, and context management.

    If a step raises an exception, execution is stopped and the error
    is recorded in the WorkflowContext.

    Attributes:
        steps (List[WorkflowStep]):
            Ordered list of workflow steps to execute.

    Methods:
        run():
            Executes all steps sequentially and returns the workflow context
            containing results and any errors encountered.
    """

    def __init__(self, steps: List[WorkflowStep]):
        self.steps = steps

    def run(self) -> WorkflowContext:

        context = WorkflowContext()
        for step in self.steps:

            try:
                logger.info(
                    "Executing step: %s",
                    step.__class__.__name__
                )

                step.execute(context)

            except Exception as e:

                logger.exception(
                    "Step '%s' failed.",
                    step.__class__.__name__
                )

                context.errors.append(e)

                # Here we could implement rollback logic or break the loop
                break

        logger.info("Workflow finished.")
        return context
