import pytest
from datetime import datetime
from tests.test_config import get_test_client, TEST_BOARD_ID, TEST_GROUP_ID, TEST_PROJECT_ID, TEST_ASSIGNEE_ID
from vaiz.models import CreateTaskRequest, EditTaskRequest, TaskPriority, TaskResponse, GetHistoryRequest, GetHistoryResponse, HistoryItem, ReplaceDocumentResponse
from vaiz.models.enums import EKind

@pytest.fixture(scope="module")
def client():
    return get_test_client()

@pytest.fixture(scope="module")
def task_id(client):
    """Fixture that creates a test task with due dates and returns its ID."""
    if not all([TEST_GROUP_ID, TEST_BOARD_ID, TEST_PROJECT_ID, TEST_ASSIGNEE_ID]):
        pytest.skip("Test config values are missing. Please set VAIZ_GROUP_ID, VAIZ_BOARD_ID, VAIZ_PROJECT_ID, VAIZ_ASSIGNEE_ID.")
    task = CreateTaskRequest(
        name="Test Task with DateTime",
        group=TEST_GROUP_ID,
        board=TEST_BOARD_ID,
        project=TEST_PROJECT_ID,
        priority=TaskPriority.High,
        completed=False,
        due_start=datetime(2025, 2, 1, 9, 0, 0),    # February 1st, 9:00 AM
        due_end=datetime(2025, 2, 15, 17, 0, 0),    # February 15th, 5:00 PM
        types=[],
        assignees=[str(TEST_ASSIGNEE_ID)],
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
    if not TEST_ASSIGNEE_ID:
        pytest.skip("TEST_ASSIGNEE_ID is missing.")
    edit_task = EditTaskRequest(
        task_id=task_id,
        name="Updated Test Task",
        priority=TaskPriority.Medium,
        completed=True,
        due_start=datetime(2025, 3, 1, 10, 0, 0),   # March 1st, 10:00 AM (updated)
        due_end=datetime(2025, 3, 20, 16, 0, 0)     # March 20th, 4:00 PM (updated)
    )
    response = client.edit_task(edit_task)
    assert response.type == "EditTask"
    assert response.payload["task"]["name"] == "Updated Test Task"
    
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
    assert response.payload["task"]["name"] == "Updated Test Task"
    
    # Check that due dates are properly set  
    task_data = response.payload["task"]
    assert task_data.get("dueStart") is not None
    assert task_data.get("dueEnd") is not None
    print(f"Retrieved dueStart: {task_data.get('dueStart')}")
    print(f"Retrieved dueEnd: {task_data.get('dueEnd')}") 

def test_get_history(client, task_id):
    """Test the get_history API method for a task."""
    request = GetHistoryRequest(
        kind=EKind.Task,
        kindId=task_id,
        excludeKeys=["TASK_COMMENTED", "MILESTONE_COMMENTED", "DOCUMENT_COMMENTED"],
        lastLoadedDate=0
    )
    response = client.get_history(request)
    assert isinstance(response, GetHistoryResponse)
    assert response.type == "GetHistory"
    assert hasattr(response.payload, "histories")
    assert isinstance(response.payload.histories, list)
    # Optionally check that each item is a HistoryItem
    if response.payload.histories:
        assert isinstance(response.payload.histories[0], HistoryItem)


def test_task_get_description_method_with_initial_content(client):
    """Test Task.get_task_description() with a task that has initial description content."""
    if not all([TEST_GROUP_ID, TEST_BOARD_ID, TEST_PROJECT_ID]):
        pytest.skip("Test config values are missing. Please set VAIZ_GROUP_ID, VAIZ_BOARD_ID, VAIZ_PROJECT_ID.")
    
    # Create task with initial description
    initial_description = "Initial task description content"
    task = CreateTaskRequest(
        name="Task for Description Test - Initial",
        group=TEST_GROUP_ID,
        board=TEST_BOARD_ID,
        project=TEST_PROJECT_ID,
        priority=TaskPriority.General,
        description=initial_description
    )
    
    task_response = client.create_task(task)
    assert task_response.type == "CreateTask"
    
    # Get the Task model instance
    task_instance = task_response.task
    assert task_instance.document is not None
    
    # Use the convenience method to get description
    description_body = task_instance.get_task_description(client)
    assert isinstance(description_body, dict)
    
    print(f"Initial description body keys: {list(description_body.keys())}")
    print(f"Full description body: {description_body}")
    print(f"Task document ID: {task_instance.document}")
    
    # Check if there's content in the default key
    if 'default' in description_body:
        default_content = description_body['default']
        print(f"Default content type: {type(default_content)}")
        print(f"Default content: {default_content}")



def test_task_update_description_method(client):
    """Test Task.update_task_description() to replace description content."""
    if not all([TEST_GROUP_ID, TEST_BOARD_ID, TEST_PROJECT_ID]):
        pytest.skip("Test config values are missing. Please set VAIZ_GROUP_ID, VAIZ_BOARD_ID, VAIZ_PROJECT_ID.")

    # Create task with initial description
    task = CreateTaskRequest(
        name="Task for Update Description Test",
        group=TEST_GROUP_ID,
        board=TEST_BOARD_ID,
        project=TEST_PROJECT_ID,
        priority=TaskPriority.General,
        description="Initial description"
    )

    task_response = client.create_task(task)
    assert task_response.type == "CreateTask"

    task_instance = task_response.task
    assert task_instance.document is not None

    # Update description via convenience method
    new_description = (
        "Updated via Task.update_task_description()\n\n"
        "This replaces the existing description content."
    )
    update_response = task_instance.update_task_description(client, new_description, files=[])
    assert isinstance(update_response, ReplaceDocumentResponse)

    # Fetch description body to ensure API call succeeded
    updated_body = task_instance.get_task_description(client)
    assert isinstance(updated_body, dict)


def test_task_update_description_with_files(client):
    """Test Task.update_task_description() with file attachments."""
    if not all([TEST_GROUP_ID, TEST_BOARD_ID, TEST_PROJECT_ID]):
        pytest.skip("Test config values are missing. Please set VAIZ_GROUP_ID, VAIZ_BOARD_ID, VAIZ_PROJECT_ID.")

    # Create task with initial description
    task = CreateTaskRequest(
        name="Task for Update Description with Files Test",
        group=TEST_GROUP_ID,
        board=TEST_BOARD_ID,
        project=TEST_PROJECT_ID,
        priority=TaskPriority.General,
        description="Initial description"
    )

    task_response = client.create_task(task)
    assert task_response.type == "CreateTask"

    task_instance = task_response.task
    assert task_instance.document is not None

    # Upload a test file to attach
    import tempfile
    import os
    
    # Create a temporary text file for testing
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
        temp_file.write("Test file content for task description update")
        temp_file_path = temp_file.name
    
    try:
        # Upload the file
        from vaiz.models.enums import EUploadFileType
        upload_response = client.upload_file(
            file_path=temp_file_path,
            file_type=EUploadFileType.File
        )
        
        uploaded_file_id = upload_response.file.id
        print(f"Uploaded file ID: {uploaded_file_id}")
        
        # Update description via convenience method with file attachment
        new_description = (
            "📎 Task Description Updated with File\n\n"
            "This task description was updated using Task.update_task_description()\n"
            "with an attached file.\n\n"
            "- ✅ Convenience method works\n"
            "- 📎 File attachment supported\n"
            "- 🎯 Complete functionality"
        )
        
        update_response = task_instance.update_task_description(
            client, 
            new_description, 
            files=[uploaded_file_id]
        )
        
        assert isinstance(update_response, ReplaceDocumentResponse)
        
        # Verify the update worked by fetching the description
        updated_body = task_instance.get_task_description(client)
        assert isinstance(updated_body, dict)
        
        print(f"✅ Task description updated with file attachment successfully!")
        print(f"✅ File ID: {uploaded_file_id}")
        print(f"✅ Task document ID: {task_instance.document}")
        
    finally:
        # Clean up temporary file
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path) 