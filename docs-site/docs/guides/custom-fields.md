---
sidebar_position: 7
title: Working with Custom Fields — Text, Numbers, Dates & More | Vaiz Python SDK
description: Learn how to create and manage custom fields on tasks using the Vaiz Python SDK. Supports text, number, date, select, and multi-select field types.
---

# Custom Fields

Add custom data fields to your tasks.

## Available Field Types

See [`CustomFieldType`](../api-reference/enums#customfieldtype) for all available field types.

## Creating Custom Fields

Use helper functions for easy field creation:

### Text Field

```python
from vaiz import make_text_field

text_field = make_text_field(
    name="Customer Name",
    board_id="board_id",
    description="Client name for this task"
)

response = client.create_board_custom_field(text_field)
```

### Number Field

```python
from vaiz import make_number_field

number_field = make_number_field(
    name="Story Points",
    board_id="board_id",
    description="Task complexity estimate"
)

response = client.create_board_custom_field(number_field)
```

### Date Field

```python
from vaiz import make_date_field

date_field = make_date_field(
    name="Launch Date",
    board_id="board_id",
    description="Planned launch date"
)

response = client.create_board_custom_field(date_field)
```

### Select Field

```python
from vaiz import make_select_field, make_select_option
from vaiz.models.enums import Color, Icon

# Create options
options = [
    make_select_option("🔥 Critical", Color.Red, Icon.Fire),
    make_select_option("⚡ High", Color.Orange, Icon.Flag),
    make_select_option("📋 Medium", Color.Blue, Icon.Circle),
    make_select_option("🌱 Low", Color.Green, Icon.Target)
]

# Create select field
select_field = make_select_field(
    name="Priority Level",
    board_id="board_id",
    options=options,
    description="Task priority classification"
)

response = client.create_board_custom_field(select_field)
```

### Other Field Types

```python
from vaiz import (
    make_checkbox_field,
    make_member_field,
    make_task_relations_field,
    make_url_field
)

# Checkbox
checkbox = make_checkbox_field(
    name="Approved",
    board_id="board_id"
)

# Member selector
member = make_member_field(
    name="Reviewer",
    board_id="board_id"
)

# Task relations
relations = make_task_relations_field(
    name="Related Tasks",
    board_id="board_id"
)

# URL
url = make_url_field(
    name="Documentation Link",
    board_id="board_id"
)
```

## Editing Custom Fields

### Edit Field Name

```python
from vaiz import edit_custom_field_name

edit = edit_custom_field_name(
    field_id="field_id",
    board_id="board_id",
    new_name="🎯 Updated Field Name"
)

client.edit_board_custom_field(edit)
```

### Edit Field Description

```python
from vaiz import edit_custom_field_description

edit = edit_custom_field_description(
    field_id="field_id",
    board_id="board_id",
    new_description="Updated field description"
)

client.edit_board_custom_field(edit)
```

### Edit Multiple Properties

```python
from vaiz import edit_custom_field_complete

edit = edit_custom_field_complete(
    field_id="field_id",
    board_id="board_id",
    name="New Name",
    description="New description",
    hidden=False
)

client.edit_board_custom_field(edit)
```

## Managing Select Options

### Add Option

```python
from vaiz import add_board_custom_field_select_option, make_select_option
from vaiz.models.enums import Color, Icon

# Create new option
new_option = make_select_option("🚨 Emergency", Color.Magenta, Icon.Crown)

# Add to field
add_request = add_board_custom_field_select_option(
    field_id="field_id",
    board_id="board_id",
    new_option=new_option,
    existing_options=current_options
)

client.edit_board_custom_field(add_request)
```

### Remove Option

```python
from vaiz import remove_board_custom_field_select_option

remove_request = remove_board_custom_field_select_option(
    field_id="field_id",
    board_id="board_id",
    option_id="option_id",
    existing_options=current_options
)

client.edit_board_custom_field(remove_request)
```

### Edit Option

```python
from vaiz import edit_board_custom_field_select_field_option

edit_request = edit_board_custom_field_select_field_option(
    field_id="field_id",
    board_id="board_id",
    option_id="option_id",
    label="Updated Label",
    color=Color.Blue,
    icon=Icon.Star,
    existing_options=current_options
)

client.edit_board_custom_field(edit_request)
```

## Using Custom Fields in Tasks

### Set Field Values

```python
from vaiz import make_text_value, make_date_value, make_checkbox_value
from vaiz.models import CreateTaskRequest, CustomField
from datetime import datetime

custom_fields = [
    CustomField(
        id="text_field_id",
        value=make_text_value("Acme Corp")
    ),
    CustomField(
        id="date_field_id",
        value=make_date_value(datetime(2025, 6, 1))
    ),
    CustomField(
        id="checkbox_field_id",
        value=make_checkbox_value(True)
    )
]

task = CreateTaskRequest(
    name="Task with Custom Fields",
    board="board_id",
    group="group_id",
    custom_fields=custom_fields
)

response = client.create_task(task)
```

## Value Helper Functions

### Basic Values

```python
from vaiz import (
    make_text_value,
    make_number_value,
    make_checkbox_value,
    make_url_value
)

text = make_text_value("Hello World")
number = make_number_value(42)
checkbox = make_checkbox_value(True)
url = make_url_value("https://example.com")
```

### Date Values

```python
from vaiz import make_date_value, make_date_range_value
from datetime import datetime

# Single date
date = make_date_value(datetime(2025, 6, 1))

# Date range
date_range = make_date_range_value(
    start_date=datetime(2025, 1, 1),
    end_date=datetime(2025, 12, 31)
)
```

### Member Values

```python
from vaiz import make_member_value, add_member_to_field, remove_member_from_field

# Single member
member = make_member_value("user_id")

# Multiple members
members = make_member_value(["user1", "user2", "user3"])

# Add member
updated = add_member_to_field(members, "user4")

# Remove member
final = remove_member_from_field(updated, "user2")
```

### Task Relations

```python
from vaiz import make_task_relation_value, add_task_relation, remove_task_relation

# Create relations
relations = make_task_relation_value(["task1", "task2", "task3"])

# Add relation
updated = add_task_relation(relations, "task4")

# Remove relation
final = remove_task_relation(updated, "task1")
```

## Complete Example

```python
from vaiz import VaizClient, make_select_field, make_select_option
from vaiz.models import CreateTaskRequest, CustomField
from vaiz.models.enums import Color, Icon

client = VaizClient(api_key="...", space_id="...")

# 1. Create custom field
priority_options = [
    make_select_option("High", Color.Red, Icon.Flag),
    make_select_option("Medium", Color.Blue, Icon.Circle),
    make_select_option("Low", Color.Green, Icon.Target)
]

field = make_select_field(
    name="Priority",
    board_id="board_id",
    options=priority_options
)

field_response = client.create_board_custom_field(field)
field_id = field_response.field.id

# 2. Create task with custom field value
task = CreateTaskRequest(
    name="Important Task",
    board="board_id",
    group="group_id",
    custom_fields=[
        CustomField(
            id=field_id,
            value={"id": priority_options[0].id}  # High priority
        )
    ]
)

client.create_task(task)
```

## See Also

- [Boards API](./boards) - Board management
- [Tasks API](./tasks) - Using custom fields in tasks
- [Examples](../patterns/introduction) - More custom field examples

