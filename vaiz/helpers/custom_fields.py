"""
Custom Fields Helper Functions

This module provides helper functions for creating and managing custom fields
in the Vaiz SDK with strong typing and simplified APIs.
"""

import hashlib
from datetime import datetime
from typing import List, Optional, Dict, Any, Union
from vaiz.models import (
    CreateBoardCustomFieldRequest,
    EditBoardCustomFieldRequest, 
    CustomFieldType,
    CreateBoardCustomFieldResponse,
    EditBoardCustomFieldResponse
)
from vaiz.models.enums import Color, Icon


class SelectOption:
    """Represents a select field option with proper typing."""
    
    def __init__(
        self,
        title: str,
        color: Union[Color, str],
        icon: Union[Icon, str],
        option_id: Optional[str] = None
    ):
        self.title = title
        self.color = color if isinstance(color, Color) else Color(color)
        self.icon = icon if isinstance(icon, Icon) else Icon(icon)
        self.id = option_id or self._generate_id(title)
    
    def _generate_id(self, title: str) -> str:
        """Generate a unique ID for the option based on title."""
        return hashlib.md5(title.encode()).hexdigest()[:24]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format expected by API."""
        return {
            "_id": self.id,
            "title": self.title,
            "color": self.color,
            "icon": self.icon
        }


def make_select_option(
    title: str,
    color: Union[Color, str],
    icon: Union[Icon, str],
    option_id: Optional[str] = None
) -> SelectOption:
    """
    Create a select field option with proper typing.
    
    Args:
        title: Display name for the option
        color: Color from Color enum or string value
        icon: Icon from Icon enum or string value
        option_id: Optional custom ID (auto-generated if not provided)
        
    Returns:
        SelectOption: Typed option object
        
    Example:
        option = make_select_option(
            title="High Priority",
            color=Color.Red,
            icon=Icon.Flag
        )
    """
    return SelectOption(title, color, icon, option_id)


def make_text_field(
    name: str,
    board_id: str,
    description: Optional[str] = None,
    hidden: bool = False
) -> CreateBoardCustomFieldRequest:
    """
    Create a text custom field request.
    
    Args:
        name: Field name
        board_id: Board ID where field will be created
        description: Optional field description
        hidden: Whether field is hidden from view
        
    Returns:
        CreateBoardCustomFieldRequest: Ready-to-use request object
        
    Example:
        text_field = make_text_field(
            name="Customer Name",
            board_id="board123",
            description="Name of the customer"
        )
    """
    return CreateBoardCustomFieldRequest(
        name=name,
        type=CustomFieldType.TEXT,
        board_id=board_id,
        description=description,
        hidden=hidden
    )


def make_number_field(
    name: str,
    board_id: str,
    description: Optional[str] = None,
    hidden: bool = False
) -> CreateBoardCustomFieldRequest:
    """
    Create a number custom field request.
    
    Args:
        name: Field name
        board_id: Board ID where field will be created
        description: Optional field description
        hidden: Whether field is hidden from view
        
    Returns:
        CreateBoardCustomFieldRequest: Ready-to-use request object
        
    Example:
        number_field = make_number_field(
            name="Price",
            board_id="board123",
            description="Item price in USD"
        )
    """
    return CreateBoardCustomFieldRequest(
        name=name,
        type=CustomFieldType.NUMBER,
        board_id=board_id,
        description=description,
        hidden=hidden
    )


def make_checkbox_field(
    name: str,
    board_id: str,
    description: Optional[str] = None,
    hidden: bool = False
) -> CreateBoardCustomFieldRequest:
    """
    Create a checkbox custom field request.
    
    Args:
        name: Field name
        board_id: Board ID where field will be created
        description: Optional field description
        hidden: Whether field is hidden from view
        
    Returns:
        CreateBoardCustomFieldRequest: Ready-to-use request object
        
    Example:
        checkbox_field = make_checkbox_field(
            name="Approved",
            board_id="board123",
            description="Mark if approved"
        )
    """
    return CreateBoardCustomFieldRequest(
        name=name,
        type=CustomFieldType.CHECKBOX,
        board_id=board_id,
        description=description,
        hidden=hidden
    )


def make_date_field(
    name: str,
    board_id: str,
    description: Optional[str] = None,
    hidden: bool = False
) -> CreateBoardCustomFieldRequest:
    """
    Create a date custom field request.
    
    Args:
        name: Field name
        board_id: Board ID where field will be created
        description: Optional field description
        hidden: Whether field is hidden from view
        
    Returns:
        CreateBoardCustomFieldRequest: Ready-to-use request object
        
    Example:
        date_field = make_date_field(
            name="Launch Date",
            board_id="board123",
            description="Product launch date"
        )
    """
    return CreateBoardCustomFieldRequest(
        name=name,
        type=CustomFieldType.DATE,
        board_id=board_id,
        description=description,
        hidden=hidden
    )


def make_member_field(
    name: str,
    board_id: str,
    description: Optional[str] = None,
    hidden: bool = False
) -> CreateBoardCustomFieldRequest:
    """
    Create a member custom field request.
    
    Args:
        name: Field name
        board_id: Board ID where field will be created
        description: Optional field description
        hidden: Whether field is hidden from view
        
    Returns:
        CreateBoardCustomFieldRequest: Ready-to-use request object
        
    Example:
        member_field = make_member_field(
            name="Reviewer",
            board_id="board123",
            description="Task reviewer"
        )
    """
    return CreateBoardCustomFieldRequest(
        name=name,
        type=CustomFieldType.MEMBER,
        board_id=board_id,
        description=description,
        hidden=hidden
    )


def make_task_relations_field(
    name: str,
    board_id: str,
    description: Optional[str] = None,
    hidden: bool = False
) -> CreateBoardCustomFieldRequest:
    """
    Create a task relations custom field request.
    
    Args:
        name: Field name
        board_id: Board ID where field will be created
        description: Optional field description
        hidden: Whether field is hidden from view
        
    Returns:
        CreateBoardCustomFieldRequest: Ready-to-use request object
        
    Example:
        relations_field = make_task_relations_field(
            name="Related Tasks",
            board_id="board123",
            description="Related or dependent tasks"
        )
    """
    return CreateBoardCustomFieldRequest(
        name=name,
        type=CustomFieldType.TASK_RELATIONS,
        board_id=board_id,
        description=description,
        hidden=hidden
    )


def make_select_field(
    name: str,
    board_id: str,
    options: List[Union[SelectOption, Dict[str, Any]]],
    description: Optional[str] = None,
    hidden: bool = False
) -> CreateBoardCustomFieldRequest:
    """
    Create a select custom field request with options.
    
    Args:
        name: Field name
        board_id: Board ID where field will be created
        options: List of SelectOption objects or dictionaries
        description: Optional field description
        hidden: Whether field is hidden from view
        
    Returns:
        CreateBoardCustomFieldRequest: Ready-to-use request object
        
    Example:
        options = [
            make_select_option("High", Color.Red, Icon.Flag),
            make_select_option("Medium", Color.Orange, Icon.Circle),
            make_select_option("Low", Color.Green, Icon.Target)
        ]
        select_field = make_select_field(
            name="Priority",
            board_id="board123",
            options=options,
            description="Task priority level"
        )
    """
    # Convert options to proper format
    formatted_options = []
    for option in options:
        if isinstance(option, SelectOption):
            formatted_options.append(option.to_dict())
        elif isinstance(option, dict):
            formatted_options.append(option)
        else:
            raise ValueError(f"Invalid option type: {type(option)}. Must be SelectOption or dict.")
    
    return CreateBoardCustomFieldRequest(
        name=name,
        type=CustomFieldType.SELECT,
        board_id=board_id,
        description=description,
        hidden=hidden,
        options=formatted_options
    )


def make_url_field(
    name: str,
    board_id: str,
    description: Optional[str] = None,
    hidden: bool = False
) -> CreateBoardCustomFieldRequest:
    """
    Create a URL custom field request.
    
    Args:
        name: Field name
        board_id: Board ID where field will be created
        description: Optional field description
        hidden: Whether field is hidden from view
        
    Returns:
        CreateBoardCustomFieldRequest: Ready-to-use request object
        
    Example:
        url_field = make_url_field(
            name="Reference Link",
            board_id="board123",
            description="Link to external resource"
        )
    """
    return CreateBoardCustomFieldRequest(
        name=name,
        type=CustomFieldType.URL,
        board_id=board_id,
        description=description,
        hidden=hidden
    )


def add_board_custom_field_select_option(
    field_id: str,
    board_id: str,
    new_option: Union[SelectOption, Dict[str, Any]],
    existing_options: List[Dict[str, Any]]
) -> EditBoardCustomFieldRequest:
    """
    Add a new option to an existing select field.
    
    Args:
        field_id: ID of the custom field to edit
        board_id: Board ID where field exists
        new_option: New option to add (SelectOption or dict)
        existing_options: Current field options
        
    Returns:
        EditBoardCustomFieldRequest: Ready-to-use edit request
        
    Example:
        # First get the field and its current options from API
        # board = client.get_board(board_id)
        # field = next(f for f in board.custom_fields if f.id == field_id)
        # existing_options = field.options
        
        new_option = make_select_option("Very High", Color.Magenta, Icon.Crown)
        edit_request = add_board_custom_field_select_option(
            field_id=field_id,
            board_id=board_id,
            new_option=new_option,
            existing_options=existing_options
        )
        # client.edit_board_custom_field(edit_request)
    """
    # Format new option
    if isinstance(new_option, SelectOption):
        formatted_option = new_option.to_dict()
    elif isinstance(new_option, dict):
        formatted_option = new_option
    else:
        raise ValueError(f"Invalid option type: {type(new_option)}. Must be SelectOption or dict.")
    
    # Combine existing and new options
    updated_options = existing_options + [formatted_option]
    
    return EditBoardCustomFieldRequest(
        field_id=field_id,
        board_id=board_id,
        options=updated_options
    )


def remove_board_custom_field_select_option(
    field_id: str,
    board_id: str,
    option_id: str,
    existing_options: List[Dict[str, Any]]
) -> EditBoardCustomFieldRequest:
    """
    Remove an option from an existing select field.
    
    Args:
        field_id: ID of the custom field to edit
        board_id: Board ID where field exists
        option_id: ID of the option to remove
        existing_options: Current field options
        
    Returns:
        EditBoardCustomFieldRequest: Ready-to-use edit request
        
    Example:
        # First get the field and its current options from API
        # board = client.get_board(board_id)
        # field = next(f for f in board.custom_fields if f.id == field_id)
        # existing_options = field.options
        
        edit_request = remove_board_custom_field_select_option(
            field_id=field_id,
            board_id=board_id,
            option_id="option_id_to_remove",
            existing_options=existing_options
        )
        # client.edit_board_custom_field(edit_request)
    """
    # Filter out the option to remove
    updated_options = [opt for opt in existing_options if opt.get("_id") != option_id]
    
    if len(updated_options) == len(existing_options):
        raise ValueError(f"Option with ID '{option_id}' not found in existing options")
    
    return EditBoardCustomFieldRequest(
        field_id=field_id,
        board_id=board_id,
        options=updated_options
    )


def edit_board_custom_field_select_field_option(
    field_id: str,
    board_id: str,
    option_id: str,
    updated_option: Union[SelectOption, Dict[str, Any]],
    existing_options: List[Dict[str, Any]]
) -> EditBoardCustomFieldRequest:
    """
    Edit an existing option in a select field.
    
    Args:
        field_id: ID of the custom field to edit
        board_id: Board ID where field exists
        option_id: ID of the option to edit
        updated_option: Updated option data (SelectOption or dict)
        existing_options: Current field options
        
    Returns:
        EditBoardCustomFieldRequest: Ready-to-use edit request
        
    Example:
        # First get the field and its current options from API
        # board = client.get_board(board_id)
        # field = next(f for f in board.custom_fields if f.id == field_id)
        # existing_options = field.options
        
        updated_option = make_select_option("Critical", Color.Red, Icon.Fire)
        edit_request = edit_board_custom_field_select_field_option(
            field_id=field_id,
            board_id=board_id,
            option_id="option_id_to_edit",
            updated_option=updated_option,
            existing_options=existing_options
        )
        # client.edit_board_custom_field(edit_request)
    """
    # Format updated option
    if isinstance(updated_option, SelectOption):
        formatted_option = updated_option.to_dict()
        # Preserve the original ID if not explicitly set
        if "_id" not in formatted_option or formatted_option["_id"] != option_id:
            formatted_option["_id"] = option_id
    elif isinstance(updated_option, dict):
        formatted_option = updated_option.copy()
        formatted_option["_id"] = option_id
    else:
        raise ValueError(f"Invalid option type: {type(updated_option)}. Must be SelectOption or dict.")
    
    # Find and replace the option
    updated_options = []
    option_found = False
    
    for opt in existing_options:
        if opt.get("_id") == option_id:
            updated_options.append(formatted_option)
            option_found = True
        else:
            updated_options.append(opt)
    
    if not option_found:
        raise ValueError(f"Option with ID '{option_id}' not found in existing options")
    
    return EditBoardCustomFieldRequest(
        field_id=field_id,
        board_id=board_id,
        options=updated_options
    )


# =============================================================================
# EDIT CUSTOM FIELD HELPERS
# =============================================================================

def edit_custom_field_name(
    field_id: str,
    board_id: str,
    new_name: str
) -> EditBoardCustomFieldRequest:
    """
    Edit the name of an existing custom field.
    
    Args:
        field_id: ID of the custom field to edit
        board_id: Board ID where field exists
        new_name: New name for the field
        
    Returns:
        EditBoardCustomFieldRequest: Ready-to-use edit request
        
    Example:
        edit_request = edit_custom_field_name(
            field_id="field123",
            board_id="board123",
            new_name="Updated Field Name"
        )
        # client.edit_board_custom_field(edit_request)
    """
    return EditBoardCustomFieldRequest(
        field_id=field_id,
        board_id=board_id,
        name=new_name
    )


def edit_custom_field_description(
    field_id: str,
    board_id: str,
    new_description: Optional[str]
) -> EditBoardCustomFieldRequest:
    """
    Edit the description of an existing custom field.
    
    Args:
        field_id: ID of the custom field to edit
        board_id: Board ID where field exists
        new_description: New description for the field (None to remove)
        
    Returns:
        EditBoardCustomFieldRequest: Ready-to-use edit request
        
    Example:
        edit_request = edit_custom_field_description(
            field_id="field123",
            board_id="board123",
            new_description="Updated field description"
        )
        # client.edit_board_custom_field(edit_request)
    """
    return EditBoardCustomFieldRequest(
        field_id=field_id,
        board_id=board_id,
        description=new_description
    )


def edit_custom_field_visibility(
    field_id: str,
    board_id: str,
    hidden: bool
) -> EditBoardCustomFieldRequest:
    """
    Edit the visibility of an existing custom field.
    
    Args:
        field_id: ID of the custom field to edit
        board_id: Board ID where field exists
        hidden: Whether the field should be hidden
        
    Returns:
        EditBoardCustomFieldRequest: Ready-to-use edit request
        
    Example:
        # Hide a field
        edit_request = edit_custom_field_visibility(
            field_id="field123",
            board_id="board123",
            hidden=True
        )
        # client.edit_board_custom_field(edit_request)
    """
    return EditBoardCustomFieldRequest(
        field_id=field_id,
        board_id=board_id,
        hidden=hidden
    )


def edit_custom_field_complete(
    field_id: str,
    board_id: str,
    name: Optional[str] = None,
    description: Optional[str] = None,
    hidden: Optional[bool] = None,
    options: Optional[List[Dict[str, Any]]] = None
) -> EditBoardCustomFieldRequest:
    """
    Edit multiple properties of an existing custom field at once.
    
    Args:
        field_id: ID of the custom field to edit
        board_id: Board ID where field exists
        name: New name for the field (optional)
        description: New description for the field (optional)
        hidden: Whether the field should be hidden (optional)
        options: New options for select fields (optional)
        
    Returns:
        EditBoardCustomFieldRequest: Ready-to-use edit request
        
    Example:
        edit_request = edit_custom_field_complete(
            field_id="field123",
            board_id="board123",
            name="Updated Name",
            description="Updated description",
            hidden=False
        )
        # client.edit_board_custom_field(edit_request)
    """
    request = EditBoardCustomFieldRequest(
        field_id=field_id,
        board_id=board_id
    )
    
    if name is not None:
        request.name = name
    if description is not None:
        request.description = description
    if hidden is not None:
        request.hidden = hidden
    if options is not None:
        request.options = options
    
    return request


# =============================================================================
# TASK RELATIONS HELPERS
# =============================================================================

def make_task_relation_value(
    related_task_ids: List[str]
) -> List[str]:
    """
    Create a properly formatted value for task relations custom field.
    
    Args:
        related_task_ids: List of task IDs to relate
        
    Returns:
        List[str]: Formatted value for task relations field
        
    Example:
        relations = make_task_relation_value([
            "task123",
            "task456", 
            "task789"
        ])
        
        custom_field = CustomField(
            id="field_id",
            value=relations
        )
    """
    return related_task_ids


def add_task_relation(
    current_relations: List[str],
    new_task_id: str
) -> List[str]:
    """
    Add a new task relation to existing relations.
    
    Args:
        current_relations: Current list of related task IDs
        new_task_id: New task ID to add to relations
        
    Returns:
        List[str]: Updated list of task relations
        
    Example:
        # Get current relations from task custom field
        current_relations = task.custom_fields[0].value  # Assuming it's a relations field
        
        # Add new relation
        updated_relations = add_task_relation(current_relations, "new_task_123")
        
        # Update the custom field
        updated_field = CustomField(id=field_id, value=updated_relations)
    """
    if new_task_id not in current_relations:
        return current_relations + [new_task_id]
    return current_relations


def remove_task_relation(
    current_relations: List[str],
    task_id_to_remove: str
) -> List[str]:
    """
    Remove a task relation from existing relations.
    
    Args:
        current_relations: Current list of related task IDs
        task_id_to_remove: Task ID to remove from relations
        
    Returns:
        List[str]: Updated list of task relations
        
    Example:
        # Get current relations from task custom field
        current_relations = task.custom_fields[0].value
        
        # Remove relation
        updated_relations = remove_task_relation(current_relations, "task_to_remove")
        
        # Update the custom field
        updated_field = CustomField(id=field_id, value=updated_relations)
    """
    return [task_id for task_id in current_relations if task_id != task_id_to_remove]


# =============================================================================
# MEMBER FIELD HELPERS
# =============================================================================

def make_member_value(
    member_ids: Union[str, List[str]]
) -> Union[str, List[str]]:
    """
    Create a properly formatted value for member custom field.
    
    Args:
        member_ids: Single member ID or list of member IDs
        
    Returns:
        Union[str, List[str]]: Formatted value for member field
        
    Example:
        # Single member
        single_member = make_member_value("user123")
        
        # Multiple members
        multiple_members = make_member_value(["user123", "user456", "user789"])
        
        custom_field = CustomField(
            id="field_id",
            value=single_member  # or multiple_members
        )
    """
    return member_ids


def add_member_to_field(
    current_members: Union[str, List[str]],
    new_member_id: str
) -> List[str]:
    """
    Add a new member to an existing member field.
    
    Args:
        current_members: Current member(s) - string for single, list for multiple
        new_member_id: New member ID to add
        
    Returns:
        List[str]: Updated list of members
        
    Example:
        # Current field has single member
        current_members = "user123"
        updated_members = add_member_to_field(current_members, "user456")
        # Result: ["user123", "user456"]
        
        # Current field has multiple members
        current_members = ["user123", "user456"]
        updated_members = add_member_to_field(current_members, "user789")
        # Result: ["user123", "user456", "user789"]
    """
    # Convert to list if it's a single string
    if isinstance(current_members, str):
        members_list = [current_members]
    else:
        members_list = list(current_members)
    
    # Add new member if not already present
    if new_member_id not in members_list:
        members_list.append(new_member_id)
    
    return members_list


def remove_member_from_field(
    current_members: Union[str, List[str]],
    member_id_to_remove: str
) -> Union[str, List[str]]:
    """
    Remove a member from an existing member field.
    
    Args:
        current_members: Current member(s) - string for single, list for multiple
        member_id_to_remove: Member ID to remove
        
    Returns:
        Union[str, List[str]]: Updated member(s) - maintains original format
        
    Example:
        # Remove from single member (results in empty)
        current_members = "user123"
        updated_members = remove_member_from_field(current_members, "user123")
        # Result: []
        
        # Remove from multiple members
        current_members = ["user123", "user456", "user789"]
        updated_members = remove_member_from_field(current_members, "user456")
        # Result: ["user123", "user789"]
    """
    # Convert to list if it's a single string
    if isinstance(current_members, str):
        if current_members == member_id_to_remove:
            return []
        else:
            return current_members
    
    # Filter out the member to remove
    filtered_members = [member_id for member_id in current_members if member_id != member_id_to_remove]
    
    # Return in appropriate format
    if len(filtered_members) == 0:
        return []
    elif len(filtered_members) == 1:
        return filtered_members[0]  # Return as string for single member
    else:
        return filtered_members


# =============================================================================
# DATE FIELD HELPERS
# =============================================================================

def make_date_value(
    date: Union[datetime, str]
) -> str:
    """
    Create a properly formatted value for date custom field.
    
    Args:
        date: Date as datetime object or ISO string
        
    Returns:
        str: Formatted date string for the field
        
    Example:
        from datetime import datetime
        
        # Using datetime object
        date_value = make_date_value(datetime(2025, 12, 31))
        
        # Using ISO string
        date_value = make_date_value("2025-12-31T00:00:00")
        
        custom_field = CustomField(
            id="field_id",
            value=date_value
        )
    """
    if isinstance(date, datetime):
        return date.isoformat()
    return date


def make_date_range_value(
    start_date: Union[datetime, str],
    end_date: Union[datetime, str]
) -> Dict[str, str]:
    """
    Create a properly formatted value for date range custom field.
    
    Args:
        start_date: Start date as datetime object or ISO string
        end_date: End date as datetime object or ISO string
        
    Returns:
        Dict[str, str]: Formatted date range for the field
        
    Example:
        from datetime import datetime
        
        date_range = make_date_range_value(
            start_date=datetime(2025, 1, 1),
            end_date=datetime(2025, 12, 31)
        )
        
        custom_field = CustomField(
            id="field_id",
            value=date_range
        )
    """
    start_str = start_date.isoformat() if isinstance(start_date, datetime) else start_date
    end_str = end_date.isoformat() if isinstance(end_date, datetime) else end_date
    
    return {
        "start": start_str,
        "end": end_str
    }


# =============================================================================
# TEXT AND NUMBER FIELD HELPERS
# =============================================================================

def make_text_value(text: str) -> str:
    """
    Create a properly formatted value for text custom field.
    
    Args:
        text: Text content
        
    Returns:
        str: Formatted text value
        
    Example:
        text_value = make_text_value("Customer: Acme Corporation")
        
        custom_field = CustomField(
            id="field_id",
            value=text_value
        )
    """
    return str(text)


def make_number_value(number: Union[int, float, str]) -> str:
    """
    Create a properly formatted value for number custom field.
    
    Args:
        number: Numeric value as int, float, or string
        
    Returns:
        str: Formatted number value
        
    Example:
        # Integer
        number_value = make_number_value(50000)
        
        # Float
        number_value = make_number_value(99.99)
        
        # String
        number_value = make_number_value("12345")
        
        custom_field = CustomField(
            id="field_id",
            value=number_value
        )
    """
    return str(number)


def make_checkbox_value(checked: bool) -> str:
    """
    Create a properly formatted value for checkbox custom field.
    
    Args:
        checked: Whether the checkbox is checked
        
    Returns:
        str: Formatted checkbox value ("true" or "false")
        
    Example:
        checkbox_value = make_checkbox_value(True)
        
        custom_field = CustomField(
            id="field_id",
            value=checkbox_value
        )
    """
    return "true" if checked else "false"


def make_url_value(url: str) -> str:
    """
    Create a properly formatted value for URL custom field.
    
    Args:
        url: URL string
        
    Returns:
        str: Formatted URL value
        
    Example:
        url_value = make_url_value("https://example.com/design-mockup")
        
        custom_field = CustomField(
            id="field_id",
            value=url_value
        )
    """
    return str(url) 