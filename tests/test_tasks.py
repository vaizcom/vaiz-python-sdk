import pytest
from tests.test_config import get_test_client, TEST_BOARD_ID, TEST_GROUP_ID, TEST_PROJECT_ID, TEST_ASSIGNEE_ID
from vaiz.models import CreateTaskRequest, EditTaskRequest, TaskPriority, TaskResponse

@pytest.fixture(scope="module")
def client():
    return get_test_client()

@pytest.fixture(scope="module")
def task_id(client):
    """Fixture that creates a test task and returns its ID."""
    task = CreateTaskRequest(
        name="Integration Test Task",
        group=TEST_GROUP_ID,
        board=TEST_BOARD_ID,
        project=TEST_PROJECT_ID,
        priority=TaskPriority.High,
        completed=True,
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
    """Test that task editing works correctly."""
    edit_task = EditTaskRequest(
        taskId=task_id,
        completed=True,
        name="Integration Test Task Updated",
        assignees=[TEST_ASSIGNEE_ID]
    )
    response = client.edit_task(edit_task)
    assert response.type == "EditTask"
    assert response.payload["task"]["name"] == "Integration Test Task Updated"

def test_get_task(client, task_id):
    """Test that task retrieval works correctly."""
    response = client.get_task(task_id)
    assert response.type == "GetTask"
    assert response.payload["task"]["_id"] == task_id
    assert response.payload["task"]["name"] == "Integration Test Task Updated" 