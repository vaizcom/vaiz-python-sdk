---
sidebar_position: 6
---

# Boards

Complete reference for board-related methods and models.

## Methods

### `get_boards`

```python
get_boards() -> BoardsResponse
```

Get all boards in current space.

**Returns:** `BoardsResponse` with list of boards

---

### `get_board`

```python
get_board(board_id: str) -> BoardResponse
```

Get a single board by ID.

**Parameters:**
- `board_id` - Board ID

**Returns:** `BoardResponse` with board data

---

### `create_board_type`

```python
create_board_type(request: CreateBoardTypeRequest) -> CreateBoardTypeResponse
```

Create a new board type (e.g., Bug, Feature).

**Parameters:**
- `request` - Type configuration (board_id, label, icon, color)

**Returns:** `CreateBoardTypeResponse` with created type

---

### `edit_board_type`

```python
edit_board_type(request: EditBoardTypeRequest) -> EditBoardTypeResponse
```

Edit an existing board type.

**Parameters:**
- `request` - Edit request with board_type_id and fields to update

**Returns:** `EditBoardTypeResponse` with updated type

---

### `create_board_group`

```python
create_board_group(request: CreateBoardGroupRequest) -> CreateBoardGroupResponse
```

Create a new board group (column).

**Parameters:**
- `request` - Group configuration (name, board_id)

**Returns:** `CreateBoardGroupResponse` with all board groups

---

### `edit_board_group`

```python
edit_board_group(request: EditBoardGroupRequest) -> EditBoardGroupResponse
```

Edit an existing board group.

**Parameters:**
- `request` - Edit request with board_group_id and fields to update

**Returns:** `EditBoardGroupResponse` with all board groups

---

### `create_board_custom_field`

```python
create_board_custom_field(request: CreateBoardCustomFieldRequest) -> CreateBoardCustomFieldResponse
```

Create a custom field on a board.

**Parameters:**
- `request` - Field configuration (use helper functions like `make_text_field`)

**Returns:** `CreateBoardCustomFieldResponse` with created field

---

### `edit_board_custom_field`

```python
edit_board_custom_field(request: EditBoardCustomFieldRequest) -> EditBoardCustomFieldResponse
```

Edit an existing custom field.

**Parameters:**
- `request` - Edit request (use helper functions like `edit_custom_field_name`)

**Returns:** `EditBoardCustomFieldResponse` with updated field

---

## Models & Interfaces

### Board

```python
class Board:
    id: str                              # Board ID
    name: str                            # Board name
    project: Optional[str]               # Project ID
    groups: Optional[List[BoardGroup]]   # Board groups (columns)
    types_list: Optional[List[BoardType]]  # Task types
    custom_fields: Optional[List[BoardCustomField]]  # Custom fields
    task_order_by_groups: Optional[Dict[str, List[str]]]  # Task ordering
    creator: Optional[str]               # Creator ID
    archiver: Optional[str]              # Archiver ID (if archived)
    deleter: Optional[str]               # Deleter ID (if deleted)
    archived_at: Optional[datetime]      # Archive timestamp
    created_at: Optional[datetime]       # Creation timestamp
    updated_at: Optional[datetime]       # Last update timestamp
    deleted_at: Optional[datetime]       # Deletion timestamp
```

---

### BoardGroup

```python
class BoardGroup:
    id: str                    # Group ID
    name: str                  # Group name
    description: Optional[str] # Description
    limit: Optional[int]       # Task limit for group
    hidden: Optional[bool]     # Hidden status
```

---

### BoardType

```python
class BoardType:
    id: str                    # Type ID
    label: str                 # Type label
    icon: Icon                 # Type icon
    color: Union[str, Color]   # Type color
    description: Optional[str] # Description
    hidden: Optional[bool]     # Hidden status
```

---

### BoardCustomField

```python
class BoardCustomField:
    id: str                         # Field ID
    name: Optional[str]             # Field name
    type: CustomFieldType           # Field type
    description: Optional[str]      # Description
    options: Optional[List[Any]]    # Options (for SELECT type)
    hidden: Optional[bool]          # Hidden status
```

---

### BoardResponse

```python
class BoardResponse:
    type: str                   # Response type ("GetBoard")
    payload: Dict[str, Board]   # Response payload
    
    @property
    def board(self) -> Board:  # Convenience property
        ...
```

---

### BoardsResponse

```python
class BoardsResponse:
    type: str                    # Response type ("GetBoards")
    payload: BoardsPayload       # Response payload
    
    @property
    def boards(self) -> List[Board]:  # Convenience property
        ...
```

---

### BoardsPayload

```python
class BoardsPayload:
    boards: List[Board]         # List of boards
```

---

## Request Models

### CreateBoardTypeRequest

```python
class CreateBoardTypeRequest:
    board_id: str                       # Required - Board ID
    label: str                          # Required - Type label
    icon: Icon                         # Required - Type icon
    color: Color                       # Required - Type color
```

