import pytest
from tests.test_config import get_test_client, TEST_BOARD_ID, TEST_GROUP_ID, TEST_PROJECT_ID
from vaiz.models import CreateTaskRequest, TaskPriority, TaskFile
from vaiz.models.enums import EUploadFileType

@pytest.fixture(scope="module")
def client():
    return get_test_client()

def test_create_task_with_description():
    """Test creating a task with description."""
    client = get_test_client()
    
    task = CreateTaskRequest(
        name="Test Task with Description",
        group=TEST_GROUP_ID,
        board=TEST_BOARD_ID,
        project=TEST_PROJECT_ID,
        priority=TaskPriority.Medium,
        completed=False,
        description="This is a test task with a description."
    )
    
    response = client.create_task(task)
    
    assert response.type == "CreateTask"
    assert response.payload["task"]["name"] == "Test Task with Description"
    # API accepts description but doesn't return it in response
    # Description is stored in a separate document referenced by 'document' field
    assert "document" in response.payload["task"]
    assert response.payload["task"]["document"] is not None

def test_create_task_with_mock_files():
    """Test creating a task with mock files."""
    client = get_test_client()
    
    # Create mock file data
    mock_file = TaskFile(
        url="http://example.com/test.pdf",
        name="test.pdf",
        dimension=[0, 0],
        ext="pdf",
        _id="mock_file_id_123",
        type=EUploadFileType.Pdf
    )
    
    task = CreateTaskRequest(
        name="Test Task with Files",
        group=TEST_GROUP_ID,
        board=TEST_BOARD_ID,
        project=TEST_PROJECT_ID,
        priority=TaskPriority.High,
        completed=False,
        description="This task includes mock files for testing.",
        files=[mock_file]
    )
    
    response = client.create_task(task)
    
    assert response.type == "CreateTask"
    assert response.payload["task"]["name"] == "Test Task with Files"
    # API accepts files but doesn't return them in response
    # Files are stored but not included in the task response
    assert "document" in response.payload["task"]
    assert response.payload["task"]["document"] is not None

def test_create_task_with_description_and_files():
    """Test creating a task with both description and files."""
    client = get_test_client()
    
    # Create mock file data
    mock_file = TaskFile(
        url="http://example.com/document.pdf",
        name="document.pdf",
        dimension=[0, 0],
        ext="pdf",
        _id="mock_file_id_456",
        type=EUploadFileType.Pdf
    )
    
    task = CreateTaskRequest(
        name="Test Task with Description and Files",
        group=TEST_GROUP_ID,
        board=TEST_BOARD_ID,
        project=TEST_PROJECT_ID,
        priority=TaskPriority.Low,
        completed=False,
        description="This task has both a description and attached files.",
        files=[mock_file]
    )
    
    response = client.create_task(task)
    assert response.type == "CreateTask"
    assert response.payload["task"]["name"] == "Test Task with Description and Files"
    # API accepts both description and files but doesn't return them in response
    assert "document" in response.payload["task"]
    assert response.payload["task"]["document"] is not None

def test_task_has_document_field():
    """Test that created tasks have a document field (which contains document ID)."""
    client = get_test_client()
    
    task = CreateTaskRequest(
        name="Test Task Document Field",
        group=TEST_GROUP_ID,
        board=TEST_BOARD_ID,
        project=TEST_PROJECT_ID,
        priority=TaskPriority.General,
        completed=False
    )
    
    response = client.create_task(task)
    assert response.type == "CreateTask"
    assert "document" in response.payload["task"]
    assert response.payload["task"]["document"] is not None
    # Document field contains an ID, not the actual document content
    assert isinstance(response.payload["task"]["document"], str) 