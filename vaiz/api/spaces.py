from vaiz.api.base import BaseAPIClient
from vaiz.models import GetSpaceResponse


class SpacesAPIClient(BaseAPIClient):
    def get_space(self, space_id: str) -> GetSpaceResponse:
        """
        Get information about a specific space.
        
        Args:
            space_id (str): The ID of the space to retrieve
            
        Returns:
            GetSpaceResponse: The space information
        """
        response_data = self._make_request("getSpace", method="POST", json_data={"spaceId": space_id})
        return GetSpaceResponse(**response_data)

