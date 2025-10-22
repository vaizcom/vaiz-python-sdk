---
sidebar_position: 6
---

# Boards

Manage boards, types, and groups.

## Getting Boards

### All Boards

```python
response = client.get_boards()

for board in response.boards:
    print(f"📋 {board.name}")
```

### Single Board

```python
response = client.get_board("board_id")
board = response.board

print(f"Board: {board.name}")
print(f"Groups: {len(board.groups or [])}")
print(f"Types: {len(board.types_list or [])}")
```

## Board Types

Types categorize tasks (e.g., Bug, Feature, Task).

### Create Type

```python
from vaiz.models import CreateBoardTypeRequest
from vaiz.models.enums import Icon, Color

request = CreateBoardTypeRequest(
    board_id="board_id",
    label="Bug",
    icon=Icon.Bug,
    color=Color.Red,
    description="Bug reports and issues"
)

response = client.create_board_type(request)
print(f"✅ Created type: {response.board_type.label}")
```

### Edit Type

```python
from vaiz.models import EditBoardTypeRequest

request = EditBoardTypeRequest(
    board_type_id="type_id",
    board_id="board_id",
    label="Critical Bug",
    color=Color.Magenta,
    description="High priority bugs",
    hidden=False
)

response = client.edit_board_type(request)
```

### Common Type Examples

```python
from vaiz.models.enums import Icon, Color

# Bug type
bug_type = CreateBoardTypeRequest(
    board_id="board_id",
    label="🐛 Bug",
    icon=Icon.Bug,
    color=Color.Red
)

# Feature type
feature_type = CreateBoardTypeRequest(
    board_id="board_id",
    label="✨ Feature",
    icon=Icon.Star,
    color=Color.Blue
)

# Task type
task_type = CreateBoardTypeRequest(
    board_id="board_id",
    label="📋 Task",
    icon=Icon.Checkbox,
    color=Color.Green
)
```

## Board Groups

Groups organize tasks in columns (e.g., To Do, In Progress, Done).

### Create Group

```python
from vaiz.models import CreateBoardGroupRequest

request = CreateBoardGroupRequest(
    name="In Review",
    board_id="board_id",
    description="Tasks pending code review"
)

response = client.create_board_group(request)
print(f"✅ Created group: {request.name}")
```

### Edit Group

```python
from vaiz.models import EditBoardGroupRequest

request = EditBoardGroupRequest(
    board_group_id="group_id",
    board_id="board_id",
    name="Code Review",
    description="Pending review by team",
    limit=10,        # Max tasks in group
    hidden=False     # Visible in board
)

response = client.edit_board_group(request)
```

### Common Group Structure

```python
# Typical Kanban board groups
groups = [
    "📝 Backlog",
    "🎯 To Do",
    "⏳ In Progress",
    "👀 In Review",
    "✅ Done"
]

for group_name in groups:
    request = CreateBoardGroupRequest(
        name=group_name,
        board_id="board_id"
    )
    client.create_board_group(request)
```

## Complete Board Setup

```python
from vaiz import VaizClient
from vaiz.models import (
    CreateBoardTypeRequest,
    CreateBoardGroupRequest
)
from vaiz.models.enums import Icon, Color

client = VaizClient(api_key="...", space_id="...")

board_id = "board_id"

# Create types
types = [
    ("Bug", Icon.Bug, Color.Red),
    ("Feature", Icon.Star, Color.Blue),
    ("Task", Icon.Checkbox, Color.Green),
    ("Documentation", Icon.Document, Color.Gold),
]

for label, icon, color in types:
    request = CreateBoardTypeRequest(
        board_id=board_id,
        label=label,
        icon=icon,
        color=color
    )
    response = client.create_board_type(request)
    print(f"✅ Created type: {label}")

# Create groups
groups = [
    ("Backlog", "Tasks to be prioritized"),
    ("To Do", "Ready to start"),
    ("In Progress", "Currently being worked on"),
    ("Review", "Pending review"),
    ("Done", "Completed tasks"),
]

for name, description in groups:
    request = CreateBoardGroupRequest(
        name=name,
        board_id=board_id,
        description=description
    )
    response = client.create_board_group(request)
    print(f"✅ Created group: {name}")
```

## Working with Board Structure

### Get Board Details

```python
response = client.get_board("board_id")
board = response.board

print(f"Board: {board.name}")
print("\nGroups:")
for group in board.groups or []:
    print(f"  - {group.name}")

print("\nTypes:")
for type_item in board.types_list or []:
    print(f"  - {type_item.label} ({type_item.color})")
```

### Create Tasks with Types

```python
from vaiz.models import CreateTaskRequest

# Get board to find type IDs
board_response = client.get_board("board_id")
board = board_response.board

# Find bug type
bug_type = next(t for t in board.types_list if t.label == "Bug")

# Create bug task
task = CreateTaskRequest(
    name="Fix login issue",
    board="board_id",
    group="group_id",
    types=[bug_type.id]  # Use .id attribute, not dictionary access
)

response = client.create_task(task)
```

## See Also

- [Custom Fields](./custom-fields) - Add custom data to tasks
- [Tasks API](./tasks) - Task operations
- [Examples](../patterns/introduction) - More examples
