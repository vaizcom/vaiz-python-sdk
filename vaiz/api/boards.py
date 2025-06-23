from vaiz.api.base import BaseAPIClient
from vaiz.models import (
    BoardsResponse, 
    BoardResponse, 
    CreateBoardTypeRequest, 
    CreateBoardTypeResponse,
    EditBoardTypeRequest,
    EditBoardTypeResponse,
    CreateBoardCustomFieldRequest,
    CreateBoardCustomFieldResponse,
    EditBoardCustomFieldRequest,
    EditBoardCustomFieldResponse,
    CreateBoardGroupRequest,
    CreateBoardGroupResponse,
    EditBoardGroupRequest,
    EditBoardGroupResponse,
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

    def create_board_custom_field(self, request: CreateBoardCustomFieldRequest) -> CreateBoardCustomFieldResponse:
        """
        Create a new custom field in a board.
        
        Args:
            request (CreateBoardCustomFieldRequest): The custom field creation request
            
        Returns:
            CreateBoardCustomFieldResponse: The created custom field information
        """
        response_data = self._make_request("createBoardCustomField", method="POST", json_data=request.model_dump())
        return CreateBoardCustomFieldResponse(**response_data)

    def edit_board_custom_field(self, request: EditBoardCustomFieldRequest) -> EditBoardCustomFieldResponse:
        """
        Edit an existing custom field in a board.
        
        Args:
            request (EditBoardCustomFieldRequest): The custom field edit request
            
        Returns:
            EditBoardCustomFieldResponse: The updated custom field information
        """
        response_data = self._make_request("editBoardCustomField", method="POST", json_data=request.model_dump())
        return EditBoardCustomFieldResponse(**response_data)

    def create_board_group(self, request: CreateBoardGroupRequest) -> CreateBoardGroupResponse:
        """
        Create a new group in a board.

        Args:
            request (CreateBoardGroupRequest): The board group creation request

        Returns:
            CreateBoardGroupResponse: The list of board groups including the new one.
        """
        response_data = self._make_request("createBoardGroup", method="POST", json_data=request.model_dump())
        return CreateBoardGroupResponse(**response_data)

    def edit_board_group(self, request: EditBoardGroupRequest) -> EditBoardGroupResponse:
        """
        Edit a group in a board.

        Args:
            request (EditBoardGroupRequest): The board group edit request

        Returns:
            EditBoardGroupResponse: The list of board groups after editing.
        """
        response_data = self._make_request("editBoardGroup", method="POST", json_data=request.model_dump())
        return EditBoardGroupResponse(**response_data) 