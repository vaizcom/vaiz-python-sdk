---
sidebar_position: 7
---

# Projects

Manage projects in your workspace.

## Get All Projects

```python
response = client.get_projects()

for project in response.projects:
    print(f"📁 {project.name}")
    print(f"   Color: {project.color}")
    print(f"   Boards: {len(project.boards)}")
```

## Get Single Project

```python
response = client.get_project("project_id")
project = response.project

print(f"Project: {project.name}")
print(f"Description: {project.description}")
print(f"Boards: {project.boards}")
```

## Project Model

```python
class Project:
    id: str                      # Project ID
    name: str                    # Project name
    color: str                   # Color enum
    description: Optional[str]   # Description
    boards: List[str]            # Board IDs
    created_at: datetime         # Creation date
    updated_at: datetime         # Last update
```

## Project Colors

Projects support `Color` enum values:

```python
from vaiz.models.enums import Color

# Using enum
project_color = Color.Blue
```

:::tip Color Options
The `color` field accepts predefined enum values from the `Color` enum.
:::

## Working with Project Boards

```python
response = client.get_project("project_id")
project = response.project

# Get all boards in project
for board_id in project.boards:
    board = client.get_board(board_id)
    print(f"Board: {board.payload['board']['name']}")
```

## Filtering Tasks by Project

```python
from vaiz.models import GetTasksRequest

# Get all tasks in project
request = GetTasksRequest(
    project="project_id",
    completed=False,
    limit=50
)

response = client.get_tasks(request)
print(f"Found {len(response.payload.tasks)} tasks")
```

## Complete Example

```python
from vaiz import VaizClient

client = VaizClient(api_key="...", space_id="...")

# List all projects
projects = client.get_projects()
print("Projects:")
for project in projects.projects:
    print(f"  - {project.name} ({project.color})")
    
    # Get project details
    details = client.get_project(project.id)
    print(f"    Boards: {len(details.project.boards)}")
```

## See Also

- [Boards API](./boards) - Board management
- [Tasks API](./tasks) - Task operations
- [Examples](../patterns/introduction) - More examples
