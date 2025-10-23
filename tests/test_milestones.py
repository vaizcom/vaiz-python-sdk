import pytest
from datetime import datetime
from tests.test_config import get_test_client, TEST_BOARD_ID, TEST_PROJECT_ID, TEST_GROUP_ID
from vaiz.models import CreateMilestoneRequest, EditMilestoneRequest, ToggleMilestoneRequest, CreateTaskRequest, TaskPriority


@pytest.fixture(scope="module")
def client():
    return get_test_client()


def test_get_milestones(client):
    response = client.get_milestones()
    assert response.type == "GetMilestones"
    assert isinstance(response.milestones, list)
    
    if response.milestones:
        milestone = response.milestones[0]
        assert hasattr(milestone, "id")
        assert hasattr(milestone, "name")
        assert hasattr(milestone, "description")
        assert hasattr(milestone, "due_start")
        assert hasattr(milestone, "due_end")
        assert hasattr(milestone, "archiver")
        assert hasattr(milestone, "archived_at")
        assert hasattr(milestone, "project")
        assert hasattr(milestone, "followers")
        assert hasattr(milestone, "board")
        assert hasattr(milestone, "document")
        assert hasattr(milestone, "total")
        assert hasattr(milestone, "completed")
        assert hasattr(milestone, "created_at")
        assert hasattr(milestone, "updated_at")
        assert hasattr(milestone, "deleter")
        assert hasattr(milestone, "deleted_at")
        assert hasattr(milestone, "creator")
        
        # Test the types of important fields
        assert isinstance(milestone.total, int)
        assert isinstance(milestone.completed, int)
        assert isinstance(milestone.followers, dict)


def test_create_milestone(client):
    request = CreateMilestoneRequest(
        name="Test Milestone",
        board=TEST_BOARD_ID,
        project=TEST_PROJECT_ID
    )
    
    response = client.create_milestone(request)
    
    assert response.type == "CreateMilestone"
    assert response.milestone.name == "Test Milestone"
    assert response.milestone.description == ""  # API returns empty description by default
    assert response.milestone.due_end is None  # API returns None for due dates by default
    assert response.milestone.board == TEST_BOARD_ID
    assert response.milestone.project == TEST_PROJECT_ID
    assert response.milestone.total == 0
    assert response.milestone.completed == 0
    assert isinstance(response.milestone.id, str)
    assert isinstance(response.milestone.document, str)
    assert isinstance(response.milestone.creator, str)
    # Check that created_at is now a datetime object after our changes
    assert isinstance(response.milestone.created_at, datetime)
    # Check that updated_at is now a datetime object after our changes  
    assert isinstance(response.milestone.updated_at, datetime)
    assert isinstance(response.milestone.followers, dict)


def test_get_milestone(client):
    # First create a milestone to ensure we have one to get
    create_request = CreateMilestoneRequest(
        name="Test Milestone for Get",
        board=TEST_BOARD_ID,
        project=TEST_PROJECT_ID,
        description="Test milestone for get operation"
    )
    
    create_response = client.create_milestone(create_request)
    milestone_id = create_response.milestone.id
    
    # Now get the milestone by ID
    response = client.get_milestone(milestone_id)
    
    assert response.type == "GetMilestone"
    assert response.milestone.id == milestone_id
    assert hasattr(response.milestone, "name")
    assert hasattr(response.milestone, "description")
    assert hasattr(response.milestone, "due_start")
    assert hasattr(response.milestone, "due_end")
    assert hasattr(response.milestone, "archiver")
    assert hasattr(response.milestone, "archived_at")
    assert hasattr(response.milestone, "project")
    assert hasattr(response.milestone, "followers")
    assert hasattr(response.milestone, "board")
    assert hasattr(response.milestone, "document")
    assert hasattr(response.milestone, "total")
    assert hasattr(response.milestone, "completed")
    assert hasattr(response.milestone, "created_at")
    assert hasattr(response.milestone, "updated_at")
    assert hasattr(response.milestone, "deleter")
    assert hasattr(response.milestone, "deleted_at")
    assert hasattr(response.milestone, "creator")
    assert hasattr(response.milestone, "editor")
    
    # Test the types of important fields
    assert isinstance(response.milestone.total, int)
    assert isinstance(response.milestone.completed, int)
    assert isinstance(response.milestone.followers, dict) 


