---
sidebar_position: 5
---

# Milestones

Complete reference for milestone-related methods and models.

## Methods

### `get_milestones`

```python
get_milestones() -> MilestonesResponse
```

Get all milestones in current space.

**Returns:** `MilestonesResponse` with list of milestones

---

### `get_milestone`

```python
get_milestone(milestone_id: str) -> GetMilestoneResponse
```

Get a single milestone by ID.

**Parameters:**
- `milestone_id` - Milestone ID

**Returns:** `GetMilestoneResponse` with milestone data

---

### `create_milestone`

```python
create_milestone(request: CreateMilestoneRequest) -> CreateMilestoneResponse
```

Create a new milestone.

**Parameters:**
- `request` - Milestone configuration (name, board, project required)

**Returns:** `CreateMilestoneResponse` with created milestone

---

### `edit_milestone`

```python
edit_milestone(request: EditMilestoneRequest) -> EditMilestoneResponse
```

Edit an existing milestone.

**Parameters:**
- `request` - Edit request with milestone_id and fields to update

**Returns:** `EditMilestoneResponse` with updated milestone

---

### `toggle_milestone`

```python
toggle_milestone(request: ToggleMilestoneRequest) -> ToggleMilestoneResponse
```

Attach/detach milestones to/from a task.

**Parameters:**
- `request` - Task ID and milestone IDs to toggle

**Returns:** `ToggleMilestoneResponse` with updated task

---

## Models

### CreateMilestoneRequest

```python
class CreateMilestoneRequest:
    name: str                           # Required - Milestone name
    board: str                          # Required - Board ID
    project: str                        # Required - Project ID
    description: Optional[str]          # Description
    due_start: Optional[datetime]       # Start date
    due_end: Optional[datetime]         # End date
    tags: List[str]                     # Tags
    color: str                          # Color name (default: "blue")
```

---

### EditMilestoneRequest

```python
class EditMilestoneRequest:
    milestone_id: str                   # Required - Milestone ID
    name: Optional[str]                 # New name
    description: Optional[str]          # New description
    due_start: Optional[datetime]       # New start date
    due_end: Optional[datetime]         # New end date
    tags: Optional[List[str]]           # New tags
    color: Optional[str]                # New color name
```

---

### ToggleMilestoneRequest

```python
class ToggleMilestoneRequest:
    task_id: str                        # Required - Task ID
    milestone_ids: List[str]            # Required - Milestone IDs to toggle
```

---

### Milestone

```python
class Milestone:
    id: str                             # Milestone ID
    name: str                           # Name
    description: Optional[str]          # Description
    board: str                          # Board ID
    project: str                        # Project ID
    total: int                          # Total tasks
    completed: int                      # Completed tasks
    creator: str                        # Creator ID
    editor: Optional[str]               # Editor ID
    created_at: datetime                # Creation timestamp
    updated_at: datetime                # Update timestamp
    due_start: Optional[datetime]       # Start date
    due_end: Optional[datetime]         # End date
    tags: List[str]                     # Tags
    color: Optional[str]                # Color
    is_archived: bool                   # Archive status
    is_active: bool                     # Active status
    is_completed: bool                  # Completion status
```

---

## See Also

- [Milestones Guide](../guides/milestones) - Usage examples and patterns

