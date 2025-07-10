import pytest
from tests.test_config import get_test_client


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