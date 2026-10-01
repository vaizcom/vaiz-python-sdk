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
- `request` - History request (kind, kindId, optional filters and cursor)

**Returns:** `GetHistoryResponse` with a page of history events (newest first) and pagination info

---

## Models

### HistoryItem

Main history event model.

```python
class HistoryItem:
    id: str                          # History event ID (alias "_id")
    creatorId: str                   # Member who made the change
    createdAt: str                   # Timestamp of change
    data: HistoryData                # Changed data
    key: str                         # Event key, e.g. "TASK_CREATED"
    type: int                        # Event type
    taskId: Optional[str]            # Task ID (for task events)
    boardId: Optional[str]           # Board ID
    projectId: Optional[str]         # Project ID
    documentId: Optional[str]        # Document ID
    milestoneId: Optional[str]       # Milestone ID
    memberId: Optional[str]          # Member ID
    spaceId: Optional[str]           # Space ID
    agentId: Optional[str]           # Agent ID (for changes made by an agent)
    updatedAt: Optional[str]         # Last update timestamp
```

---

### HistoryPage

Cursor pagination info.

```python
class HistoryPage:
    hasMore: bool                    # More events are available
    nextCursor: Optional[int]        # Pass as GetHistoryRequest.nextCursor to load the next page
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
    kind: Kind                           # Required - Entity type (Task, Project, Board, etc.)
    kindId: str                          # Required - Entity ID
    memberIds: Optional[List[str]]       # Filter by member IDs who made the changes
    boardIds: Optional[List[str]]        # Filter by board IDs
    groupIds: Optional[List[str]]        # Filter by group IDs (requires boardIds)
    agentId: Optional[str]               # Only events of this agent
    eventKeys: Optional[List[str]]       # Only include these event keys
    dateRangeStart: Optional[datetime]   # Start of date range filter
    dateRangeEnd: Optional[datetime]     # End of date range filter
    limit: Optional[int]                 # Page size
    nextCursor: Optional[int]            # Cursor from the previous page
```

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `kind` | `Kind` | Yes | Entity type — `Kind.Task`, `Kind.Project`, `Kind.Board`, etc. |
| `kindId` | `str` | Yes | ID of the entity to get history for |
| `memberIds` | `List[str]` | No | Filter events by member IDs who made the changes |
| `boardIds` | `List[str]` | No | Filter events by board IDs |
| `groupIds` | `List[str]` | No | Filter events by group IDs; applied only together with `boardIds` |
| `agentId` | `str` | No | Only events of this agent |
| `eventKeys` | `List[str]` | No | Only include events matching these keys (e.g. `["TASK_CREATED"]`) |
| `dateRangeStart` | `datetime` | No | Return events after this date |
| `dateRangeEnd` | `datetime` | No | Return events before this date |
| `limit` | `int` | No | Page size |
| `nextCursor` | `int` | No | `payload.page.nextCursor` from the previous response |

:::caution Deprecated parameters
The old names are still accepted with a `DeprecationWarning` and mapped to the new ones: `createdBy` → `memberIds`, `keys` → `eventKeys`, `groupsIds` → `groupIds`, `lastLoadedDate` → `nextCursor`. `excludeKeys` and `tasksIds` are no longer supported by the API and are ignored.
:::

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
    items: List[HistoryItem]         # Page of history events, newest first
    page: Optional[HistoryPage]      # Pagination info

    @property
    def histories(self) -> List[HistoryItem]: ...  # Deprecated alias for items
```

---

## See Also

- [History Guide](../guides/history) - Usage examples and patterns
- [Enums](./enums) - Kind enum for entity types

