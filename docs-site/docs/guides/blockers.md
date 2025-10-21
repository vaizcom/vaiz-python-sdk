---
sidebar_position: 11
---

# Task Blockers

Manage blocking relationships between tasks.

## Understanding Blockers

Tasks can have blocking relationships:
- **Blockers** (`blockers`) - Tasks that block this task
- **Blocking** (`blocking`) - Tasks that this task blocks

```
Task A blocks Task B
  ↓
Task B.blockers = [Task A]
Task A.blocking = [Task B]
```

## Setting Blockers

### In CreateTaskRequest

```python
from vaiz.models import CreateTaskRequest

task = CreateTaskRequest(
    name="Feature Implementation",
    board="board_id",
    group="group_id",
    project="project_id",
    blockers=["design_task_id"],     # This task is blocked by design task
    blocking=["testing_task_id"]     # This task blocks testing task
)

response = client.create_task(task)
```

### In EditTaskRequest

```python
from vaiz.models import EditTaskRequest

edit = EditTaskRequest(
    task_id="task_id",
    blockers=["task1_id", "task2_id"],  # Update blockers
    blocking=["task3_id"]                # Update blocking
)

response = client.edit_task(edit)
```

## Reading Blocker Relationships

```python
response = client.get_task("PRJ-123")
task = response.task

print(f"Blocked by {len(task.blockers)} tasks:")
for blocker_id in task.blockers:
    blocker = client.get_task(blocker_id)
    print(f"  - {blocker.task.hrid}: {blocker.task.name}")

print(f"\nBlocking {len(task.blocking)} tasks:")
for blocked_id in task.blocking:
    blocked = client.get_task(blocked_id)
    print(f"  - {blocked.task.hrid}: {blocked.task.name}")
```

## Use Cases

### Create Task with Dependencies

```python
# 1. Create design task
design_task = CreateTaskRequest(
    name="Design UI Mockups",
    board="board_id",
    group="group_id",
    project="project_id"
)
design_response = client.create_task(design_task)

# 2. Create implementation task that depends on design
implementation_task = CreateTaskRequest(
    name="Implement UI",
    board="board_id",
    group="group_id",
    project="project_id",
    blockers=[design_response.task.id]  # Blocked by design task
)
impl_response = client.create_task(implementation_task)

# 3. Create testing task that depends on implementation
testing_task = CreateTaskRequest(
    name="Test UI",
    board="board_id",
    group="group_id",
    project="project_id",
    blockers=[impl_response.task.id]  # Blocked by implementation
)
test_response = client.create_task(testing_task)

print("✅ Created task chain: Design → Implementation → Testing")
```

### Update Blockers

```python
# Add new blocker
edit = EditTaskRequest(
    task_id="task_id",
    blockers=["new_blocker_id", "existing_blocker_id"]
)
client.edit_task(edit)

# Remove all blockers
edit = EditTaskRequest(
    task_id="task_id",
    blockers=[]
)
client.edit_task(edit)
```

### Check if Task is Blocked

```python
def is_task_blocked(task_id: str) -> bool:
    """Check if task has any blockers"""
    response = client.get_task(task_id)
    task = response.task
    return len(task.blockers) > 0

def can_start_task(task_id: str) -> bool:
    """Check if all blocker tasks are completed"""
    response = client.get_task(task_id)
    task = response.task
    
    if not task.blockers:
        return True  # No blockers
    
    # Check if all blockers are completed
    for blocker_id in task.blockers:
        blocker = client.get_task(blocker_id)
        if not blocker.task.completed:
            return False  # At least one blocker not done
    
    return True  # All blockers completed

if can_start_task("task_id"):
    print("✅ Task ready to start!")
else:
    print("⏸️ Waiting for blockers to complete")
```

## See Also

- [Tasks](./tasks) - Task operations
- [Examples](../patterns/introduction) - More examples

