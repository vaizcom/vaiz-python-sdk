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

## Models

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

## See Also

- [Boards Guide](../guides/boards) - Usage examples and patterns
- [Custom Fields Guide](../guides/custom-fields) - Custom field management
- [Helpers](../guides/helpers) - Helper functions for custom fields
- [Enums](./enums) - Icon, Color, and CustomFieldType enums

