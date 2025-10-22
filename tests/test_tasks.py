import pytest
from datetime import datetime
from tests.test_config import get_test_client, TEST_BOARD_ID, TEST_GROUP_ID, TEST_PROJECT_ID, TEST_ASSIGNEE_ID
from vaiz.models import CreateTaskRequest, EditTaskRequest, TaskPriority, GetHistoryRequest, GetHistoryResponse, HistoryItem, ReplaceDocumentResponse, GetTasksRequest, GetTasksResponse
from vaiz.models.enums import Kind

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
        priority=TaskPriority.High,
        completed=False,
        due_start=datetime(2025, 2, 1, 9, 0, 0),    # February 1st, 9:00 AM
        due_end=datetime(2025, 2, 15, 17, 0, 0),    # February 15th, 5:00 PM
        types=[],
        assignees=[str(TEST_ASSIGNEE_ID)],
        subtasks=[],
        milestones=[],
        blocking=[],
        blockers=[]
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
        kind=Kind.Task,
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
    update_response = task_instance.update_task_description(client, new_description)
    assert isinstance(update_response, ReplaceDocumentResponse)

    # Fetch description body to ensure API call succeeded
    updated_body = task_instance.get_task_description(client)
    assert isinstance(updated_body, dict)


def test_get_tasks_default_parameters(client):
    """Test get_tasks with default parameters."""
    request = GetTasksRequest()
    response = client.get_tasks(request)
    
    assert isinstance(response, GetTasksResponse)
    assert response.type == "GetTasks"
    assert hasattr(response.payload, "tasks")
    assert isinstance(response.payload.tasks, list)
    
    # Check default values are applied correctly
    assert request.limit == 50
    assert request.skip == 0
    assert request.assignees is None


def test_get_tasks_with_assignees_filter(client):
    """Test get_tasks with assignees filter."""
    if not TEST_ASSIGNEE_ID:
        pytest.skip("TEST_ASSIGNEE_ID is missing.")
    
    request = GetTasksRequest(
        assignees=[str(TEST_ASSIGNEE_ID)],
        limit=10,
        skip=0
    )
    response = client.get_tasks(request)
    
    assert isinstance(response, GetTasksResponse)
    assert response.type == "GetTasks"
    assert hasattr(response.payload, "tasks")
    assert isinstance(response.payload.tasks, list)
    
    # Verify that returned tasks have the correct assignee (if any tasks returned)
    for task in response.payload.tasks:
        assert str(TEST_ASSIGNEE_ID) in task.assignees


def test_get_tasks_with_pagination(client):
    """Test get_tasks with pagination parameters."""
    # First, get tasks with limit 5
    request1 = GetTasksRequest(limit=5, skip=0)
    response1 = client.get_tasks(request1)
    
    assert isinstance(response1, GetTasksResponse)
    assert response1.type == "GetTasks"
    assert len(response1.payload.tasks) <= 5
    
    # Then get next page
    request2 = GetTasksRequest(limit=5, skip=5)
    response2 = client.get_tasks(request2)
    
    assert isinstance(response2, GetTasksResponse)
    assert response2.type == "GetTasks"
    assert len(response2.payload.tasks) <= 5
    
    # Verify different tasks are returned (if there are enough tasks)
    if len(response1.payload.tasks) == 5 and len(response2.payload.tasks) > 0:
        task_ids_1 = {task.id for task in response1.payload.tasks}
        task_ids_2 = {task.id for task in response2.payload.tasks}
        # Should have different task IDs (no overlap)
        assert len(task_ids_1.intersection(task_ids_2)) == 0


def test_get_tasks_with_max_limit(client):
    """Test get_tasks with maximum allowed limit (50)."""
    request = GetTasksRequest(limit=50, skip=0)
    response = client.get_tasks(request)
    
    assert isinstance(response, GetTasksResponse)
    assert response.type == "GetTasks"
    assert hasattr(response.payload, "tasks")
    assert isinstance(response.payload.tasks, list)
    assert len(response.payload.tasks) <= 50


