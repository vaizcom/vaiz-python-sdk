---
sidebar_position: 12
---

# Helper Functions

The SDK provides convenient helper functions to simplify common operations.

## Custom Field Helpers

### Field Creation

```python
from vaiz import (
    make_text_field,
    make_number_field,
    make_checkbox_field,
    make_date_field,
    make_member_field,
    make_task_relations_field,
    make_select_field,
    make_url_field
)

# Create any field type easily
text_field = make_text_field(
    name="Customer Name",
    board_id="board_id",
    description="Client name"
)

number_field = make_number_field(
    name="Story Points",
    board_id="board_id"
)

checkbox_field = make_checkbox_field(
    name="Approved",
    board_id="board_id"
)
```

### Field Editing

```python
from vaiz import (
    edit_custom_field_name,
    edit_custom_field_description,
    edit_custom_field_visibility,
    edit_custom_field_complete
)

# Edit specific property
edit = edit_custom_field_name(
    field_id="field_id",
    board_id="board_id",
    new_name="Updated Name"
)

# Edit multiple properties
edit = edit_custom_field_complete(
    field_id="field_id",
    board_id="board_id",
    name="New Name",
    description="New description",
    hidden=False
)
```

### Value Formatting

```python
from vaiz import (
    make_text_value,
    make_number_value,
    make_checkbox_value,
    make_url_value,
    make_date_value,
    make_date_range_value
)
from datetime import datetime

# Format values for CustomField
text = make_text_value("Hello World")
number = make_number_value(42.5)
checkbox = make_checkbox_value(True)
url = make_url_value("https://example.com")
date = make_date_value(datetime(2025, 6, 1))

# Date range
date_range = make_date_range_value(
    start_date=datetime(2025, 1, 1),
    end_date=datetime(2025, 12, 31)
)
```

## Select Field Helpers

### Creating Select Options

```python
from vaiz import make_select_option
from vaiz.models.enums import Color, Icon

# Create option with icon and color
option = make_select_option(
    label="🔥 Critical",
    color=Color.Red,
    icon=Icon.Fire
)
```

### Managing Select Options

```python
from vaiz import (
    add_board_custom_field_select_option,
    remove_board_custom_field_select_option,
    edit_board_custom_field_select_field_option
)

# Add option
add_request = add_board_custom_field_select_option(
    field_id="field_id",
    board_id="board_id",
    new_option=new_option,
    existing_options=current_options
)

# Remove option
remove_request = remove_board_custom_field_select_option(
    field_id="field_id",
    board_id="board_id",
    option_id="option_id",
    existing_options=current_options
)

# Edit option
edit_request = edit_board_custom_field_select_field_option(
    field_id="field_id",
    board_id="board_id",
    option_id="option_id",
    label="Updated Label",
    color=Color.Blue,
    icon=Icon.Star,
    existing_options=current_options
)
```

## Member Field Helpers

```python
from vaiz import (
    make_member_value,
    add_member_to_field,
    remove_member_from_field
)

# Single member
member = make_member_value("user_id")

# Multiple members
members = make_member_value(["user1", "user2", "user3"])

# Add member
updated = add_member_to_field(members, "user4")

# Remove member
final = remove_member_from_field(updated, "user2")
```

## Task Relations Helpers

```python
from vaiz import (
    make_task_relation_value,
    add_task_relation,
    remove_task_relation
)

# Create relations
relations = make_task_relation_value(["task1", "task2", "task3"])

# Add relation
updated = add_task_relation(relations, "task4")

# Remove relation
final = remove_task_relation(updated, "task1")
```

## Complete Example

```python
from vaiz import VaizClient
from vaiz import (
    make_select_field,
    make_select_option,
    make_text_value,
    make_date_value
)
from vaiz.models import CreateTaskRequest, CustomField
from vaiz.models.enums import Color, Icon
from datetime import datetime

client = VaizClient(api_key="...", space_id="...")

# 1. Create custom fields using helpers
priority_options = [
    make_select_option("High", Color.Red, Icon.Flag),
    make_select_option("Medium", Color.Blue, Icon.Circle),
    make_select_option("Low", Color.Green, Icon.Target)
]

select_field = make_select_field(
    name="Priority",
    board_id="board_id",
    options=priority_options
)

field_response = client.create_board_custom_field(select_field)
field_id = field_response.field.id

# 2. Use value helpers when creating tasks
custom_fields = [
    CustomField(
        id=field_id,
        value={"id": priority_options[0].id}  # High priority
    )
]

task = CreateTaskRequest(
    name="Task with Custom Fields",
    board="board_id",
    group="group_id",
    custom_fields=custom_fields
)

response = client.create_task(task)
print(f"✅ Created task with custom fields")
```

## Why Use Helpers?

### ✅ With Helpers (Recommended)

```python
from vaiz import make_text_value, make_date_value
from datetime import datetime

# Clean, readable, type-safe
custom_fields = [
    CustomField(id="text_field", value=make_text_value("Hello")),
    CustomField(id="date_field", value=make_date_value(datetime.now()))
]
```

### ❌ Without Helpers (Manual)

```python
# Error-prone, no validation
custom_fields = [
    CustomField(id="text_field", value={"text": "Hello"}),
    CustomField(id="date_field", value={"date": datetime.now().isoformat()})
]
```

Helpers provide:
- **Type safety** - Correct data structures
- **Validation** - Catches errors early  
- **Consistency** - Uniform API across field types
- **Maintainability** - Code is easier to read and update

## Available Helpers Reference

### Field Creation

| Helper | Field Type | Description |
|--------|------------|-------------|
| `make_text_field` | Text | Text input |
| `make_number_field` | Number | Numeric input |
| `make_checkbox_field` | Checkbox | Boolean checkbox |
| `make_date_field` | Date | Date picker |
| `make_member_field` | Member | User selector |
| `make_task_relations_field` | Relations | Task links |
| `make_select_field` | Select | Dropdown |
| `make_url_field` | URL | URL input |

### Field Editing

| Helper | Purpose |
|--------|---------|
| `edit_custom_field_name` | Update field name |
| `edit_custom_field_description` | Update description |
| `edit_custom_field_visibility` | Show/hide field |
| `edit_custom_field_complete` | Update multiple properties |

### Value Formatting

| Helper | Value Type | Example |
|--------|------------|---------|
| `make_text_value` | Text | `make_text_value("text")` |
| `make_number_value` | Number | `make_number_value(42)` |
| `make_checkbox_value` | Boolean | `make_checkbox_value(True)` |
| `make_url_value` | URL | `make_url_value("https://...")` |
| `make_date_value` | Date | `make_date_value(datetime.now())` |
| `make_date_range_value` | Date Range | `make_date_range_value(start, end)` |
| `make_member_value` | Members | `make_member_value(["user1"])` |
| `make_task_relation_value` | Relations | `make_task_relation_value(["task1"])` |

### Select Options

| Helper | Purpose |
|--------|---------|
| `make_select_option` | Create select option |
| `add_board_custom_field_select_option` | Add option to field |
| `remove_board_custom_field_select_option` | Remove option |
| `edit_board_custom_field_select_field_option` | Edit option |

### Member & Relations

| Helper | Purpose |
|--------|---------|
| `add_member_to_field` | Add user to member field |
| `remove_member_from_field` | Remove user |
| `add_task_relation` | Add task relation |
| `remove_task_relation` | Remove task relation |

## See Also

- [Custom Fields](./custom-fields) - Full custom fields documentation
- [Tasks](./tasks) - Using custom fields in tasks
- [Examples](../patterns/introduction) - Practical examples

