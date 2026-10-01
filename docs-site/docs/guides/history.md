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

for history in response.payload.items:
    print(f"{history.key}: {history.createdAt}")
    print(f"  Changed by: {history.creatorId}")
    print(f"  Data: {history.data}")
```

Events are returned newest first, one page at a time.

## Filter History

### Include only specific events

```python
# Only get task creation and completion events
request = GetHistoryRequest(
    kind=Kind.Task,
    kindId="task_id",
    eventKeys=["TASK_CREATED", "TASK_COMPLETED"]
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
    memberIds=["member_id_1", "member_id_2"]
)

response = client.get_history(request)
```

### Filter by boards and groups

```python
# Project history narrowed to one board and one of its groups
request = GetHistoryRequest(
    kind=Kind.Project,
    kindId="project_id",
    boardIds=["board_id"],
    groupIds=["group_id"]
)

response = client.get_history(request)
```

`groupIds` is applied only together with `boardIds`.

## Pagination

Use `limit` for the page size and pass `payload.page.nextCursor` to load the next page:

```python
def iter_history(kind, kind_id, page_size=50):
    cursor = None
    while True:
        response = client.get_history(GetHistoryRequest(
            kind=kind,
            kindId=kind_id,
            limit=page_size,
            nextCursor=cursor,
        ))
        yield from response.payload.items

        page = response.payload.page
        if not page or not page.hasMore:
            break
        cursor = page.nextCursor

for event in iter_history(Kind.Task, "task_id"):
    print(event.key, event.createdAt)
```

## Use Cases

### Audit trail

```python
def get_task_audit_trail(task_id: str):
    """Get audit trail for a task"""
    for event in iter_history(Kind.Task, task_id):
        print(f"{event.createdAt}: {event.key}")
        print(f"  By: {event.creatorId}")
        print(f"  Value: {event.data}")

get_task_audit_trail("task_id")
```

### Weekly activity report

```python
from datetime import datetime, timedelta

def weekly_activity_report(task_id: str):
    """Get activity for the last 7 days"""
    now = datetime.now()

    request = GetHistoryRequest(
        kind=Kind.Task,
        kindId=task_id,
        dateRangeStart=now - timedelta(days=7),
        dateRangeEnd=now,
    )

    response = client.get_history(request)

    for event in response.payload.items:
        print(f"{event.key} at {event.createdAt}")
        print(f"  New value: {event.data}")
```

### Generate reports

```python
def generate_activity_report(task_id: str):
    """Generate activity report for a task"""
    histories = list(iter_history(Kind.Task, task_id))

    changes = {}
    for event in histories:
        changes[event.key] = changes.get(event.key, 0) + 1

    contributors = set(event.creatorId for event in histories)

    print(f"Total changes: {len(histories)}")
    print(f"Contributors: {len(contributors)}")
    print("\nChanges by type:")
    for key, count in sorted(changes.items(), key=lambda x: x[1], reverse=True):
        print(f"  {key}: {count}")
```

See [GetHistoryRequest](../api-reference/history#gethistoryrequest) for all parameters and deprecated aliases.

## See Also

- [Tasks API](./tasks) - Task operations
- [Profile](./profile) - User information
- [Examples](../patterns/introduction) - More examples
