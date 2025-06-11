import pytest
from tests.test_config import get_test_client


@pytest.fixture(scope="module")
def client():
    return get_test_client()


def test_get_projects(client):
    response = client.get_projects()
    assert response.type == "GetProjects"
    assert isinstance(response.projects, list)
    
    if response.projects:
        project = response.projects[0]
        assert hasattr(project, "id")
        assert hasattr(project, "name")
        assert hasattr(project, "color")
        assert hasattr(project, "slug")
        assert hasattr(project, "icon")
        assert hasattr(project, "creator")
        assert hasattr(project, "space")
        assert hasattr(project, "created_at")
        assert hasattr(project, "updated_at") 