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
    project="project_id",
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

## Task Descriptions

Tasks store descriptions as structured JSON documents. The SDK provides convenient methods to work with descriptions directly from Task objects.

### Get Task Description

```python
# Get from task object
task_response = client.get_task("PRJ-123")
task = task_response.task
document_id = task.document

# Get document content
description = client.get_document_body(document_id)
print(description)  # JSON structure
```

### Update Task Description

Replace task description completely:

```python
# Get task
task_response = client.get_task("PRJ-123")
document_id = task_response.task.document

# Update description
new_content = """
# Updated Description

This completely replaces the previous content.

## Features
- Complete replacement
- Plain text support
- Direct API access
"""

client.replace_document(
    document_id=document_id,
    description=new_content
)
```

### Using Task Helper Methods

The Task model provides convenient helper methods:

```python
# Get task
task_response = client.create_task(task)
task_obj = task_response.task

# Get description using helper
description = task_obj.get_task_description(client)
print(description)

# Update description using helper
task_obj.update_task_description(
    client, 
    "New task description content"
)
```

### Full Workflow Example

```python
from vaiz.models import CreateTaskRequest

# 1. Create task with initial description
task = CreateTaskRequest(
    name="Documentation Task",
    board="board_id",
    group="group_id",
    project="project_id"
)

response = client.create_task(
    task,
    description="Initial task description"
)

# 2. Get task object
task_obj = response.task

# 3. Update description later
task_obj.update_task_description(
    client,
    "Updated task description with more details"
)

# 4. Read current content
content = task_obj.get_task_description(client)
print(content)
```

### Programmatic Description Updates

```python
from datetime import datetime

def add_status_update(task_id: str, status: str):
    """Append status update to task description"""
    
    # Get task
    task = client.get_task(task_id)
    doc_id = task.payload["task"]["document"]
    
    # Get current content
    current = client.get_document_body(doc_id)
    
    # Add status update
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    new_content = f"""
{current}

---
**Status Update ({timestamp})**: {status}
"""
    
    client.replace_document(doc_id, new_content)

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
- [Examples](../examples) - Code examples

