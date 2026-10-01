from typing import List
from vaiz.api.base import BaseAPIClient
from vaiz.models import GetSpaceMembersResponse, GetMembersRequest, GetMembersResponse


class MembersAPIClient(BaseAPIClient):
    def get_space_members(self) -> GetSpaceMembersResponse:
        """
        Get all members in the current space.
        
        Returns:
            GetSpaceMembersResponse: The list of space members
        """
        response_data = self._make_request("getSpaceMembers", method="POST", json_data={})
        return GetSpaceMembersResponse(**response_data)

    def get_members(self, member_ids: List[str]) -> GetMembersResponse:
        """
        Get members by their IDs.
        
        Args:
            member_ids (List[str]): IDs of the members to retrieve
            
        Returns:
            GetMembersResponse: The requested members; unknown IDs are skipped
        """
        request = GetMembersRequest(member_ids=member_ids)
        response_data = self._make_request("getMembers", method="POST", json_data=request.model_dump())
        return GetMembersResponse(**response_data)
