from vaiz.api.base import BaseAPIClient
from vaiz.models import ProfileResponse, EditProfileRequest


class ProfileAPIClient(BaseAPIClient):
    def get_profile(self) -> ProfileResponse:
        """
        Get the current member's profile in the current space.
        
        Returns:
            ProfileResponse: The member's profile information
        """
        response_data = self._make_request("getProfile", method="POST", json_data={})
        return ProfileResponse(**response_data)

    def edit_profile(self, request: EditProfileRequest) -> ProfileResponse:
        """
        Edit the current member's profile in the current space.
        
        Args:
            request (EditProfileRequest): Fields to update; omitted fields stay unchanged
            
        Returns:
            ProfileResponse: The updated profile
        """
        response_data = self._make_request("editProfile", method="POST", json_data=request.model_dump())
        return ProfileResponse(**response_data)
