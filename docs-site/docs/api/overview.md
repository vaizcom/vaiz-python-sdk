---
sidebar_position: 1
---

# API Overview

Complete overview of the Vaiz SDK capabilities and API structure.

## Client Initialization

All API interactions go through the `VaizClient` class:

```python
from vaiz import VaizClient

client = VaizClient(
    api_key="your_api_key",
    space_id="your_space_id",
    verify_ssl=True,      # Default: True
    base_url="https://..."  # Optional
)
```

## Core Concepts

### Automatic Type Conversion

The SDK automatically handles type conversions:

```python
from datetime import datetime
from vaiz.models import CreateTaskRequest

# Input: Python datetime objects
task = CreateTaskRequest(
    name="Task",
    due_end=datetime(2025, 12, 31, 17, 0)
)

# SDK converts to ISO strings for API
response = client.create_task(task)

# Output: Python datetime objects
print(response.task.created_at)     # datetime object
print(response.task.due_end.year)   # 2025
```

### Type Safety with Enums

Use enums for type-safe values:

```python
from vaiz.models import TaskPriority
from vaiz.models.enums import Icon, Color, EUploadFileType

priority = TaskPriority.High           # 3
icon = Icon.Bug                       # "Bug"
color = Color.Red                     # "Red"
file_type = EUploadFileType.Image      # "image"
```

### Pydantic Models

All requests and responses use Pydantic v2 for validation:

```python
from vaiz.models import CreateTaskRequest

# Full IDE autocomplete and validation
task = CreateTaskRequest(
    name="Task",           # Required - will error if missing
    board="board_id",      # Required
    group="group_id",      # Required
    priority=TaskPriority.High,  # Optional
    assignees=["user_id"]  # Optional
)

# Automatic validation on creation
# Invalid data raises ValidationError
```

## Common Patterns

### Error Handling

```python
from requests.exceptions import HTTPError

try:
    response = client.create_task(task)
except HTTPError as e:
    if e.response.status_code == 400:
        print("Validation error:", e.response.json())
    elif e.response.status_code == 401:
        print("Authentication failed")
    elif e.response.status_code == 404:
        print("Resource not found")
    else:
        print(f"Error: {e}")
```

### Pagination

```python
from vaiz.models import GetTasksRequest

all_tasks = []
skip = 0

while True:
    request = GetTasksRequest(
        completed=False,
        limit=50,
        skip=skip
    )
    
    response = client.get_tasks(request)
    tasks = response.payload.tasks
    
    if not tasks:
        break
    
    all_tasks.extend(tasks)
    skip += 50
    
    if len(tasks) < 50:
        break  # Last page

print(f"Total: {len(all_tasks)} tasks")
```

### Working with Dates

```python
from datetime import datetime, timedelta

# Create with dates
task = CreateTaskRequest(
    name="Sprint Task",
    due_start=datetime.now(),
    due_end=datetime.now() + timedelta(weeks=2)
)

response = client.create_task(task)

# Use datetime methods
days_left = (response.task.due_end - datetime.now()).days
print(f"Days remaining: {days_left}")
```

### Batch Operations

```python
# Create multiple tasks
tasks_data = [
    ("Design mockups", TaskPriority.High),
    ("Implement API", TaskPriority.High),
    ("Write tests", TaskPriority.Medium),
]

for name, priority in tasks_data:
    task = CreateTaskRequest(
        name=name,
        board="board_id",
        group="group_id",
        priority=priority
    )
    client.create_task(task)
```

## Response Structure

All methods return typed response objects:

```python
response = client.create_task(task)

# Type-safe access
task_id = response.task.id              # str
task_name = response.task.name          # str
created_at = response.task.created_at   # datetime
priority = response.task.priority       # int
```

## Field Naming Conventions

The SDK uses Python naming (snake_case) while the API uses camelCase:

```python
# You write:
task = CreateTaskRequest(
    due_start=datetime.now(),  # snake_case
    due_end=datetime.now()
)

# SDK sends to API:
{
    "dueStart": "2025-01-01T00:00:00",  # camelCase
    "dueEnd": "2025-01-01T23:59:59"
}

# You receive:
response.task.due_start  # snake_case again
```

All conversion is automatic via Pydantic field aliases.

## Best Practices

### Use Environment Variables

```python
# ✅ Good
from dotenv import load_dotenv
import os

load_dotenv()
client = VaizClient(
    api_key=os.getenv("VAIZ_API_KEY"),
    space_id=os.getenv("VAIZ_SPACE_ID")
)

# ❌ Bad
client = VaizClient(
    api_key="hardcoded_key",  # Never commit API keys!
    space_id="hardcoded_id"
)
```

### Use Type Hints

```python
# ✅ Good
from vaiz.models import Task
from typing import List

def get_high_priority_tasks() -> List[Task]:
    request = GetTasksRequest(priority=[3])
    response = client.get_tasks(request)
    return response.payload.tasks

# ❌ Bad
def get_tasks():  # No type hints
    request = GetTasksRequest(priority=[3])
    return client.get_tasks(request).payload.tasks
```

### Handle Errors

```python
# ✅ Good
try:
    response = client.create_task(task)
    return response.task
except HTTPError as e:
    logger.error(f"Failed to create task: {e}")
    return None

# ❌ Bad
response = client.create_task(task)  # Can crash
return response.task
```

### Use Helper Functions

The SDK provides [helper functions](./helpers) for common operations:

```python
from vaiz import make_text_value, make_date_value, make_select_option

# Clean, type-safe value creation
value = make_text_value("Hello")
date = make_date_value(datetime.now())
option = make_select_option("High", Color.Red, Icon.Flag)
```

[See all helper functions →](./helpers)

## API Reference

Explore detailed documentation for each API category:

- [Tasks](./tasks) - Create, read, update tasks
- [Comments](./comments) - Comments, reactions, and replies
- [Files](./files) - File uploads and attachments
- [Milestones](./milestones) - Track progress
- [Boards](./boards) - Board types and groups
- [Custom Fields](./custom-fields) - Extend tasks with custom data
- [Projects](./projects) - Project management
- [Profile](./profile) - User information
- [Documents](./documents) - Task descriptions
- [History Events](./history) - Change tracking
- [Task Blockers](./blockers) - Manage task dependencies
- [Helper Functions](./helpers) - Utility functions

Or check out [Examples](../examples) for ready-to-use code.
