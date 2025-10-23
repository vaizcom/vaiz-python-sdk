---
sidebar_position: 7
sidebar_label: Projects
title: Working with Projects — Organize Your Workspace | Vaiz Python SDK
description: Learn how to retrieve and manage projects and lists in your Vaiz workspace using the Python SDK. Complete guide with examples.
---

# Projects

Manage projects in your workspace.

## Get All Projects

```python
response = client.get_projects()

for project in response.projects:
    print(f"📁 {project.name}")
    print(f"   Slug: {project.slug}")
    print(f"   Color: {project.color}")
```

## Get Single Project

```python
response = client.get_project("project_id")
project = response.project

print(f"Project: {project.name}")
print(f"Description: {project.description}")
print(f"Slug: {project.slug}")
print(f"Team: {len(project.team)} members")
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

To get boards in a project, use `get_boards()`:

```python
# Get all boards in workspace
boards_response = client.get_boards()

# Filter boards by project
project_id = "project_id"
project_boards = [
    board for board in boards_response.boards 
    if board.project == project_id
]

for board in project_boards:
    print(f"Board: {board.name}")
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
    print(f"  - {project.name} ({project.slug})")
    print(f"    Color: {project.color}")
    print(f"    Team: {len(project.team)} members")
    
# Get specific project
project_response = client.get_project("project_id")
project = project_response.project
print(f"\nProject Details:")
print(f"  Name: {project.name}")
print(f"  Description: {project.description}")
print(f"  Icon: {project.icon}")
```

## See Also

- [Projects API Reference](../api-reference/projects) - Complete API documentation and model definitions
- [Boards API](./boards) - Board management
- [Tasks API](./tasks) - Task operations
- [Examples](../patterns/introduction) - More examples
