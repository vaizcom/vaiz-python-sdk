---
sidebar_position: 2
sidebar_label: Tasks
title: Working with Tasks — Complete Guide | Vaiz Python SDK
description: Learn how to create, edit, and manage tasks using the Vaiz Python SDK. Includes custom fields, file attachments, priorities, assignees, and rich-text descriptions.
---

# Tasks

Complete reference for working with tasks in the Vaiz SDK.

## Creating Tasks

### Basic Task

```python
from vaiz import VaizClient
from vaiz.models import CreateTaskRequest, TaskPriority

client = VaizClient(api_key="...", space_id="...")

task = CreateTaskRequest(
    name="Implement user authentication",
    board="board_id",
    group="group_id",  # Optional - specify if board has groups
    priority=TaskPriority.High
)

response = client.create_task(task)
print(f"Created: {response.task.id}")
```

:::tip Optional Fields
- `group` - Optional if board doesn't use groups
- `project` - Optional, API determines from board
:::

### Task with Description

Use the `description` parameter for convenience:

```python
task = CreateTaskRequest(
    name="Task Name",
    board="board_id",
    group="group_id"
)

response = client.create_task(
    task,
    description="Task description content"
)
```

### Task with Dates

```python
from datetime import datetime

task = CreateTaskRequest(
    name="Project Milestone",
    board="board_id",
    group="group_id",
    due_start=datetime(2025, 2, 1, 9, 0),
    due_end=datetime(2025, 2, 15, 17, 0)
)

response = client.create_task(task)
```

### Task with Files (Easy Way)

Upload and attach file in one step:

```python
from vaiz.models import TaskUploadFile
from vaiz.models.enums import UploadFileType

task = CreateTaskRequest(
    name="Review Document",
    board="board_id",
    group="group_id"
)

# File automatically uploaded and attached
response = client.create_task(
    task,
    file=TaskUploadFile(path="doc.pdf", type=UploadFileType.Pdf)
)
```

### Task with Files (Manual Way)

Or upload manually and create TaskFile:

```python
from vaiz.models import TaskFile

# Upload file
file_response = client.upload_file("doc.pdf", UploadFileType.Pdf)

# Create TaskFile
task_file = TaskFile(
    url=file_response.file.url,
    name=file_response.file.name,
    ext=file_response.file.ext,
    id=file_response.file.id,
    type=file_response.file.type,
    dimension=file_response.file.dimension
)

# Create task
task = CreateTaskRequest(
    name="Review Document",
    board="board_id",
    group="group_id",
    files=[task_file]
)

response = client.create_task(task)
```

### Task with Blockers

Create tasks with dependency relationships:

```python
# Task that is blocked by another task
task = CreateTaskRequest(
    name="Implement Feature",
    board="board_id",
    group="group_id",
    blockers=["design_task_id"]  # This task depends on design task
)

response = client.create_task(task)
```

Learn more in [Task Blockers](./blockers) documentation.

## Updating Tasks

```python
from vaiz.models import EditTaskRequest

edit = EditTaskRequest(
    task_id="task_id",
    name="Updated Name",
    completed=True,
    priority=TaskPriority.High
)

response = client.edit_task(edit)
```

## Getting Tasks

### Single Task

```python
response = client.get_task("PRJ-123")
task = response.task
```

### Multiple Tasks

```python
from vaiz.models import GetTasksRequest

request = GetTasksRequest(
    completed=False,
    assignees=["user_id"],
    limit=50
)

response = client.get_tasks(request)
for task in response.payload.tasks:
    print(f"{task.hrid}: {task.name}")
```

## Moving Tasks Between Groups

To move tasks between board groups, use the `move_tasks` method. This is the correct way to change a task's group — `edit_task` does not support group changes.

### Move a single task

```python
from vaiz.models import MoveTaskItem, MoveTasksRequest

move_request = MoveTasksRequest(
    moves=[
        MoveTaskItem(
            task_id="task_id",
            to_group_id="target_group_id",
            to_index=0  # Position in the target group
        )
    ]
)

response = client.move_tasks(move_request)
print(f"Moved: {response.payload.success_ids}")
print(f"Failed: {response.payload.failed_ids}")
```

### Move multiple tasks at once

```python
move_request = MoveTasksRequest(
    moves=[
        MoveTaskItem(task_id="task_1", to_group_id="group_b", to_index=0),
        MoveTaskItem(task_id="task_2", to_group_id="group_b", to_index=1),
        MoveTaskItem(task_id="task_3", to_group_id="group_c", to_index=0),
    ]
)

response = client.move_tasks(move_request)
```

:::tip
You can move tasks to different groups in a single request. Each move specifies its own target group and position.
:::

## Task Descriptions

Every task stores its description as a document (the `task.document` field). The recommended way to read and write descriptions is Markdown — it is converted to native rich blocks on the server.

### Get Task Description

```python
# Get from task object
task_response = client.get_task("PRJ-123")
task = task_response.task
document_id = task.document

# Get description as Markdown
description = client.get_markdown_document(document_id)
print(description)
```

### Update Task Description

Replace task description completely:

```python
# Get task
task_response = client.get_task("PRJ-123")
document_id = task_response.task.document

# Update description with Markdown
new_content = """
# Updated Description

This completely replaces the previous content.

## Features
- **Rich formatting** with Markdown
- Lists, tables, code blocks
- Links and checklists
"""

client.replace_markdown_document(document_id, new_content)
```

### Appending Content

Add content to the end of the description without removing existing content:

```python
client.append_markdown_document(
    document_id,
    "## Update\n\nAdditional notes"
)
```

:::warning Deprecated
The non-Markdown write methods `replace_document()`, `replace_json_document()`, `append_document()`, `append_json_document()`, and the `Task.update_task_description()` helper are deprecated and emit a `DeprecationWarning`. Use the Markdown methods above instead.
:::

### Programmatic Description Updates

```python
from datetime import datetime

def add_status_update(task_id: str, status: str):
    """Append status update to task description"""
    
    # Get task
    task_response = client.get_task(task_id)
    doc_id = task_response.task.document
    
    # Append status update
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    client.append_markdown_document(
        doc_id,
        f"---\n**Status Update ({timestamp})**: {status}"
    )

# Usage
add_status_update("PRJ-123", "Design phase completed")
```

:::info Advanced Usage
If you need more control, you can work directly with the document ID from `task.document` field using the [Documents API](./documents) methods.
:::

## See Also

- [Task Blockers](./blockers) - Manage task dependencies
- [Files](./files) - File attachments
- [Comments](./comments) - Task discussions
- [Documents](./documents) - Document lists and management
- [Examples](../patterns/introduction) - Code examples

