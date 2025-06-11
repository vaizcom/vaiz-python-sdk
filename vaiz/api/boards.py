from vaiz.api.base import BaseAPIClient
from vaiz.models import BoardsResponse, BoardResponse


class BoardsAPIClient(BaseAPIClient):
    def get_boards(self) -> BoardsResponse:
        """
        Get all boards in the current space.
        
        Returns:
            BoardsResponse: The list of boards
        """
        response_data = self._make_request("getBoards", method="POST", json_data={})
        return BoardsResponse(**response_data)

    def get_board(self, board_id: str) -> BoardResponse:
        """
        Get a single board by its ID.
        
        Args:
            board_id (str): The ID of the board to retrieve
            
        Returns:
            BoardResponse: The board information
        """
        response_data = self._make_request("getBoard", method="POST", json_data={"boardId": board_id})
        return BoardResponse(**response_data) 