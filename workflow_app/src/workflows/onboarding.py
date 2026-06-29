from workflow_app.src.core.orchestrator import BaseWorkflow
from workflow_app.src.steps.users_steps import (
    FetchUserDataStep,
    CleanDataStep,
    SaveUserStep
)
from workflow_app.src.steps.notification_steps import SendWelcomeEmailStep

__all__ = ["UserOnboardingWorkflow"]


class UserOnboardingWorkflow(BaseWorkflow):

    def __init__(self, user_id: int, db_repository):

        """Defines the exact pipeline of steps for this specific workflow"""
        steps = [
            FetchUserDataStep(user_id=user_id),
            CleanDataStep(),
            SaveUserStep(db_repository),
            SendWelcomeEmailStep()
        ]

        super().__init__(steps=steps)
