from pydantic import BaseModel, RootModel, Field, ConfigDict, model_serializer
from typing import List, Optional, Dict, Literal, Any, Union
from enum import Enum
from datetime import datetime


class VaizBaseModel(BaseModel):
    """
    Base model for all Vaiz API models with automatic date/datetime handling.
    
    Features:
    - Automatically parses ISO date strings to datetime objects
    - Automatically serializes datetime objects to ISO strings for API
    - Proper field alias support
    """
    
    model_config = ConfigDict(
        # Allow population by field name and alias
        populate_by_name=True,
        # Validate assignments
        validate_assignment=True
    )

    @model_serializer(mode='wrap')
    def serialize_model(self, serializer, info):
        """Custom serializer to handle datetime objects."""
        data = serializer(self)
        if isinstance(data, dict):
            # Convert datetime objects to ISO strings
            for key, value in data.items():
                if isinstance(value, datetime):
                    data[key] = value.isoformat()
        return data


class ColorInfo(BaseModel):
    """Color configuration used across different entities (profiles, spaces, members)."""
    color: str
    is_dark: bool = Field(..., alias="isDark")


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