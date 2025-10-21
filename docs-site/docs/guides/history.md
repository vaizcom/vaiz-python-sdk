---
sidebar_position: 10
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

### Exclude Specific Keys

```python
# Track everything except description changes
request = GetHistoryRequest(
    kind=Kind.Task,
    kindId="task_id",
    excludeKeys=["description", "customFields"]
)

response = client.get_history(request)
```

## Use Cases

### Audit Trail

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

### Filter Specific Changes

```python
def monitor_important_changes(task_id: str):
    """Get history excluding description changes"""
    request = GetHistoryRequest(
        kind=Kind.Task,
        kindId=task_id,
        excludeKeys=["description", "files"]
    )
    
    response = client.get_history(request)
    
    for event in response.payload.histories:
        print(f"{event.key} changed at {event.createdAt}")
        print(f"  New value: {event.data}")
```

### Generate Reports

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
from vaiz.models.enums import Kind

client = VaizClient(api_key="...", space_id="...")

# Get task
task = client.get_task("PRJ-123")
task_id = task.payload["task"]["_id"]

# Get all history
request = GetHistoryRequest(
    kind=Kind.Task,
    kindId=task_id
)

response = client.get_history(request)
print(f"📊 Total changes: {len(response.payload.histories)}")

# Get history excluding certain keys
filtered = GetHistoryRequest(
    kind=Kind.Task,
    kindId=task_id,
    excludeKeys=["description", "files", "customFields"]
)

response = client.get_history(filtered)
print(f"⚡ Important changes: {len(response.payload.histories)}")

for event in response.payload.histories:
    print(f"  {event.key}: {event.createdAt}")
```

## See Also

- [Tasks API](./tasks) - Task operations
- [Profile](./profile) - User information
- [Examples](../examples) - More examples

