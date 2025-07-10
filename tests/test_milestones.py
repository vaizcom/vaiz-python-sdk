import pytest
from tests.test_config import get_test_client, TEST_BOARD_ID, TEST_PROJECT_ID
from vaiz.models import CreateMilestoneRequest


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
    assert isinstance(response.milestone.created_at, str)
    assert isinstance(response.milestone.updated_at, str)
    assert isinstance(response.milestone.followers, dict) 