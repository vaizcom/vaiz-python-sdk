---
sidebar_position: 5
---

# Milestones

Track progress with milestones in Vaiz SDK.

## Getting Milestones

### All Milestones

```python
response = client.get_milestones()

for milestone in response.milestones:
    progress = f"{milestone.completed}/{milestone.total}"
    print(f"📍 {milestone.name}: {progress}")
```

### Single Milestone

```python
response = client.get_milestone("milestone_id")
milestone = response.milestone

print(f"Name: {milestone.name}")
print(f"Progress: {milestone.completed}/{milestone.total}")
print(f"Due: {milestone.due_end}")
```

## Creating Milestones

### Basic Milestone

```python
from vaiz.models import CreateMilestoneRequest

milestone = CreateMilestoneRequest(
    name="Q1 2025",
    board="board_id",
    project="project_id"
)

response = client.create_milestone(milestone)
```

### With Dates

```python
from datetime import datetime

milestone = CreateMilestoneRequest(
    name="Q1 2025 Release",
    description="First quarter tasks",
    board="board_id",
    project="project_id",
    due_start=datetime(2025, 1, 1),
    due_end=datetime(2025, 3, 31),
    color="#4CAF50"
)

response = client.create_milestone(milestone)
```

## Editing Milestones

```python
from vaiz.models import EditMilestoneRequest

edit = EditMilestoneRequest(
    milestone_id="milestone_id",
    name="Updated Name",
    description="New description",
    due_end=datetime(2025, 12, 31)
)

response = client.edit_milestone(edit)
```

## Attaching to Tasks

### Toggle Milestone

```python
from vaiz.models import ToggleMilestoneRequest

request = ToggleMilestoneRequest(
    task_id="task_id",
    milestone_ids=["milestone_id_1", "milestone_id_2"]
)

response = client.toggle_milestone(request)
task = response.task

print(f"Milestones: {task.milestones}")
```

:::info Toggle Behavior
The `toggle_milestone` method works as a switch:
- If milestone is attached → it detaches
- If milestone is not attached → it attaches
:::

## Request Models

### CreateMilestoneRequest

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | `str` | Yes | Milestone name |
| `board` | `str` | Yes | Board ID |
| `project` | `str` | Yes | Project ID |
| `description` | `str` | No | Description |
| `due_start` | `datetime` | No | Start date |
| `due_end` | `datetime` | No | End date |
| `color` | `str` | No | Hex color |

### EditMilestoneRequest

All fields except `milestone_id` are optional. Only provide fields you want to update.

## Examples

### Create Quarterly Milestones

```python
from datetime import datetime

quarters = [
    ("Q1 2025", datetime(2025, 1, 1), datetime(2025, 3, 31)),
    ("Q2 2025", datetime(2025, 4, 1), datetime(2025, 6, 30)),
    ("Q3 2025", datetime(2025, 7, 1), datetime(2025, 9, 30)),
    ("Q4 2025", datetime(2025, 10, 1), datetime(2025, 12, 31)),
]

for name, start, end in quarters:
    milestone = CreateMilestoneRequest(
        name=name,
        board="board_id",
        project="project_id",
        due_start=start,
        due_end=end
    )
    
    response = client.create_milestone(milestone)
    print(f"✅ Created: {name}")
```

### Track Progress

```python
response = client.get_milestones()

for milestone in response.milestones:
    if milestone.total > 0:
        percentage = (milestone.completed / milestone.total) * 100
        print(f"{milestone.name}: {percentage:.0f}% complete")
```

## See Also

- [Tasks](./tasks) - Task operations
- [Projects](./projects) - Project management
- [Examples](../examples) - More examples

