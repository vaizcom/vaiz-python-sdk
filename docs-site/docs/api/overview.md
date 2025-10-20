---
sidebar_position: 1
---

# API Overview

The Vaiz SDK provides a comprehensive Python interface to the Vaiz platform API.

## Main Client

All API interactions go through the `VaizClient` class:

```python
from vaiz import VaizClient

client = VaizClient(
    api_key="your_api_key",
    space_id="your_space_id"
)
```

## API Categories

### Tasks

Create, read, update tasks with full support for:
- Custom fields
- File attachments  
- Assignees and priorities
- Due dates and milestones

```python
from vaiz.models import CreateTaskRequest

task = CreateTaskRequest(
    name="New Task",
    board="board_id",
    group="group_id"
)
response = client.create_task(task)
```

[Learn more about Tasks →](./tasks)

### Projects & Boards

Manage projects and boards:

```python
# Get all projects
projects = client.get_projects()

# Get specific board
board = client.get_board("board_id")
```

### Milestones

Track progress with milestones:

```python
from vaiz.models import CreateMilestoneRequest

milestone = CreateMilestoneRequest(
    name="Q1 2025",
    board="board_id",
    project="project_id"
)
response = client.create_milestone(milestone)
```

[Learn more about Milestones →](./milestones)

### Comments

Full comment system with HTML, files, and reactions:

```python
# Post comment
response = client.post_comment(
    document_id="document_id",
    content="<p>My comment</p>"
)

# Add reaction
client.add_reaction(
    comment_id=response.comment.id,
    reaction=CommentReactionType.THUMBS_UP
)
```

[Learn more about Comments →](./comments)

### Files

Upload and manage files:

```python
from vaiz.models.enums import EUploadFileType

# Upload local file
response = client.upload_file(
    "/path/to/file.pdf",
    file_type=EUploadFileType.Pdf
)

# Upload from URL
response = client.upload_file_from_url(
    "https://example.com/image.png"
)
```

[Learn more about Files →](./files)

## Response Format

All API methods return typed response objects:

```python
response = client.create_task(task)

# Access data with full type support
task_id = response.task.id
task_name = response.task.name
created_at = response.task.created_at  # datetime object
```

## Error Handling

The SDK uses standard Python exceptions:

```python
from requests.exceptions import HTTPError

try:
    response = client.get_task("invalid_id")
except HTTPError as e:
    if e.response.status_code == 404:
        print("Task not found")
    elif e.response.status_code == 401:
        print("Authentication error")
    else:
        print(f"Error: {e}")
```

## Pagination

For list endpoints, use pagination parameters:

```python
from vaiz.models import GetTasksRequest

# First page
request = GetTasksRequest(limit=50, skip=0)
response = client.get_tasks(request)

# Second page
request = GetTasksRequest(limit=50, skip=50)
response = client.get_tasks(request)
```

## DateTime Handling

All datetime fields automatically convert between Python `datetime` and ISO strings:

```python
from datetime import datetime

# Input: Python datetime
task = CreateTaskRequest(
    name="Task",
    due_end=datetime(2025, 12, 31)
)

# Output: Python datetime
response = client.create_task(task)
print(response.task.due_end.year)  # 2025
```

## Next Steps

- [Tasks API](./tasks) - Complete task management
- [Comments API](./comments) - Comment system
- [Files API](./files) - File upload and management
- [Milestones API](./milestones) - Milestone tracking

