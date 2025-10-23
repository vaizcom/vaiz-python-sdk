---
sidebar_position: 5
title: Milestones API — Create & Track Project Milestones | Vaiz Python SDK
description: Learn how to use the Vaiz Python SDK to create, edit, toggle, and track milestones in your Vaiz projects. Complete API reference with examples.
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

### Milestone

Main milestone model representing a milestone in the system.

```python
class Milestone:
    id: str                             # Milestone ID
    name: str                           # Milestone name
    description: Optional[str]          # Description
    board: str                          # Board ID
    project: str                        # Project ID
    document: Optional[str]             # Document ID
    due_start: Optional[datetime]       # Start date
    due_end: Optional[datetime]         # End date
    total: Optional[int]                # Total tasks count
    completed: Optional[int]            # Completed tasks count
    tags: List[str]                     # Tags
    color: Optional[str]                # Color
    is_archived: bool                   # Archive status
    is_active: bool                     # Active status
    is_completed: bool                  # Completion status
    creator: str                        # Creator user ID
    editor: Optional[str]               # Last editor user ID
    archiver: Optional[str]             # Archiver user ID (if archived)
    deleter: Optional[str]              # Deleter user ID (if deleted)
    created_at: datetime                # Creation timestamp
    updated_at: datetime                # Last update timestamp
    archived_at: Optional[datetime]     # Archive timestamp
    deleted_at: Optional[datetime]      # Deletion timestamp
    followers: Optional[Dict[str, str]] # Follower mapping
```

---

## Request Models

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

## Response Models

### MilestonesResponse

```python
class MilestonesResponse:
    type: str                           # Response type ("GetMilestones")
    payload: MilestonesPayload          # Response payload
    
    @property
    def milestones(self) -> List[Milestone]:  # Convenience property
        ...
```

---

### MilestonesPayload

```python
class MilestonesPayload:
    milestones: List[Milestone]         # List of milestones
```

---

### GetMilestoneResponse

```python
class GetMilestoneResponse:
    type: str                           # Response type ("GetMilestone")
    payload: GetMilestonePayload        # Response payload
    
    @property
    def milestone(self) -> Milestone:  # Convenience property
        ...
```

---

### GetMilestonePayload

```python
class GetMilestonePayload:
    milestone: Milestone                # Milestone object
```

---

### CreateMilestoneResponse

```python
class CreateMilestoneResponse:
    type: str                           # Response type ("CreateMilestone")
    payload: CreateMilestonePayload     # Response payload
    
    @property
    def milestone(self) -> Milestone:  # Convenience property
        ...
```

---

### CreateMilestonePayload

```python
class CreateMilestonePayload:
    milestone: Milestone                # Created milestone
```

---

### EditMilestoneResponse

```python
class EditMilestoneResponse:
    type: str                           # Response type ("EditMilestone")
    payload: EditMilestonePayload       # Response payload
    
    @property
    def milestone(self) -> Milestone:  # Convenience property
        ...
```

---

### EditMilestonePayload

```python
class EditMilestonePayload:
    milestone: Milestone                # Edited milestone
```

---

### ToggleMilestoneResponse

```python
class ToggleMilestoneResponse:
    type: str                           # Response type ("ToggleMilestone")
    payload: ToggleMilestonePayload     # Response payload
    
    @property
    def task(self) -> Task:            # Convenience property
        ...
```

---

### ToggleMilestonePayload

```python
class ToggleMilestonePayload:
    task: Dict[str, Any]               # Task with updated milestones
```

---

## See Also

- [Milestones Guide](../guides/milestones) - Usage examples and patterns

