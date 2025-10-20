---
sidebar_position: 10
---

# History

Track all changes made to tasks and other entities.

## Get Task History

```python
from vaiz.models import GetHistoryRequest
from vaiz.models.enums import EKind

request = GetHistoryRequest(
    kind=EKind.Task,
    kindId="task_id"
)

response = client.get_history(request)

for history in response.payload.histories:
    print(f"{history.key}: {history.createdAt}")
    print(f"  Changed by: {history.createdBy}")
    print(f"  Data: {history.data}")
```

## Filter History

### By Date Range

```python
from datetime import datetime

request = GetHistoryRequest(
    kind=EKind.Task,
    kindId="task_id",
    dateRangeStart=datetime(2025, 1, 1).isoformat(),
    dateRangeEnd=datetime(2025, 12, 31).isoformat()
)

response = client.get_history(request)
```

### By User

```python
request = GetHistoryRequest(
    kind=EKind.Task,
    kindId="task_id",
    createdBy=["user_id_1", "user_id_2"]
)
```

### By Specific Keys

```python
# Only track name and priority changes
request = GetHistoryRequest(
    kind=EKind.Task,
    kindId="task_id",
    keys=["name", "priority", "completed"]
)
```

### Exclude Keys

```python
# Track everything except description changes
request = GetHistoryRequest(
    kind=EKind.Task,
    kindId="task_id",
    excludeKeys=["description"]
)
```

## Common History Keys

Track these common task changes:

| Key | Description |
|-----|-------------|
| `name` | Task name changes |
| `priority` | Priority updates |
| `completed` | Status changes |
| `assignees` | Assignee modifications |
| `dueStart`, `dueEnd` | Date changes |
| `description` | Description updates |
| `types` | Type changes |
| `milestones` | Milestone assignments |
| `customFields` | Custom field updates |

## Request Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `kind` | `EKind` | Entity type (Task, Project, etc.) |
| `kindId` | `str` | Entity ID |
| `limit` | `int` | Max results (default: 50, max: 100) |
| `keys` | `List[str]` | Filter by specific keys |
| `excludeKeys` | `List[str]` | Exclude specific keys |
| `createdBy` | `List[str]` | Filter by user IDs |
| `dateRangeStart` | `str` | ISO datetime string |
| `dateRangeEnd` | `str` | ISO datetime string |

## Use Cases

### Audit Trail

```python
def get_task_audit_trail(task_id: str):
    """Get complete audit trail for a task"""
    request = GetHistoryRequest(
        kind=EKind.Task,
        kindId=task_id,
        limit=100
    )
    
    response = client.get_history(request)
    
    print(f"Audit Trail for {task_id}")
    print("-" * 50)
    
    for event in response.payload.histories:
        print(f"{event.createdAt}: {event.key} changed")
        print(f"  By: {event.createdBy}")
        print(f"  Value: {event.data}")
        print()

get_task_audit_trail("task_id")
```

### Track User Activity

```python
def get_user_changes(user_id: str, days: int = 7):
    """Get all changes made by user in last N days"""
    from datetime import datetime, timedelta
    
    start_date = datetime.now() - timedelta(days=days)
    
    request = GetHistoryRequest(
        kind=EKind.Task,
        kindId="task_id",  # Or iterate over tasks
        createdBy=[user_id],
        dateRangeStart=start_date.isoformat()
    )
    
    response = client.get_history(request)
    
    print(f"Changes by user {user_id} in last {days} days:")
    for event in response.payload.histories:
        print(f"  - {event.key} at {event.createdAt}")
```

### Monitor Important Changes

```python
def monitor_priority_changes(task_id: str):
    """Monitor only priority and status changes"""
    request = GetHistoryRequest(
        kind=EKind.Task,
        kindId=task_id,
        keys=["priority", "completed"]
    )
    
    response = client.get_history(request)
    
    for event in response.payload.histories:
        if event.key == "priority":
            print(f"⚡ Priority changed to {event.data}")
        elif event.key == "completed":
            status = "✅ Completed" if event.data else "⏳ Reopened"
            print(f"{status} at {event.createdAt}")
```

### Generate Reports

```python
def generate_activity_report(task_id: str):
    """Generate activity report for a task"""
    request = GetHistoryRequest(
        kind=EKind.Task,
        kindId=task_id
    )
    
    response = client.get_history(request)
    histories = response.payload.histories
    
    # Count changes by type
    changes = {}
    for event in histories:
        changes[event.key] = changes.get(event.key, 0) + 1
    
    # Count contributors
    contributors = set(event.createdBy for event in histories)
    
    print("📊 Activity Report")
    print(f"Total changes: {len(histories)}")
    print(f"Contributors: {len(contributors)}")
    print("\nChanges by type:")
    for key, count in sorted(changes.items(), key=lambda x: x[1], reverse=True):
        print(f"  {key}: {count}")
```

## Complete Example

```python
from vaiz import VaizClient
from vaiz.models import GetHistoryRequest
from vaiz.models.enums import EKind
from datetime import datetime, timedelta

client = VaizClient(api_key="...", space_id="...")

# Get task
task = client.get_task("PRJ-123")
task_id = task.payload["task"]["_id"]

# Get recent history
recent = GetHistoryRequest(
    kind=EKind.Task,
    kindId=task_id,
    dateRangeStart=(datetime.now() - timedelta(days=7)).isoformat(),
    limit=20
)

response = client.get_history(recent)

print(f"📊 Recent changes (last 7 days): {len(response.payload.histories)}")

# Get changes by specific user
user_id = "user_id"
user_changes = GetHistoryRequest(
    kind=EKind.Task,
    kindId=task_id,
    createdBy=[user_id]
)

response = client.get_history(user_changes)
print(f"👤 Changes by user: {len(response.payload.histories)}")

# Get only important changes
important = GetHistoryRequest(
    kind=EKind.Task,
    kindId=task_id,
    keys=["name", "priority", "completed", "assignees"]
)

response = client.get_history(important)
print(f"⚡ Important changes: {len(response.payload.histories)}")
```

## See Also

- [Tasks API](./tasks) - Task operations
- [Profile](./profile) - User information
- [Examples](../examples) - More examples

