from vaiz.api.base import BaseAPIClient
from vaiz.models import MilestonesResponse, CreateMilestoneRequest, CreateMilestoneResponse, GetMilestoneResponse, EditMilestoneRequest, EditMilestoneResponse, ToggleMilestoneRequest, ToggleMilestoneResponse


class MilestonesAPIClient(BaseAPIClient):
    def get_milestones(self) -> MilestonesResponse:
        """
        Get all milestones in the current space.
        
        Returns:
            MilestonesResponse: The list of milestones
        """
        response_data = self._make_request("getMilestones", method="POST", json_data={})
        return MilestonesResponse(**response_data)

    def get_milestone(self, milestone_id: str) -> GetMilestoneResponse:
        """
        Get a single milestone by its ID.
        
        Args:
            milestone_id (str): The ID of the milestone to retrieve
            
        Returns:
            GetMilestoneResponse: The milestone information
        """
        response_data = self._make_request("getMilestone", method="POST", json_data={"_id": milestone_id})
        return GetMilestoneResponse(**response_data)

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

    def edit_milestone(self, request: EditMilestoneRequest) -> EditMilestoneResponse:
        """
        Edit an existing milestone.
        
        Args:
            request (EditMilestoneRequest): The milestone edit request
            
        Returns:
            EditMilestoneResponse: The updated milestone information
        """
        response_data = self._make_request("editMilestone", method="POST", json_data=request.model_dump())
        return EditMilestoneResponse(**response_data)

    def toggle_milestone(self, request: ToggleMilestoneRequest) -> ToggleMilestoneResponse:
        """
        Toggle milestone assignment for a task (attach/detach task to/from milestones).
        
        Args:
            request (ToggleMilestoneRequest): The milestone toggle request containing task ID and milestone IDs
            
        Returns:
            ToggleMilestoneResponse: The updated task information with milestone assignments
        """
        response_data = self._make_request("toggleMilestone", method="POST", json_data=request.model_dump())
        return ToggleMilestoneResponse(**response_data) 