---

### EditBoardTypeRequest

```python
class EditBoardTypeRequest:
    board_type_id: str                  # Required - Type ID
    board_id: str                       # Required - Board ID
    label: Optional[str]                # New label
    icon: Optional[Icon]               # New icon
    color: Optional[Color]             # New color
    description: Optional[str]          # New description
    hidden: Optional[bool]              # Hidden status
```

---

### CreateBoardGroupRequest

```python
class CreateBoardGroupRequest:
    name: str                           # Required - Group name
    board_id: str                       # Required - Board ID
    description: Optional[str]          # Description
```

---

### EditBoardGroupRequest

```python
class EditBoardGroupRequest:
    board_group_id: str                 # Required - Group ID
    board_id: str                       # Required - Board ID
    name: Optional[str]                 # New name
    description: Optional[str]          # New description
    limit: Optional[int]                # Task limit
    hidden: Optional[bool]              # Hidden status
```

---

### CreateBoardCustomFieldRequest

```python
class CreateBoardCustomFieldRequest:
    name: str                           # Required - Field name
    type: CustomFieldType               # Required - Field type
    board_id: str                       # Required - Board ID
    description: Optional[str]          # Description
    hidden: bool                        # Hidden status (default: False)
    options: Optional[List[Any]]        # Options (for SELECT type)
```

---

### EditBoardCustomFieldRequest

```python
class EditBoardCustomFieldRequest:
    field_id: str                       # Required - Field ID
    board_id: str                       # Required - Board ID
    name: Optional[str]                 # New field name
    hidden: Optional[bool]              # Hidden status
    description: Optional[str]          # New description
    options: Optional[List[Any]]        # New options (for SELECT type)
```

---

### CustomField

```python
class CustomField:
    id: str                             # Field ID
    value: Any                          # Field value (use helper functions)
```

---

### SelectOption

```python
class SelectOption:
    id: str                             # Option ID
    label: str                          # Option label
    color: Color                       # Option color
    icon: Icon                         # Option icon
```

---

## Response Models

### CreateBoardTypeResponse

```python
class CreateBoardTypeResponse:
    type: str                           # Response type
    payload: CreateBoardTypePayload     # Response payload
    
    @property
    def board_type(self) -> BoardType: # Convenience property
        ...
```

---

### CreateBoardTypePayload

```python
class CreateBoardTypePayload:
    boardType: BoardType                # Created board type
```

---

### EditBoardTypeResponse

```python
class EditBoardTypeResponse:
    type: str                           # Response type
    payload: EditBoardTypePayload       # Response payload
    
    @property
    def board_type(self) -> BoardType: # Convenience property
        ...
```

---

### EditBoardTypePayload

```python
class EditBoardTypePayload:
    boardType: BoardType                # Edited board type
```

---

### CreateBoardGroupResponse

```python
class CreateBoardGroupResponse:
    type: str                           # Response type
    payload: CreateBoardGroupPayload    # Response payload
    
    @property
    def board_groups(self) -> List[BoardGroup]:  # Convenience property
        ...
```

---

### CreateBoardGroupPayload

```python
class CreateBoardGroupPayload:
    boardGroups: List[BoardGroup]       # All board groups
```

---

### EditBoardGroupResponse

```python
class EditBoardGroupResponse:
    type: str                           # Response type
    payload: EditBoardGroupPayload      # Response payload
    
    @property
    def board_groups(self) -> List[BoardGroup]:  # Convenience property
        ...
```

---

### EditBoardGroupPayload

```python
class EditBoardGroupPayload:
    boardGroups: List[BoardGroup]       # All board groups
```

---

### CreateBoardCustomFieldResponse

```python
class CreateBoardCustomFieldResponse:
    type: str                           # Response type
    payload: CreateBoardCustomFieldPayload  # Response payload
    
    @property
    def custom_field(self) -> BoardCustomField:  # Convenience property
        ...
```

---

### CreateBoardCustomFieldPayload

```python
class CreateBoardCustomFieldPayload:
    customField: BoardCustomField       # Created custom field
```

---

### EditBoardCustomFieldResponse

```python
class EditBoardCustomFieldResponse:
    type: str                           # Response type
    payload: EditBoardCustomFieldPayload  # Response payload
    
    @property
    def custom_field(self) -> BoardCustomField:  # Convenience property
        ...
```

---

### EditBoardCustomFieldPayload

```python
class EditBoardCustomFieldPayload:
    customField: BoardCustomField       # Edited custom field
```

---

## See Also

- [Boards Guide](../guides/boards) - Usage examples and patterns
- [Custom Fields Guide](../guides/custom-fields) - Custom field management
- [Helpers](../guides/helpers) - Helper functions for custom fields
- [Enums](./enums) - Icon, Color, and CustomFieldType enums

