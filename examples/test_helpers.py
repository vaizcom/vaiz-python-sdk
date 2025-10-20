"""
Helper functions for creating test data in examples and tests.
"""

from vaiz.models import CreateTaskRequest, TaskPriority
from tests.test_config import get_test_client, TEST_BOARD_ID, TEST_GROUP_ID, TEST_PROJECT_ID, TEST_ASSIGNEE_ID


def create_test_task_and_get_document_id(task_name="Test Task for Comment Examples") -> str:
    """
    Create a test task and return its document ID.
    This ensures we have a valid document to comment on.
    
    Args:
        task_name (str): Name for the test task
        
    Returns:
        str: Document ID of the created task
    """
    client = get_test_client()
    
    task = CreateTaskRequest(
        name=task_name,
        group=TEST_GROUP_ID,
        board=TEST_BOARD_ID,
        project=TEST_PROJECT_ID,
        priority=TaskPriority.High,
        completed=False,
        types=[],
        assignees=[TEST_ASSIGNEE_ID] if TEST_ASSIGNEE_ID else [],
        subtasks=[],
        milestones=[],
        blocking=[],
        blockers=[]
    )
    
    response = client.create_task(task)
    assert response.type == "CreateTask"
    
    # Extract document ID from the created task
    task_data = response.task
    document_id = task_data.document
    print(f"✅ Created test task '{task_name}' with document ID: {document_id}")
    return document_id


def get_or_create_document_id() -> str:
    """
    Get a document ID for examples. Creates a new test task if needed.
    
    Returns:
        str: Document ID to use for examples
    """
    return create_test_task_and_get_document_id("Example Task for Comments") 