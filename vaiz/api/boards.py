from vaiz.api.base import BaseAPIClient
from vaiz.models import BoardsResponse


class BoardsAPIClient(BaseAPIClient):
    def get_boards(self) -> BoardsResponse:
        """
        Get all boards in the current space.
        
        Returns:
            BoardsResponse: The list of boards
        """
        response_data = self._make_request("getBoards", method="POST", json_data={})
        return BoardsResponse(**response_data) 