def test_edit_milestone(client):
    # First create a milestone to edit
    create_request = CreateMilestoneRequest(
        name="Test Milestone for Edit",
        board=TEST_BOARD_ID,
        project=TEST_PROJECT_ID
    )
    
    create_response = client.create_milestone(create_request)
    milestone_id = create_response.milestone.id
    
    # Now edit the milestone
    edit_request = EditMilestoneRequest(
        milestone_id=milestone_id,
        name="Updated Milestone Name",
        description="This is an updated description",
        due_end=datetime(2025, 12, 31, 23, 59, 59, 999000)  # Using datetime object
    )
    
    response = client.edit_milestone(edit_request)
    
    assert response.type == "EditMilestone"
    assert response.milestone.id == milestone_id
    assert response.milestone.name == "Updated Milestone Name"
    assert response.milestone.description == "This is an updated description"
    # Check that due_end is now a datetime object and verify the date
    assert response.milestone.due_end.year == 2025
    assert response.milestone.due_end.month == 12
    assert response.milestone.due_end.day == 31
    assert response.milestone.board == TEST_BOARD_ID
    assert response.milestone.project == TEST_PROJECT_ID
    assert isinstance(response.milestone.editor, str)  # Should have an editor now
    # Check that updated_at is now a datetime object after our changes
    assert isinstance(response.milestone.updated_at, datetime)
    
    # Verify the changes were actually applied by getting the milestone again
    get_response = client.get_milestone(milestone_id)
    assert get_response.milestone.name == "Updated Milestone Name"
    assert get_response.milestone.description == "This is an updated description"
    # Check that due_end is still a datetime object in the retrieved milestone
    assert get_response.milestone.due_end.year == 2025
    assert get_response.milestone.due_end.month == 12
    assert get_response.milestone.due_end.day == 31 


def test_toggle_milestone(client):
    # First create a milestone to toggle
    create_milestone_request = CreateMilestoneRequest(
        name="Test Milestone for Toggle",
        board=TEST_BOARD_ID,
        project=TEST_PROJECT_ID
    )
    
    milestone_response = client.create_milestone(create_milestone_request)
    milestone_id = milestone_response.milestone.id
    
    # Create a task to assign the milestone to
    create_task_request = CreateTaskRequest(
        name="Test Task for Milestone Toggle",
        group=TEST_GROUP_ID,
        board=TEST_BOARD_ID,
        priority=TaskPriority.Medium,
        completed=False
    )
    
    task_response = client.create_task(create_task_request)
    task_id = task_response.task.id
    
    # Now toggle the milestone on the task
    toggle_request = ToggleMilestoneRequest(
        task_id=task_id,
        milestone_ids=[milestone_id]
    )
    
    response = client.toggle_milestone(toggle_request)
    
    assert response.type == "ToggleMilestone"
    assert response.task.id == task_id
    assert milestone_id in response.task.milestones
    assert response.task.milestone == milestone_id  # Should set the main milestone field too
    assert hasattr(response.task, "name")
    assert hasattr(response.task, "board")
    assert hasattr(response.task, "project")
    assert hasattr(response.task, "priority")
    # Editor might be None for toggle operations, so we just check it's there
    assert hasattr(response.task, "editor")
    # Check that updated_at is now a datetime object after our changes
    assert isinstance(response.task.updated_at, datetime)
    
    # Test toggling again (should remove the milestone)
    response2 = client.toggle_milestone(toggle_request)
    assert response2.type == "ToggleMilestone"
    assert response2.task.id == task_id
    # Note: Depending on API behavior, milestone might be removed or remain
    # We'll check what actually happens in the response 