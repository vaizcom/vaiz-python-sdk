import pytest
from tests.test_config import get_test_client, TEST_BOARD_ID, TEST_GROUP_ID, TEST_PROJECT_ID, TEST_ASSIGNEE_ID
from vaiz.models import CreateTaskRequest, EditTaskRequest, TaskPriority

@pytest.fixture(scope="module")
def client():
    return get_test_client()

@pytest.fixture(scope="module")
def task_id(client):
    task = CreateTaskRequest(
        name="Integration Test Task",
        group=TEST_GROUP_ID,
        board=TEST_BOARD_ID,
        project=TEST_PROJECT_ID,
        priority=TaskPriority.High,
        completed=False,
        types=["649bea169d17e4070e0337fa"],
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
    assert task_id

def test_edit_task(client, task_id):
    edit_task = EditTaskRequest(
        taskId=task_id,
        name="Integration Test Task Updated",
        assignees=[TEST_ASSIGNEE_ID]
    )
    response = client.edit_task(edit_task)
    assert response.type == "EditTask"
    assert response.payload["task"]["name"] == "Integration Test Task Updated"

def test_get_task(client, task_id):
    response = client.get_task(task_id)
    assert response.type == "GetTask"
    assert response.payload["task"]["_id"] == task_id
    assert response.payload["task"]["name"] == "Integration Test Task Updated"