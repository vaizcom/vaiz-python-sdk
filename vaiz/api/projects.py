from vaiz.api.base import BaseAPIClient
from vaiz.models import ProjectsResponse, ProjectResponse


class ProjectsAPIClient(BaseAPIClient):
    def get_projects(self) -> ProjectsResponse:
        """
        Get all projects in the current space.
        
        Returns:
            ProjectsResponse: The list of projects
        """
        response_data = self._make_request("getProjects", method="POST", json_data={})
        return ProjectsResponse(**response_data)

    def get_project(self, project_id: str) -> ProjectResponse:
        """
        Get a single project by its ID.
        
        Args:
            project_id (str): The ID of the project to retrieve
            
        Returns:
            ProjectResponse: The project information
        """
        response_data = self._make_request("getProject", method="POST", json_data={"projectId": project_id})
        return ProjectResponse(**response_data) 