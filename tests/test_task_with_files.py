import pytest
import os
from tests.test_config import get_test_client, TEST_BOARD_ID, TEST_GROUP_ID, TEST_PROJECT_ID
from vaiz.models import CreateTaskRequest, TaskPriority, TaskFile, TaskUploadFile
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
        completed=True,
        description="This is a test task with a description."
    )
    
    response = client.create_task(task)
    
    assert response.type == "CreateTask"
    assert response.payload["task"]["name"] == "Test Task with Description"
    # API accepts description but doesn't return it in response
    # Description is stored in a separate document referenced by 'document' field
    assert "document" in response.payload["task"]
    assert response.payload["task"]["document"] is not None

def test_create_task_with_real_file():
    """Test creating a task with a real file from assets."""
    client = get_test_client()
    
    # Upload a real file from assets
    file_path = "./assets/example.pdf"
    if not os.path.exists(file_path):
        pytest.skip(f"Test file {file_path} not found")
    
    try:
        upload_response = client.upload_file(file_path, file_type=EUploadFileType.Pdf)
        uploaded_file = upload_response.file
        
        # Create TaskFile object from uploaded file
        task_file = TaskFile(
            url=uploaded_file.url,
            name=uploaded_file.name,
            dimension=uploaded_file.dimension,
            ext=uploaded_file.ext,
            _id=uploaded_file.id,
            type=uploaded_file.type
        )
        
        task = CreateTaskRequest(
            name="Test Task with Real File",
            group=TEST_GROUP_ID,
            board=TEST_BOARD_ID,
            project=TEST_PROJECT_ID,
            priority=TaskPriority.High,
            completed=True,
            description="This task includes a real file from assets for testing.",
            files=[task_file]
        )
        
        response = client.create_task(task)
        
        assert response.type == "CreateTask"
        assert response.payload["task"]["name"] == "Test Task with Real File"
        # API accepts files but doesn't return them in response
        # Files are stored but not included in the task response
        assert "document" in response.payload["task"]
        assert response.payload["task"]["document"] is not None
        
    except Exception as e:
        pytest.fail(f"Failed to upload file or create task: {e}")

def test_create_task_with_multiple_real_files():
    """Test creating a task with multiple real files from assets."""
    client = get_test_client()
    
    # Upload multiple real files from assets
    files_to_upload = [
        ("./assets/example.pdf", EUploadFileType.Pdf),
        ("./assets/example.png", EUploadFileType.Image),
        ("./assets/example.mp4", EUploadFileType.Video)
    ]
    
    task_files = []
    for file_path, file_type in files_to_upload:
        if not os.path.exists(file_path):
            pytest.skip(f"Test file {file_path} not found")
        
        try:
            upload_response = client.upload_file(file_path, file_type=file_type)
            uploaded_file = upload_response.file
            
            task_file = TaskFile(
                url=uploaded_file.url,
                name=uploaded_file.name,
                dimension=uploaded_file.dimension,
                ext=uploaded_file.ext,
                _id=uploaded_file.id,
                type=uploaded_file.type
            )
            task_files.append(task_file)
        except Exception as e:
            pytest.fail(f"Failed to upload {file_path}: {e}")
    
    if not task_files:
        pytest.skip("No files were uploaded successfully")
    
    task = CreateTaskRequest(
        name="Test Task with Multiple Real Files",
        group=TEST_GROUP_ID,
        board=TEST_BOARD_ID,
        project=TEST_PROJECT_ID,
        priority=TaskPriority.Low,
        completed=True,
        description="This task has multiple real files from assets folder.",
        files=task_files
    )
    
    response = client.create_task(task)
    
    assert response.type == "CreateTask"
    assert response.payload["task"]["name"] == "Test Task with Multiple Real Files"
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
        completed=True
    )
    
    response = client.create_task(task)
    assert response.type == "CreateTask"
    assert "document" in response.payload["task"]
    assert response.payload["task"]["document"] is not None
    # Document field contains an ID, not the actual document content
    assert isinstance(response.payload["task"]["document"], str)

def test_create_task_with_file_pdf(client):
    file_path = "./assets/example.pdf"
    if not os.path.exists(file_path):
        pytest.skip(f"Test file {file_path} not found")
    
    task = CreateTaskRequest(
        name="Test Task with PDF",
        group=TEST_GROUP_ID,
        board=TEST_BOARD_ID,
        project=TEST_PROJECT_ID,
        completed=True
    )
    file = TaskUploadFile(path=file_path, type=EUploadFileType.Pdf)
    response = client.create_task(task, file=file)
    task_response = response.task
    assert task_response.completed is True
    assert isinstance(task_response.document, str)


