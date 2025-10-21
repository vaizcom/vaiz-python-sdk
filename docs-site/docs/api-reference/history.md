---
sidebar_position: 10
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

### GetHistoryRequest

```python
class GetHistoryRequest:
    kind: Kind                         # Required - Entity type (Task, Project, etc.)
    kindId: str                         # Required - Entity ID
    excludeKeys: Optional[List[str]]    # Keys to exclude from history
    lastLoadedDate: Optional[int]       # Timestamp for pagination (default: 0)
```

---

## See Also

- [History Guide](../guides/history) - Usage examples and patterns
- [Enums](./enums) - Kind enum for entity types

