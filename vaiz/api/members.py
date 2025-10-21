from vaiz.api.base import BaseAPIClient
from vaiz.models import GetSpaceMembersResponse


class MembersAPIClient(BaseAPIClient):
    def get_space_members(self) -> GetSpaceMembersResponse:
        """
        Get all members in the current space.
        
        Returns:
            GetSpaceMembersResponse: The list of space members
        """
        response_data = self._make_request("getSpaceMembers", method="POST", json_data={})
        return GetSpaceMembersResponse(**response_data)

