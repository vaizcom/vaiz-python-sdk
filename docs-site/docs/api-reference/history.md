---
sidebar_position: 10
sidebar_label: History
title: History API — Track Document & Task Changes | Vaiz Python SDK
description: Learn how to use the Vaiz Python SDK to retrieve change history for documents and tasks. Track edits, authors, timestamps, and more.
---

# History

Complete reference for history-related methods and models.

## Methods

### `get_history`

```python
get_history(request: GetHistoryRequest) -> GetHistoryResponse
```

Get change history for an entity.

**Parameters:**
- `request` - History request (kind, kindId, optional filters)

**Returns:** `GetHistoryResponse` with list of history events

---

## Models

### HistoryItem

Main history event model.

```python
class HistoryItem:
    _id: str                         # History event ID
    taskId: str                      # Task ID
    creatorId: str                   # User who made the change
    createdAt: str                   # Timestamp of change
    data: HistoryData                # Changed data
    key: str                         # Change type key
    type: int                        # Event type
    updatedAt: str                   # Last update timestamp
    boardId: Optional[str]           # Board ID (if applicable)
```

---

### HistoryData

```python
class HistoryData:
    _id: str                         # Entity ID
    hrid: Optional[str]              # Human-readable ID
    name: Optional[str]              # Entity name
    taskPriority: Optional[int]      # Task priority (if changed)
    board: Optional[str]             # Board ID (if changed)
    members: Optional[List[str]]     # Members (if changed)
    project: Optional[str]           # Project ID (if changed)
    dueStart: Optional[str]          # Due start (if changed)
    dueEnd: Optional[str]            # Due end (if changed)
    # ... additional fields depending on what changed
```

:::info Dynamic Fields
`HistoryData` accepts arbitrary additional fields using `extra="allow"` configuration, as different change types include different data fields.
:::

---

## Request Models

### GetHistoryRequest

```python
class GetHistoryRequest:
    kind: Kind                         # Required - Entity type (Task, Project, etc.)
    kindId: str                         # Required - Entity ID
    excludeKeys: Optional[List[str]]    # Keys to exclude from history
    lastLoadedDate: Optional[int]       # Timestamp for pagination (default: 0)
```

---

## Response Models

### GetHistoryResponse

```python
class GetHistoryResponse:
    type: str                        # Response type ("GetHistory")
    payload: GetHistoryPayload       # Response payload
```

---

### GetHistoryPayload

```python
class GetHistoryPayload:
    histories: List[HistoryItem]     # List of history events
```

---

## See Also

- [History Guide](../guides/history) - Usage examples and patterns
- [Enums](./enums) - Kind enum for entity types