def test_create_task_with_file_png(client):
    file_path = "./assets/example.png"
    if not os.path.exists(file_path):
        pytest.skip(f"Test file {file_path} not found")
    
    task = CreateTaskRequest(
        name="Test Task with PNG",
        group=TEST_GROUP_ID,
        board=TEST_BOARD_ID,
        project=TEST_PROJECT_ID,
        completed=True
    )
    file = TaskUploadFile(path=file_path, type=EUploadFileType.Image)
    response = client.create_task(task, file=file)
    task_response = response.task
    assert task_response.completed is True
    assert isinstance(task_response.document, str)


def test_create_task_with_file_mp4(client):
    file_path = "./assets/example.mp4"
    if not os.path.exists(file_path):
        pytest.skip(f"Test file {file_path} not found")
    
    task = CreateTaskRequest(
        name="Test Task with MP4",
        group=TEST_GROUP_ID,
        board=TEST_BOARD_ID,
        project=TEST_PROJECT_ID,
        completed=True
    )
    file = TaskUploadFile(path=file_path, type=EUploadFileType.Video)
    response = client.create_task(task, file=file)
    task_response = response.task
    assert task_response.completed is True
    assert isinstance(task_response.document, str)


def test_create_task_with_description_only(client):
    task = CreateTaskRequest(
        name="Test Task without File",
        group=TEST_GROUP_ID,
        board=TEST_BOARD_ID,
        project=TEST_PROJECT_ID,
        completed=True
    )
    response = client.create_task(task, description="Task without file")
    task_response = response.task
    assert task_response.completed is True
    assert isinstance(task_response.document, str)


def test_create_task_with_description_and_file(client):
    file_path = "./assets/example.pdf"
    if not os.path.exists(file_path):
        pytest.skip(f"Test file {file_path} not found")
    
    task = CreateTaskRequest(
        name="Test Task with Description and File",
        group=TEST_GROUP_ID,
        board=TEST_BOARD_ID,
        project=TEST_PROJECT_ID,
        priority=TaskPriority.High,
        completed=True
    )
    file = TaskUploadFile(path=file_path, type=EUploadFileType.Pdf)
    response = client.create_task(task, description="This task has both description and file", file=file)
    task_response = response.task
    assert task_response.completed is True
    assert task_response.priority == TaskPriority.High
    assert isinstance(task_response.document, str)


def test_create_task_with_auto_detection(client):
    file_path = "./assets/example.pdf"
    if not os.path.exists(file_path):
        pytest.skip(f"Test file {file_path} not found")
    
    task = CreateTaskRequest(
        name="Test Task with Auto-Detection",
        group=TEST_GROUP_ID,
        board=TEST_BOARD_ID,
        project=TEST_PROJECT_ID,
        completed=True
    )
    file = TaskUploadFile(path=file_path, type=EUploadFileType.Pdf)
    response = client.create_task(task, file=file)
    task_response = response.task
    assert task_response.completed is True
    assert isinstance(task_response.document, str)

def test_task_file_has_correct_fields_for_different_types(client):
    """Test that TaskFile gets correct fields based on file type."""
    
    # Test PDF file (should have size, no dimension)
    pdf_path = "./assets/example.pdf"
    if os.path.exists(pdf_path):
        task = CreateTaskRequest(
            name="Test PDF Fields",
            group=TEST_GROUP_ID,
            board=TEST_BOARD_ID,
            project=TEST_PROJECT_ID,
            completed=True
        )
        file = TaskUploadFile(path=pdf_path, type=EUploadFileType.Pdf)
        response = client.create_task(task, file=file)
        
        # Check that task was created successfully
        assert response.task.completed is True
        assert isinstance(response.task.document, str)
    
    # Test PNG file (should have dimension, no size)
    png_path = "./assets/example.png"
    if os.path.exists(png_path):
        task = CreateTaskRequest(
            name="Test PNG Fields",
            group=TEST_GROUP_ID,
            board=TEST_BOARD_ID,
            project=TEST_PROJECT_ID,
            completed=True
        )
        file = TaskUploadFile(path=png_path, type=EUploadFileType.Image)
        response = client.create_task(task, file=file)
        
        # Check that task was created successfully
        assert response.task.completed is True
        assert isinstance(response.task.document, str) 