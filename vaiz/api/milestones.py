from vaiz.api.base import BaseAPIClient
from vaiz.models import MilestonesResponse, CreateMilestoneRequest, CreateMilestoneResponse


class MilestonesAPIClient(BaseAPIClient):
    def get_milestones(self) -> MilestonesResponse:
        """
        Get all milestones in the current space.
        
        Returns:
            MilestonesResponse: The list of milestones
        """
        response_data = self._make_request("getMilestones", method="POST", json_data={})
        return MilestonesResponse(**response_data)

    def create_milestone(self, request: CreateMilestoneRequest) -> CreateMilestoneResponse:
        """
        Create a new milestone.
        
        Args:
            request (CreateMilestoneRequest): The milestone creation request
            
        Returns:
            CreateMilestoneResponse: The created milestone information
        """
        response_data = self._make_request("createMilestone", method="POST", json_data=request.model_dump())
        return CreateMilestoneResponse(**response_data) 