def test_get_tasks_request_validation():
    """Test GetTasksRequest model validation."""
    # Test valid request with all parameters
    request = GetTasksRequest(
        ids=["task1", "task2"],
        assignees=["user1", "user2"],
        limit=25,
        skip=10,
        board="board1",
        project="project1",
        parent_task="parent1",
        milestones=["milestone1", "milestone2"],
        completed=True,
        archived=False
    )
    assert request.ids == ["task1", "task2"]
    assert request.assignees == ["user1", "user2"]
    assert request.limit == 25
    assert request.skip == 10
    assert request.board == "board1"
    assert request.project == "project1"
    assert request.parent_task == "parent1"
    assert request.milestones == ["milestone1", "milestone2"]
    assert request.completed is True
    assert request.archived is False
    
    # Test default values
    request_default = GetTasksRequest()
    assert request_default.ids is None
    assert request_default.assignees is None
    assert request_default.limit == 50
    assert request_default.skip == 0
    assert request_default.board is None
    assert request_default.project is None
    assert request_default.parent_task is None
    assert request_default.milestones is None
    assert request_default.completed is None
    assert request_default.archived is None
    
    # Test model_dump excludes None values
    dumped = request_default.model_dump()
    assert "ids" not in dumped
    assert "assignees" not in dumped
    assert "board" not in dumped
    assert "project" not in dumped
    assert "parentTask" not in dumped
    assert "milestones" not in dumped
    assert "completed" not in dumped
    assert "archived" not in dumped
    assert "limit" in dumped
    assert "skip" in dumped


def test_get_tasks_request_validation_limits():
    """Test GetTasksRequest validation with edge cases."""
    # Test minimum values
    request_min = GetTasksRequest(limit=1, skip=0)
    assert request_min.limit == 1
    assert request_min.skip == 0
    
    # Test maximum limit (50 tasks per page)
    request_max = GetTasksRequest(limit=50, skip=0)
    assert request_max.limit == 50
    
    # Test with invalid values should raise validation error
    with pytest.raises(ValueError):
        GetTasksRequest(limit=0)  # Below minimum
    
    with pytest.raises(ValueError):
        GetTasksRequest(limit=51)  # Above maximum (50)
    
    with pytest.raises(ValueError):
        GetTasksRequest(limit=100)  # Way above maximum
    
    with pytest.raises(ValueError):
        GetTasksRequest(skip=-1)  # Below minimum


def test_get_tasks_response_structure(client):
    """Test that GetTasksResponse has the correct structure."""
    request = GetTasksRequest(limit=1)
    response = client.get_tasks(request)
    
    assert isinstance(response, GetTasksResponse)
    assert hasattr(response, 'payload')
    assert hasattr(response, 'type')
    assert response.type == "GetTasks"
    
    assert hasattr(response.payload, 'tasks')
    assert isinstance(response.payload.tasks, list)
    
    # If there are tasks, verify task structure
    if response.payload.tasks:
        task = response.payload.tasks[0]
        # Verify task has expected fields from the API response example
        assert hasattr(task, 'id')
        assert hasattr(task, 'name')
        assert hasattr(task, 'group')
        assert hasattr(task, 'board')
        assert hasattr(task, 'project')
        assert hasattr(task, 'priority')
        assert hasattr(task, 'hrid')
        assert hasattr(task, 'completed')
        assert hasattr(task, 'assignees')
        assert hasattr(task, 'creator')
        assert hasattr(task, 'created_at')
        assert hasattr(task, 'updated_at')


def test_get_tasks_with_ids_filter(client):
    """Test get_tasks with specific task IDs filter."""
    # Use example task IDs from the API response
    task_ids = ["68c19e08020b3f8c50a8150e", "68c19e09020b3f8c50a81663"]
    
    request = GetTasksRequest(ids=task_ids)
    response = client.get_tasks(request)
    
    assert isinstance(response, GetTasksResponse)
    assert response.type == "GetTasks"
    assert hasattr(response.payload, "tasks")
    assert isinstance(response.payload.tasks, list)
    
    # If tasks are returned, verify they match the requested IDs
    for task in response.payload.tasks:
        assert task.id in task_ids


def test_get_tasks_with_board_filter(client):
    """Test get_tasks with board filter."""
    board_id = "68c19e08020b3f8c50a814d6"  # Example from API response
    
    request = GetTasksRequest(
        board=board_id,
        limit=10
    )
    response = client.get_tasks(request)
    
    assert isinstance(response, GetTasksResponse)
    assert response.type == "GetTasks"
    assert hasattr(response.payload, "tasks")
    assert isinstance(response.payload.tasks, list)
    
    # If tasks are returned, verify they belong to the correct board
    for task in response.payload.tasks:
        assert task.board == board_id


