"""
Example: Move tasks between board groups using the moveTasks API.
"""

from config import get_client, BOARD_ID
from vaiz.models import MoveTaskItem, MoveTasksRequest, CreateTaskRequest, TaskPriority

client = get_client()

if not BOARD_ID:
    raise RuntimeError("Set VAIZ_BOARD_ID in your .env")

# Get board groups
board_response = client.get_board(BOARD_ID)
board = board_response.board

if len(board.groups) < 2:
    raise RuntimeError(f"Board '{board.name}' needs at least 2 groups")

group_a = board.groups[0]
group_b = board.groups[1]
print(f"Board: {board.name}")
print(f"Group A: {group_a.name} ({group_a.id})")
print(f"Group B: {group_b.name} ({group_b.id})")

# Create a test task in group A
task_request = CreateTaskRequest(
    name="SDK Example - Move Task",
    board=BOARD_ID,
    group=group_a.id,
    priority=TaskPriority.General,
)
task_response = client.create_task(task_request)
task_id = task_response.task.id
print(f"\nCreated task: {task_response.task.hrid} (group: {group_a.name})")

# Move task to group B
move_request = MoveTasksRequest(
    moves=[
        MoveTaskItem(
            task_id=task_id,
            to_group_id=group_b.id,
            to_index=0,
        )
    ]
)

move_response = client.move_tasks(move_request)
print(f"\nMoved: {move_response.payload.success_ids}")
print(f"Failed: {move_response.payload.failed_ids}")

# Verify
verify = client.get_task(task_id)
print(f"Task group after move: {verify.task.group} (expected: {group_b.id})")

# Move multiple tasks at once
task_ids = []
for i in range(3):
    t = client.create_task(
        CreateTaskRequest(
            name=f"SDK Example - Batch Move #{i+1}",
            board=BOARD_ID,
            group=group_a.id,
            priority=TaskPriority.General,
        )
    )
    task_ids.append(t.task.id)

print(f"\nCreated {len(task_ids)} tasks in '{group_a.name}'")

batch_move = MoveTasksRequest(
    moves=[
        MoveTaskItem(task_id=tid, to_group_id=group_b.id, to_index=i)
        for i, tid in enumerate(task_ids)
    ]
)

batch_response = client.move_tasks(batch_move)
print(f"Batch moved: {len(batch_response.payload.success_ids)} tasks to '{group_b.name}'")
print(f"Failed: {batch_response.payload.failed_ids}")
