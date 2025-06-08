import pytest
from examples.config import get_client, BOARD_ID, GROUP_ID, PROJECT_ID, ASSIGNEE_ID
from vaiz.models import CreateTaskRequest, EditTaskRequest, TaskPriority

@pytest.fixture(scope="module")
def client():
    return get_client()

@pytest.fixture(scope="module")
def task_id(client):
    task = CreateTaskRequest(
        name="Integration Test Task",
        group=GROUP_ID,
        board=BOARD_ID,
        project=PROJECT_ID,
        priority=TaskPriority.High,
        completed=False,
        types=["649bea169d17e4070e0337fa"],
        assignees=[ASSIGNEE_ID],
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
        assignees=[ASSIGNEE_ID]
    )
    response = client.edit_task(edit_task)
    assert response.type == "EditTask"
    assert response.payload["task"]["name"] == "Integration Test Task Updated"

def test_get_task(client, task_id):
    response = client.get_task(task_id)
    assert response.type == "GetTask"
    assert response.payload["task"]["_id"] == task_id
    assert response.payload["task"]["name"] == "Integration Test Task Updated"