from vaiz.api.base import BaseAPIClient
from vaiz.models import ProjectsResponse


class ProjectsAPIClient(BaseAPIClient):
    def get_projects(self) -> ProjectsResponse:
        """
        Get all projects in the current space.
        
        Returns:
            ProjectsResponse: The list of projects
        """
        response_data = self._make_request("getProjects", method="POST", json_data={})
        return ProjectsResponse(**response_data) 