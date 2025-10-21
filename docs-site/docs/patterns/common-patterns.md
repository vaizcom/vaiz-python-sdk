---
sidebar_position: 3
---

# Common Patterns

Essential patterns for everyday SDK usage.

## Pagination

Handle large result sets with pagination:

```python
from vaiz.models import GetTasksRequest

def get_all_tasks(client, project_id: str):
    """Get all tasks from a project using pagination."""
    all_tasks = []
    skip = 0
    limit = 50  # Max per request
    
    while True:
        response = client.get_tasks(
            GetTasksRequest(
                project=project_id,
                limit=limit,
                skip=skip
            )
        )
        
        tasks = response.payload.tasks
        if not tasks:
            break
        
        all_tasks.extend(tasks)
        skip += limit
        
        # Last page if less than limit
        if len(tasks) < limit:
            break
    
    return all_tasks

# Usage
all_project_tasks = get_all_tasks(client, "project_id")
print(f"Total tasks: {len(all_project_tasks)}")
```

## Getting Dynamic IDs

Never hardcode IDs - always fetch them dynamically:

```python
# ✅ Good - Get IDs from API
profile = client.get_profile()
member_id = profile.profile.member_id  # For Member documents

projects = client.get_projects()
project_id = projects.projects[0].id

space_id = client.space_id  # From client initialization

# ❌ Bad - Hardcoded IDs
member_id = "68f7519ca65f977ddb66db8e"  # Don't do this!
```

## Caching Considerations

The SDK automatically caches `get_tasks()` for 5 minutes:

```python
from vaiz.models import GetTasksRequest

# First call - hits API
response1 = client.get_tasks(GetTasksRequest(limit=10))

# Second call within 5 min - returns cached data
response2 = client.get_tasks(GetTasksRequest(limit=10))

# Clear cache manually if needed
client.clear_tasks_cache()

# This will hit API again
response3 = client.get_tasks(GetTasksRequest(limit=10))
```

## Best Practices

### Always Fetch IDs Dynamically

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

### Use Cache Effectively

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

