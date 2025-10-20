from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime

from .enums import Icon, Color
from .base import VaizBaseModel


class CustomFieldType(str, Enum):
    """Types of custom fields available in the board."""
    TEXT = "Text"
    NUMBER = "Number"
    CHECKBOX = "Checkbox"
    DATE = "Date"
    MEMBER = "Member"
    TASK_RELATIONS = "TaskRelations"
    SELECT = "Select"
    URL = "Url"
    ESTIMATION = "Estimation"


class BoardGroup(BaseModel):
    name: str
    id: str = Field(..., alias="_id")
    description: Optional[str] = None
    limit: Optional[int] = None
    hidden: Optional[bool] = None


class BoardType(BaseModel):
    label: str
    icon: Icon
    color: Union[str, Color]  # Color enum value or string
    id: str = Field(..., alias="_id")
    description: Optional[str] = None
    hidden: Optional[bool] = None


class BoardCustomField(BaseModel):
    """
    Represents a custom field in a board.
    
    Attributes:
        name (Optional[str]): The name of the custom field (may not be returned in some API responses)
        type (CustomFieldType): The type of the custom field
        id (str): The unique identifier of the custom field
        description (Optional[str]): Optional description of the custom field
        options (Optional[List[Any]]): List of options for Select type fields
        hidden (Optional[bool]): Whether the field is hidden from view
    """
    name: Optional[str] = None
    type: CustomFieldType
    id: str = Field(..., alias="_id")
    description: Optional[str] = None
    options: Optional[List[Any]] = None
    hidden: Optional[bool] = None


class Board(VaizBaseModel):
    id: str = Field(..., alias="_id")
    name: str
    project: Optional[str] = None
    creator: Optional[str] = None
    archiver: Optional[str] = None
    archived_at: Optional[datetime] = Field(default=None, alias="archivedAt")
    created_at: Optional[datetime] = Field(default=None, alias="createdAt")
    deleter: Optional[str] = None
    deleted_at: Optional[datetime] = Field(default=None, alias="deletedAt")
    groups: Optional[List[BoardGroup]] = None
    types_list: Optional[List[BoardType]] = Field(default=None, alias="typesList")
    custom_fields: Optional[List[BoardCustomField]] = Field(default=None, alias="customFields")
    task_order_by_groups: Optional[Dict[str, List[str]]] = Field(default=None, alias="taskOrderByGroups")
    updated_at: Optional[datetime] = Field(default=None, alias="updatedAt")


class BoardsPayload(BaseModel):
    boards: List[Board]


class BoardsResponse(BaseModel):
    type: str
    payload: BoardsPayload

    @property
    def boards(self) -> List[Board]:
        return self.payload.boards


class BoardResponse(BaseModel):
    type: str
    payload: Dict[str, Board] = Field(..., alias="payload")

    @property
    def board(self) -> Board:
        return self.payload["board"]


class CreateBoardTypeRequest(VaizBaseModel):
    board_id: str = Field(..., alias="boardId")
    label: str
    icon: Icon
    color: Color


class CreateBoardTypePayload(BaseModel):
    boardId: str
    boardType: BoardType


class CreateBoardTypeResponse(BaseModel):
    type: str
    payload: CreateBoardTypePayload

    @property
    def board_type(self) -> BoardType:
        return self.payload.boardType


class EditBoardTypeRequest(VaizBaseModel):
    board_type_id: str = Field(..., alias="boardTypeId")
    board_id: str = Field(..., alias="boardId")
    label: Optional[str] = None
    icon: Optional[Icon] = None
    color: Optional[Color] = None
    description: Optional[str] = None
    hidden: Optional[bool] = None


class EditBoardTypePayload(BaseModel):
    boardId: str
    boardType: BoardType


class EditBoardTypeResponse(BaseModel):
    type: str
    payload: EditBoardTypePayload

    @property
    def board_type(self) -> BoardType:
        return self.payload.boardType


class CreateBoardCustomFieldRequest(VaizBaseModel):
    name: str
    type: CustomFieldType
    board_id: str = Field(..., alias="boardId")
    hidden: Optional[bool] = False
    description: Optional[str] = None
    options: Optional[List[Any]] = None


class CreateBoardCustomFieldPayload(BaseModel):
    customField: BoardCustomField


class CreateBoardCustomFieldResponse(BaseModel):
    type: str
    payload: CreateBoardCustomFieldPayload

    @property
    def custom_field(self) -> BoardCustomField:
        return self.payload.customField


class EditBoardCustomFieldRequest(VaizBaseModel):
    field_id: str = Field(..., alias="fieldId")
    board_id: str = Field(..., alias="boardId")
    name: Optional[str] = None
    hidden: Optional[bool] = None
    description: Optional[str] = None
    options: Optional[List[Any]] = None


class EditBoardCustomFieldPayload(BaseModel):
    customField: BoardCustomField


class EditBoardCustomFieldResponse(BaseModel):
    type: str
    payload: EditBoardCustomFieldPayload

    @property
    def custom_field(self) -> BoardCustomField:
        return self.payload.customField


class CreateBoardGroupRequest(VaizBaseModel):
    name: str
    board_id: str = Field(..., alias="boardId")
    description: Optional[str] = None


class CreateBoardGroupPayload(BaseModel):
    boardGroups: List[BoardGroup]


class CreateBoardGroupResponse(BaseModel):
    type: str
    payload: CreateBoardGroupPayload

    @property
    def board_groups(self) -> List[BoardGroup]:
        return self.payload.boardGroups


class EditBoardGroupRequest(VaizBaseModel):
    board_group_id: str = Field(..., alias="boardGroupId")
    board_id: str = Field(..., alias="boardId")
    name: Optional[str] = None
    description: Optional[str] = None
    limit: Optional[int] = None
    hidden: Optional[bool] = None


class EditBoardGroupPayload(BaseModel):
    boardGroups: List[BoardGroup]


class EditBoardGroupResponse(BaseModel):
    type: str
    payload: EditBoardGroupPayload

    @property
    def board_groups(self) -> List[BoardGroup]:
        return self.payload.boardGroups 