from vaiz.api.base import BaseAPIClient
from vaiz.models import (
    BoardsResponse, 
    BoardResponse, 
    CreateBoardTypeRequest, 
    CreateBoardTypeResponse,
    EditBoardTypeRequest,
    EditBoardTypeResponse
)


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

    def create_board_type(self, request: CreateBoardTypeRequest) -> CreateBoardTypeResponse:
        """
        Create a new board type.
        
        Args:
            request (CreateBoardTypeRequest): The board type creation request
            
        Returns:
            CreateBoardTypeResponse: The created board type information
        """
        response_data = self._make_request("createBoardType", method="POST", json_data=request.model_dump())
        return CreateBoardTypeResponse(**response_data)

    def edit_board_type(self, request: EditBoardTypeRequest) -> EditBoardTypeResponse:
        """
        Edit an existing board type.
        
        Args:
            request (EditBoardTypeRequest): The board type edit request
            
        Returns:
            EditBoardTypeResponse: The updated board type information
        """
        response_data = self._make_request("editBoardType", method="POST", json_data=request.model_dump())
        return EditBoardTypeResponse(**response_data) 