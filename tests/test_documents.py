import pytest

from vaiz.models import GetDocumentRequest
from tests.test_config import get_test_client


@pytest.fixture(scope="module")
def client():
    return get_test_client()


def test_get_document_request_model_serialization():
    request = GetDocumentRequest(document_id="doc123")
    data = request.model_dump()
    assert data == {"documentId": "doc123"}


def test_get_document_fetches_json(client):
    # Create a task to get a real document id
    from vaiz.models import CreateTaskRequest, TaskPriority
    from tests.test_config import TEST_BOARD_ID, TEST_GROUP_ID, TEST_PROJECT_ID

    task = CreateTaskRequest(
        name="SDK Test - GetDocument",
        group=TEST_GROUP_ID,
        board=TEST_BOARD_ID,
        project=TEST_PROJECT_ID,
        priority=TaskPriority.General,
        completed=False,
    )
    task_response = client.create_task(task)
    document_id = task_response.task.document

    doc = client.get_document_body(document_id)

    # API may return an empty document for newly created tasks
    assert isinstance(doc, dict)