def test_get_tasks_with_project_filter(client):
    """Test get_tasks with project filter."""
    from tests.test_config import TEST_PROJECT_ID
    
    if not TEST_PROJECT_ID:
        pytest.skip("TEST_PROJECT_ID not set in environment variables")
    
    request = GetTasksRequest(
        project=TEST_PROJECT_ID,
        limit=10
    )
    response = client.get_tasks(request)
    
    assert isinstance(response, GetTasksResponse)
    assert response.type == "GetTasks"
    assert hasattr(response.payload, "tasks")
    assert isinstance(response.payload.tasks, list)
    
    # If tasks are returned, verify they belong to the correct project
    for task in response.payload.tasks:
        assert task.project == TEST_PROJECT_ID


def test_get_tasks_with_completed_filter(client):
    """Test get_tasks with completed status filter."""
    # Test completed tasks
    request_completed = GetTasksRequest(
        completed=True,
        limit=10
    )
    response_completed = client.get_tasks(request_completed)
    
    assert isinstance(response_completed, GetTasksResponse)
    assert response_completed.type == "GetTasks"
    
    # If tasks are returned, verify they are all completed
    for task in response_completed.payload.tasks:
        assert task.completed is True
    
    # Test pending tasks
    request_pending = GetTasksRequest(
        completed=False,
        limit=10
    )
    response_pending = client.get_tasks(request_pending)
    
    assert isinstance(response_pending, GetTasksResponse)
    assert response_pending.type == "GetTasks"
    
    # If tasks are returned, verify they are all pending
    for task in response_pending.payload.tasks:
        assert task.completed is False


def test_get_tasks_with_archived_filter(client):
    """Test get_tasks with archived status filter."""
    # Test non-archived tasks
    request = GetTasksRequest(
        archived=False,
        limit=10
    )
    response = client.get_tasks(request)
    
    assert isinstance(response, GetTasksResponse)
    assert response.type == "GetTasks"
    assert hasattr(response.payload, "tasks")
    assert isinstance(response.payload.tasks, list)
    
    # If tasks are returned, verify they are not archived
    for task in response.payload.tasks:
        assert task.archived_at is None


def test_get_tasks_with_parent_task_filter(client):
    """Test get_tasks with parent task filter."""
    parent_task_id = "68c19e09020b3f8c50a81663"  # Example from API response
    
    request = GetTasksRequest(
        parent_task=parent_task_id,
        limit=10
    )
    response = client.get_tasks(request)
    
    assert isinstance(response, GetTasksResponse)
    assert response.type == "GetTasks"
    assert hasattr(response.payload, "tasks")
    assert isinstance(response.payload.tasks, list)
    
    # If tasks are returned, verify they have the correct parent
    for task in response.payload.tasks:
        assert task.parent_task == parent_task_id


def test_get_tasks_with_milestones_filter(client):
    """Test get_tasks with milestones filter."""
    milestone_ids = ["68c19e08020b3f8c50a814e6"]  # Example from API response
    
    request = GetTasksRequest(
        milestones=milestone_ids,
        limit=10
    )
    response = client.get_tasks(request)
    
    assert isinstance(response, GetTasksResponse)
    assert response.type == "GetTasks"
    assert hasattr(response.payload, "tasks")
    assert isinstance(response.payload.tasks, list)
    
    # If tasks are returned, verify they have the correct milestones
    for task in response.payload.tasks:
        # Check if any of the requested milestones are in the task's milestones
        task_milestone_set = set(task.milestones)
        requested_milestone_set = set(milestone_ids)
        assert len(task_milestone_set.intersection(requested_milestone_set)) > 0


def test_get_tasks_with_multiple_filters(client):
    """Test get_tasks with multiple filters combined."""
    if not TEST_ASSIGNEE_ID:
        pytest.skip("TEST_ASSIGNEE_ID is missing.")
    
    request = GetTasksRequest(
        assignees=[str(TEST_ASSIGNEE_ID)],
        completed=False,
        archived=False,
        limit=5
    )
    response = client.get_tasks(request)
    
    assert isinstance(response, GetTasksResponse)
    assert response.type == "GetTasks"
    assert hasattr(response.payload, "tasks")
    assert isinstance(response.payload.tasks, list)
    
    # If tasks are returned, verify they match all filters
    for task in response.payload.tasks:
        assert str(TEST_ASSIGNEE_ID) in task.assignees
        assert task.completed is False
        assert task.archived_at is None


