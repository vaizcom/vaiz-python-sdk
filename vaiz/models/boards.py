from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class BoardGroup(BaseModel):
    name: str
    id: str = Field(..., alias="_id")


class BoardType(BaseModel):
    label: str
    icon: str
    color: str
    id: str = Field(..., alias="_id")
    description: Optional[str] = None
    hidden: Optional[bool] = None


class BoardCustomField(BaseModel):
    name: str
    type: str
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
    icon: str
    color: str

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
    icon: Optional[str] = None
    color: Optional[str] = None
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