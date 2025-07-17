import pytest
from datetime import datetime
from tests.test_config import get_test_client, TEST_BOARD_ID, TEST_GROUP_ID, TEST_PROJECT_ID, TEST_ASSIGNEE_ID
from vaiz.models import CreateTaskRequest, EditTaskRequest, TaskPriority, TaskResponse

@pytest.fixture(scope="module")
def client():
    return get_test_client()

@pytest.fixture(scope="module")
def task_id(client):
    """Fixture that creates a test task with due dates and returns its ID."""
    task = CreateTaskRequest(
        name="Integration Test Task",
        group=TEST_GROUP_ID,
        board=TEST_BOARD_ID,
        project=TEST_PROJECT_ID,
        priority=TaskPriority.High,
        completed=False,  # Changed to False so we can test completion later
        dueStart=datetime(2025, 2, 1, 9, 0, 0),    # February 1st, 9:00 AM
        dueEnd=datetime(2025, 2, 15, 17, 0, 0),    # February 15th, 5:00 PM
        types=[],
        assignees=[TEST_ASSIGNEE_ID],
        subtasks=[],
        milestones=[],
        rightConnectors=[],
        leftConnectors=[]
    )
    response = client.create_task(task)
    assert response.type == "CreateTask"
    return response.payload["task"]["_id"]

def test_create_task(client, task_id):
    """Test that task creation returns a valid task ID."""
    assert task_id

def test_edit_task(client, task_id):
    """Test that task editing works correctly with datetime due dates."""
    edit_task = EditTaskRequest(
        taskId=task_id,
        completed=True,
        name="Integration Test Task Updated",
        assignees=[TEST_ASSIGNEE_ID],
        dueStart=datetime(2025, 3, 1, 10, 0, 0),   # March 1st, 10:00 AM (updated)
        dueEnd=datetime(2025, 3, 20, 16, 0, 0)     # March 20th, 4:00 PM (updated)
    )
    response = client.edit_task(edit_task)
    assert response.type == "EditTask"
    assert response.payload["task"]["name"] == "Integration Test Task Updated"
    
    # Verify the task now has the updated due dates
    task_data = response.payload["task"]
    # Note: API returns ISO strings, but when parsed through TaskResponse model they become datetime objects
    print(f"Updated dueStart: {task_data.get('dueStart')}")
    print(f"Updated dueEnd: {task_data.get('dueEnd')}")

def test_get_task(client, task_id):
    """Test that task retrieval works correctly and shows datetime objects."""
    response = client.get_task(task_id)
    assert response.type == "GetTask"
    assert response.payload["task"]["_id"] == task_id
    assert response.payload["task"]["name"] == "Integration Test Task Updated"
    
    # Check that due dates are properly set  
    task_data = response.payload["task"]
    assert task_data.get("dueStart") is not None
    assert task_data.get("dueEnd") is not None
    print(f"Retrieved dueStart: {task_data.get('dueStart')}")
    print(f"Retrieved dueEnd: {task_data.get('dueEnd')}") 