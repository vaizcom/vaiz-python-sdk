from vaiz.api.base import BaseAPIClient
from vaiz.models import MilestonesResponse


class MilestonesAPIClient(BaseAPIClient):
    def get_milestones(self) -> MilestonesResponse:
        """
        Get all milestones in the current space.
        
        Returns:
            MilestonesResponse: The list of milestones
        """
        response_data = self._make_request("getMilestones", method="POST", json_data={})
        return MilestonesResponse(**response_data) 