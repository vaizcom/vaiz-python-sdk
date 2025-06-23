from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum

from .enums import EIcon, EColor


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


class BoardGroup(BaseModel):
    name: str
    id: str = Field(..., alias="_id")
    description: Optional[str] = None
    limit: Optional[int] = None
    hidden: Optional[bool] = None


class BoardType(BaseModel):
    label: str
    icon: EIcon
    color: EColor
    id: str = Field(..., alias="_id")
    description: Optional[str] = None
    hidden: Optional[bool] = None


class BoardCustomField(BaseModel):
    """
    Represents a custom field in a board.
    
    Attributes:
        name (str): The name of the custom field
        type (CustomFieldType): The type of the custom field
        id (str): The unique identifier of the custom field
        description (Optional[str]): Optional description of the custom field
        options (Optional[List[Any]]): List of options for Select type fields
        hidden (Optional[bool]): Whether the field is hidden from view
    """
    name: str
    type: CustomFieldType
    id: str = Field(..., alias="_id")
    description: Optional[str] = None
    options: Optional[List[Any]] = None
    hidden: Optional[bool] = None


class Board(BaseModel):
    id: str = Field(..., alias="_id")
    name: str
    project: Optional[str] = None
    creator: Optional[str] = None
    archiver: Optional[str] = None
    archived_at: Optional[str] = Field(None, alias="archivedAt")
    created_at: Optional[str] = Field(None, alias="createdAt")
    deleter: Optional[str] = None
    deleted_at: Optional[str] = Field(None, alias="deletedAt")
    groups: Optional[List[BoardGroup]] = None
    types_list: Optional[List[BoardType]] = Field(None, alias="typesList")
    custom_fields: Optional[List[BoardCustomField]] = Field(None, alias="customFields")
    task_order_by_groups: Optional[Dict[str, List[str]]] = Field(None, alias="taskOrderByGroups")
    updated_at: Optional[str] = Field(None, alias="updatedAt")


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


class CreateBoardTypeRequest(BaseModel):
    boardId: str
    label: str
    icon: EIcon
    color: EColor

    def model_dump(self, **kwargs):
        data = super().model_dump(**kwargs)
        return {k: v for k, v in data.items() if v is not None}


class CreateBoardTypePayload(BaseModel):
    boardId: str
    boardType: BoardType


class CreateBoardTypeResponse(BaseModel):
    type: str
    payload: CreateBoardTypePayload

    @property
    def board_type(self) -> BoardType:
        return self.payload.boardType


class EditBoardTypeRequest(BaseModel):
    boardTypeId: str
    boardId: str
    label: Optional[str] = None
    icon: Optional[EIcon] = None
    color: Optional[EColor] = None
    description: Optional[str] = None
    hidden: Optional[bool] = None

    def model_dump(self, **kwargs):
        data = super().model_dump(**kwargs)
        return {k: v for k, v in data.items() if v is not None}


class EditBoardTypePayload(BaseModel):
    boardId: str
    boardType: BoardType


class EditBoardTypeResponse(BaseModel):
    type: str
    payload: EditBoardTypePayload

    @property
    def board_type(self) -> BoardType:
        return self.payload.boardType


class CreateBoardCustomFieldRequest(BaseModel):
    name: str
    type: CustomFieldType
    boardId: str
    hidden: Optional[bool] = False
    description: Optional[str] = None
    options: Optional[List[Any]] = None

    def model_dump(self, **kwargs):
        data = super().model_dump(**kwargs)
        return {k: v for k, v in data.items() if v is not None}


class CreateBoardCustomFieldPayload(BaseModel):
    customField: BoardCustomField


class CreateBoardCustomFieldResponse(BaseModel):
    type: str
    payload: CreateBoardCustomFieldPayload

    @property
    def custom_field(self) -> BoardCustomField:
        return self.payload.customField


class EditBoardCustomFieldRequest(BaseModel):
    fieldId: str
    boardId: str
    hidden: Optional[bool] = None
    description: Optional[str] = None
    options: Optional[List[Any]] = None

    def model_dump(self, **kwargs):
        data = super().model_dump(**kwargs)
        return {k: v for k, v in data.items() if v is not None}


class EditBoardCustomFieldPayload(BaseModel):
    customField: BoardCustomField


class EditBoardCustomFieldResponse(BaseModel):
    type: str
    payload: EditBoardCustomFieldPayload

    @property
    def custom_field(self) -> BoardCustomField:
        return self.payload.customField


class CreateBoardGroupRequest(BaseModel):
    name: str
    boardId: str
    description: Optional[str] = None

    def model_dump(self, **kwargs):
        data = super().model_dump(**kwargs)
        return {k: v for k, v in data.items() if v is not None}


class CreateBoardGroupPayload(BaseModel):
    boardGroups: List[BoardGroup]


class CreateBoardGroupResponse(BaseModel):
    type: str
    payload: CreateBoardGroupPayload

    @property
    def board_groups(self) -> List[BoardGroup]:
        return self.payload.boardGroups


class EditBoardGroupRequest(BaseModel):
    boardGroupId: str
    boardId: str
    name: Optional[str] = None
    description: Optional[str] = None
    limit: Optional[int] = None
    hidden: Optional[bool] = None

    def model_dump(self, **kwargs):
        kwargs.setdefault('exclude_none', True)
        return super().model_dump(**kwargs)


class EditBoardGroupPayload(BaseModel):
    boardGroups: List[BoardGroup]


class EditBoardGroupResponse(BaseModel):
    type: str
    payload: EditBoardGroupPayload

    @property
    def board_groups(self) -> List[BoardGroup]:
        return self.payload.boardGroups 