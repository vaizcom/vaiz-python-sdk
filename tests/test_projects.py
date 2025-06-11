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


def test_get_project(client):
    # First get all projects to have a valid project ID
    projects_response = client.get_projects()
    assert projects_response.projects, "No projects available for testing"
    
    project_id = projects_response.projects[0].id
    response = client.get_project(project_id)
    
    assert response.type == "GetProject"
    assert response.project.id == project_id
    assert hasattr(response.project, "name")
    assert hasattr(response.project, "color")
    assert hasattr(response.project, "slug")
    assert hasattr(response.project, "icon")
    assert hasattr(response.project, "creator")
    assert hasattr(response.project, "space")
    assert hasattr(response.project, "created_at")
    assert hasattr(response.project, "updated_at") 