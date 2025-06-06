from pydantic import BaseModel, RootModel, Field
from typing import List, Optional, Dict, Literal, Any, Union
from enum import Enum


class TaskFollower(RootModel):
    root: Dict[str, Literal["creator"]]


class TaskPriority(int, Enum):
    Low = 0
    General = 1
    Medium = 2
    High = 3


class CustomField(BaseModel):
    id: str
    value: Union[str, List[str]] 