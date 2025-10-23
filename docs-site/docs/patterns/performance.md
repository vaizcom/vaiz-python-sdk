---
sidebar_position: 6
sidebar_label: Performance Tips
title: Performance Tips — Optimize SDK Usage | Vaiz Python SDK
description: Learn how to optimize your Vaiz Python SDK usage for better performance. Includes batch operations, caching strategies, and efficiency tips.
---

# Performance Tips

Optimize your SDK usage for better performance.

## Batch Operations Wisely

```python
# ✅ Good - Batch related operations
documents_to_create = [
    "Requirements", "Design Spec", "Test Plan", "Deployment Guide"
]

created = []
for idx, title in enumerate(documents_to_create):
    doc = client.create_document(
        CreateDocumentRequest(
            kind=Kind.Project,
            kind_id=project_id,
            title=title,
            index=idx
        )
    ).payload.document
    created.append(doc)

# ❌ Bad - Making unnecessary API calls in loops
for task in tasks:
    # Don't fetch profile in every iteration!
    profile = client.get_profile()
    # ... use profile
```

## Minimize API Calls

```python
# ✅ Good - Fetch once, use many times
projects = client.get_projects()
project_map = {p.id: p for p in projects.projects}

# Use cached data
for task in tasks:
    project = project_map.get(task.project)
    print(f"{task.name} - {project.name if project else 'Unknown'}")

# ❌ Bad - Fetching same data repeatedly
for task in tasks:
    project = client.get_project(task.project)  # Repeated API calls!
    print(f"{task.name} - {project.project.name}")
```

## Use Task Cache Effectively

```python
from vaiz.models import GetTasksRequest

# Cache is automatic for identical requests
request = GetTasksRequest(project=project_id, completed=False)

# First call - hits API (slow)
tasks1 = client.get_tasks(request)

# Within 5 minutes - uses cache (fast)
tasks2 = client.get_tasks(request)

# Different request - hits API again
tasks3 = client.get_tasks(GetTasksRequest(project=project_id, completed=True))
```

## Best Practices

### Create Lookup Maps

Cache frequently accessed data in dictionaries:

```python
# Fetch all reference data once
projects = client.get_projects()
boards = client.get_boards()
milestones = client.get_milestones()

# Create lookup maps
project_map = {p.id: p for p in projects.projects}
board_map = {b.id: b for b in boards.boards}
milestone_map = {m.id: m for m in milestones.milestones}

# Use in loops without additional API calls
for task in tasks:
    project = project_map.get(task.project)
    board = board_map.get(task.board)
    print(f"{task.name} - {project.name} - {board.name}")
```

### Batch File Operations

Upload multiple files efficiently:

```python
from vaiz.models.enums import UploadFileType

files_to_upload = [
    ("screenshot1.png", UploadFileType.Image),
    ("screenshot2.png", UploadFileType.Image),
    ("report.pdf", UploadFileType.Pdf),
]

uploaded_files = []
for file_path, file_type in files_to_upload:
    file = client.upload_file(file_path, file_type)
    uploaded_files.append(file.file)

print(f"✅ Uploaded {len(uploaded_files)} files")
```

## See Also

- [Common Patterns](./common-patterns) - Essential SDK patterns

