---
sidebar_position: 10
sidebar_label: History Events
title: Working with History — Track Changes & Events | Vaiz Python SDK
description: Learn how to retrieve and track change history for tasks and documents using the Vaiz Python SDK. Monitor edits, authors, timestamps, and activity logs.
---

# History Events

Track all changes made to tasks and other entities.

## Get Task History

```python
from vaiz.models import GetHistoryRequest
from vaiz.models.enums import Kind

request = GetHistoryRequest(
    kind=Kind.Task,
    kindId="task_id"
)

response = client.get_history(request)

for history in response.payload.histories:
    print(f"{history.key}: {history.createdAt}")
    print(f"  Changed by: {history.creatorId}")
    print(f"  Data: {history.data}")
```

## Filter History

### Exclude specific keys

```python
# Track everything except description changes
request = GetHistoryRequest(
    kind=Kind.Task,
    kindId="task_id",
    excludeKeys=["description", "customFields"]
)

response = client.get_history(request)
```

### Include only specific keys

```python
# Only get task creation and completion events
request = GetHistoryRequest(
    kind=Kind.Task,
    kindId="task_id",
    keys=["TASK_CREATED", "TASK_COMPLETED"]
)

response = client.get_history(request)
```

### Filter by date range

```python
from datetime import datetime

request = GetHistoryRequest(
    kind=Kind.Task,
    kindId="task_id",
    dateRangeStart=datetime(2025, 1, 1),
    dateRangeEnd=datetime(2025, 6, 30),
)

response = client.get_history(request)
```

### Filter by author

```python
# Only changes made by specific members
request = GetHistoryRequest(
    kind=Kind.Task,
    kindId="task_id",
    createdBy=["member_id_1", "member_id_2"]
)

response = client.get_history(request)
```

### Limit results

```python
# Get only the last 10 events
request = GetHistoryRequest(
    kind=Kind.Task,
    kindId="task_id",
    limit=10
)

response = client.get_history(request)
```

### Filter by tasks and groups

```python
# Get board history filtered by specific tasks and groups
request = GetHistoryRequest(
    kind=Kind.Board,
    kindId="board_id",
    tasksIds=["task_id_1", "task_id_2"],
    groupsIds=["group_id_1"]
)

response = client.get_history(request)
```

## Use Cases

### Audit trail

```python
def get_task_audit_trail(task_id: str):
    """Get complete audit trail for a task"""
    request = GetHistoryRequest(
        kind=Kind.Task,
        kindId=task_id
    )
    
    response = client.get_history(request)
    
    print(f"Audit Trail for {task_id}")
    print("-" * 50)
    
    for event in response.payload.histories:
        print(f"{event.createdAt}: {event.key} changed")
        print(f"  By: {event.creatorId}")
        print(f"  Value: {event.data}")
        print()

get_task_audit_trail("task_id")
```

### Weekly activity report

```python
from datetime import datetime, timedelta

def weekly_activity_report(task_id: str):
    """Get activity for the last 7 days"""
    now = datetime.now()
    week_ago = now - timedelta(days=7)

    request = GetHistoryRequest(
        kind=Kind.Task,
        kindId=task_id,
        dateRangeStart=week_ago,
        dateRangeEnd=now,
        excludeKeys=["description", "files"]
    )
    
    response = client.get_history(request)
    
    for event in response.payload.histories:
        print(f"{event.key} changed at {event.createdAt}")
        print(f"  New value: {event.data}")
```

### Generate reports

```python
def generate_activity_report(task_id: str):
    """Generate activity report for a task"""
    request = GetHistoryRequest(
        kind=Kind.Task,
        kindId=task_id
    )
    
    response = client.get_history(request)
    histories = response.payload.histories
    
    # Count changes by type
    changes = {}
    for event in histories:
        changes[event.key] = changes.get(event.key, 0) + 1
    
    # Count contributors
    contributors = set(event.creatorId for event in histories)
    
    print(f"Total changes: {len(histories)}")
    print(f"Contributors: {len(contributors)}")
    print("\nChanges by type:")
    for key, count in sorted(changes.items(), key=lambda x: x[1], reverse=True):
        print(f"  {key}: {count}")
```

## Complete example

```python
from datetime import datetime
from vaiz import VaizClient
from vaiz.models import GetHistoryRequest
from vaiz.models.enums import Kind

client = VaizClient(api_key="...", space_id="...")

# Get task
task_response = client.get_task("PRJ-123")
task_id = task_response.task.id

# Get all history
request = GetHistoryRequest(
    kind=Kind.Task,
    kindId=task_id
)

response = client.get_history(request)
print(f"Total changes: {len(response.payload.histories)}")

# Get history with all filters
filtered = GetHistoryRequest(
    kind=Kind.Task,
    kindId=task_id,
    dateRangeStart=datetime(2025, 1, 1),
    dateRangeEnd=datetime(2025, 12, 31),
    limit=20,
    excludeKeys=["description", "files", "customFields"]
)

response = client.get_history(filtered)
print(f"Important changes: {len(response.payload.histories)}")

for event in response.payload.histories:
    print(f"  {event.key}: {event.createdAt}")
```

## See Also

- [Tasks API](./tasks) - Task operations
- [Profile](./profile) - User information
- [Examples](../patterns/introduction) - More examples

