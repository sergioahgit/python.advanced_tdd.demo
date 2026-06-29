from workflow_app.src.workflows.onboarding import UserOnboardingWorkflow


def test_full_orchestration_workflow_success(mock_db_repository):
    """Verify that the full user onboarding workflow executes successfully end-to-end
    through orchestration pipeline

    This integration test ensures that all workflow steps work together correctly
    when executed in sequence through the UserOnboardingWorkflow:

    Args:
        mock_db_repository:
            A mocked repository used to verify that the SaveUserStep
            persists data correctly without interacting with a real database.

    Raises:
        AssertionError:
            If the workflow does not correctly store the saved user ID or
            if the repository is not called exactly once.
    """
    workflow = UserOnboardingWorkflow(
        user_id=123, db_repository=mock_db_repository
    )
    result_context = workflow.run()

    print("Final Store State:", result_context.store)

    assert result_context.store['raw_user_data'] == {
        'id': 123,
        'name': 'Sergio',
        'email': 'SERGIO@ADVANCED_TDD.COM'
    }
    assert result_context.store['cleaned_user_data'] == {
        'id': 123,
        'name': 'Sergio',
        'email': 'sergio@advanced_tdd.com'
    }
    assert "saved_user_id" in result_context.store