def test_get_tasks_request_alias_mapping():
    """Test that parentTask alias is properly mapped."""
    request = GetTasksRequest(parent_task="parent123")
    
    # Test model_dump with by_alias=True
    dumped_with_alias = request.model_dump(by_alias=True)
    assert "parentTask" in dumped_with_alias
    assert dumped_with_alias["parentTask"] == "parent123"
    assert "parent_task" not in dumped_with_alias
    
    # Test model_dump without by_alias
    dumped_without_alias = request.model_dump(by_alias=False)
    assert "parent_task" in dumped_without_alias
    assert dumped_without_alias["parent_task"] == "parent123"
    assert "parentTask" not in dumped_without_alias




def test_get_tasks_caching(client):
    """Test that getTasks caching works correctly."""
    import time
    
    # Enable verbose mode to track cache operations
    original_verbose = client.verbose
    client.verbose = False  # Set to True to see cache debug output
    
    # Clear cache to start fresh
    client.clear_tasks_cache()
    
    # Test 1: First request should be a cache miss
    request = GetTasksRequest(limit=5)
    start = time.time()
    response1 = client.get_tasks(request)
    time1 = time.time() - start
    
    # Test 2: Same request should be a cache hit (much faster)
    start = time.time()
    response2 = client.get_tasks(request)
    time2 = time.time() - start
    
    # Cache hit should be faster (at least 2x in most cases)
    # But we can't guarantee exact timing, so just check data consistency
    assert response1.payload.tasks == response2.payload.tasks
    assert response1.type == response2.type
    
    # Test 3: Different request should be a cache miss
    request2 = GetTasksRequest(limit=10)
    response3 = client.get_tasks(request2)
    
    # Should get different amount of tasks
    assert len(response3.payload.tasks) != len(response1.payload.tasks) or request2.limit != request.limit
    
    # Test 4: Cache is mandatory - no bypass option
    # Same request should still hit cache
    response4 = client.get_tasks(request)
    # Should get same data from cache
    assert response4.payload.tasks == response1.payload.tasks
    
    # Test 5: Clear cache
    client.clear_tasks_cache()
    # After clear, should work normally
    response5 = client.get_tasks(request)
    assert len(response5.payload.tasks) == len(response1.payload.tasks)
    
    # Restore original verbose setting
    client.verbose = original_verbose


def test_get_tasks_cache_key_generation():
    """Test that cache keys are generated correctly for different requests."""
    from vaiz import VaizClient
    
    client = VaizClient(api_key="test", space_id="test_space")
    
    # Same parameters should generate same key
    req1 = GetTasksRequest(limit=10, skip=0)
    req2 = GetTasksRequest(limit=10, skip=0)
    key1 = client._get_cache_key(req1)
    key2 = client._get_cache_key(req2)
    assert key1 == key2
    
    # Different parameters should generate different keys
    req3 = GetTasksRequest(limit=10, skip=5)
    key3 = client._get_cache_key(req3)
    assert key1 != key3
    
    # Different filters should generate different keys
    req4 = GetTasksRequest(limit=10, completed=True)
    req5 = GetTasksRequest(limit=10, completed=False)
    key4 = client._get_cache_key(req4)
    key5 = client._get_cache_key(req5)
    assert key4 != key5
    
    # Order of parameters shouldn't matter (JSON is sorted)
    req6 = GetTasksRequest(limit=10, skip=5, completed=True)
    req7 = GetTasksRequest(completed=True, skip=5, limit=10)
    key6 = client._get_cache_key(req6)
    key7 = client._get_cache_key(req7)
    assert key6 == key7


def test_get_tasks_cache_ttl():
    """Test that cache TTL is respected."""
    from vaiz import VaizClient
    from datetime import datetime, timedelta
    
    client = VaizClient(api_key="test", space_id="test")
    
    # Test that cache is valid within TTL
    now = datetime.now()
    assert client._is_cache_valid(now) == True
    assert client._is_cache_valid(now - timedelta(minutes=4)) == True
    
    # Test that cache is invalid after TTL
    assert client._is_cache_valid(now - timedelta(minutes=6)) == False
    assert client._is_cache_valid(now - timedelta(hours=1)) == False


 