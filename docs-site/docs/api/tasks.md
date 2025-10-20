---
sidebar_position: 2
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
    group="group_id",
    priority=TaskPriority.High
)

response = client.create_task(task)
print(f"Created: {response.task.id}")
```

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
from vaiz.models.enums import EUploadFileType

task = CreateTaskRequest(
    name="Review Document",
    board="board_id",
    group="group_id"
)

# File automatically uploaded and attached
response = client.create_task(
    task,
    file=TaskUploadFile(path="doc.pdf", type=EUploadFileType.Pdf)
)
```

### Task with Files (Manual Way)

Or upload manually and create TaskFile:

```python
from vaiz.models import TaskFile

# Upload file
file_response = client.upload_file("doc.pdf", EUploadFileType.Pdf)

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
task = response.payload["task"]
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

## Request Models

### CreateTaskRequest

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | `str` | Yes | Task name |
| `board` | `str` | Yes | Board ID |
| `group` | `str` | Yes | Group ID |
| `project` | `str` | Yes | Project ID |
| `description` | `str` | No | Task description |
| `priority` | `TaskPriority` | No | Priority (0-3, default: 1) |
| `completed` | `bool` | No | Completion status (default: False) |
| `assignees` | `List[str]` | No | Assignee user IDs |
| `types` | `List[str]` | No | Task type IDs |
| `parent_task` | `str` | No | Parent task ID (for subtasks) |
| `subtasks` | `List[str]` | No | Subtask IDs |
| `milestones` | `List[str]` | No | Milestone IDs |
| `due_start` | `datetime` | No | Start date |
| `due_end` | `datetime` | No | Due date |
| `custom_fields` | `List[CustomField]` | No | Custom field values |
| `files` | `List[TaskFile]` | No | Attached files |

### TaskPriority Enum

```python
TaskPriority.None_     # 0
TaskPriority.General   # 1 (default)
TaskPriority.Medium    # 2
TaskPriority.High      # 3
```

## See Also

- [Files API](./files)
- [Comments API](./comments)
- [Examples](../examples)

