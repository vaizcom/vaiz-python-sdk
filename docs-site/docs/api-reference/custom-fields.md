---
sidebar_position: 7
---

# Custom Fields

Complete reference for custom field-related methods and models.

## Methods

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

### BoardCustomField

Custom field definition on a board.

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

### CustomField

Custom field value in a task.

```python
class CustomField:
    id: str                             # Field ID
    value: Any                          # Field value (use helper functions)
```

---

### SelectOption

Option for SELECT and MULTI_SELECT custom fields.

```python
class SelectOption:
    id: str                             # Option ID
    label: str                          # Option label
    color: Color                       # Option color
    icon: Icon                         # Option icon
```

---

## Request Models

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

**Example:**
```python
from vaiz import VaizClient, CustomFieldType
from vaiz.helpers.custom_fields import make_text_field

client = VaizClient()

# Using helper function (recommended)
request = make_text_field(
    board_id="board_123",
    name="Description",
    description="Task description"
)

# Or manually
from vaiz.models import CreateBoardCustomFieldRequest

request = CreateBoardCustomFieldRequest(
    board_id="board_123",
    name="Description",
    type=CustomFieldType.TEXT,
    description="Task description"
)

response = client.create_board_custom_field(request)
field = response.custom_field
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

**Example:**
```python
from vaiz.helpers.custom_fields import edit_custom_field_name

# Using helper function (recommended)
request = edit_custom_field_name(
    field_id="field_123",
    board_id="board_123",
    new_name="New Description"
)

response = client.edit_board_custom_field(request)
field = response.custom_field
```

---

## Response Models

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

## Custom Field Types

Available custom field types (see [Enums](./enums#customfieldtype) for details):

- `TEXT` - Single-line text
- `TEXT_MULTI` - Multi-line text
- `NUMBER` - Numeric value
- `DATE` - Date value
- `TIME` - Time value
- `DATETIME` - Date and time value
- `CHECKBOX` - Boolean value
- `SELECT` - Single selection from options
- `MULTI_SELECT` - Multiple selections from options
- `USER` - User selection
- `MULTI_USER` - Multiple user selections
- `URL` - URL value
- `EMAIL` - Email value
- `PHONE` - Phone number value
- `RATING` - Rating value (1-5)
- `PROGRESS` - Progress percentage (0-100)
- `CURRENCY` - Currency value
- `FILES` - File attachments

## Helper Functions

The SDK provides helper functions for creating and editing custom fields. See [Custom Fields Guide](../guides/custom-fields) for usage examples.

### Creation Helpers

```python
from vaiz.helpers.custom_fields import (
    make_text_field,
    make_text_multi_field,
    make_number_field,
    make_date_field,
    make_time_field,
    make_datetime_field,
    make_checkbox_field,
    make_select_field,
    make_multi_select_field,
    make_user_field,
    make_multi_user_field,
    make_url_field,
    make_email_field,
    make_phone_field,
    make_rating_field,
    make_progress_field,
    make_currency_field,
    make_files_field
)
```

### Edit Helpers

```python
from vaiz.helpers.custom_fields import (
    edit_custom_field_name,
    edit_custom_field_description,
    edit_custom_field_visibility,
    add_select_options,
    remove_select_options,
    edit_select_option
)
```

### Value Helpers

```python
from vaiz.helpers.custom_fields import (
    make_custom_field_value,
    make_text_value,
    make_number_value,
    make_date_value,
    make_time_value,
    make_datetime_value,
    make_checkbox_value,
    make_select_value,
    make_multi_select_value,
    make_user_value,
    make_multi_user_value,
    make_url_value,
    make_email_value,
    make_phone_value,
    make_rating_value,
    make_progress_value,
    make_currency_value,
    make_files_value
)
```

---

## See Also

- [Custom Fields Guide](../guides/custom-fields) - Usage examples and patterns
- [Helpers Guide](../guides/helpers) - Helper functions overview
- [Boards](./boards) - Board-related API
- [Tasks](./tasks) - Task-related API
- [Enums](./enums) - CustomFieldType and other enums

