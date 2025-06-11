from vaiz.api.base import BaseAPIClient
from vaiz.models import ProfileResponse


class ProfileAPIClient(BaseAPIClient):
    def get_profile(self) -> ProfileResponse:
        """
        Get the current user's profile.
        
        Returns:
            ProfileResponse: The user's profile information
        """
        response_data = self._make_request("getProfile", method="POST", json_data={})
        return ProfileResponse(**response_data) 