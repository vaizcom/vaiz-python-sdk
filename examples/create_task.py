"""
Module demonstrating task creation functionality with datetime objects.
"""

from datetime import datetime
from vaiz.models import CreateTaskRequest, TaskPriority
from .config import get_client, BOARD_ID, GROUP_ID, PROJECT_ID

def create_task():
    """Create a new task using the Vaiz SDK with datetime objects."""
    client = get_client()
    
    # Example 1: Simple task without dates
    task = CreateTaskRequest(
        name="Test task 123",
        group=GROUP_ID,
        board=BOARD_ID,
        priority=TaskPriority.High,
        completed=True,
        types=[],
        subtasks=[],
        milestones=[],
        blocking=[],
        blockers=[]
    )

    try:
        response = client.create_task(task)
        print("✅ Task created successfully!")
        print(f"Task ID: {response.task.id}")
        print(f"Task name: {response.task.name}")
        print(f"Created at: {response.task.created_at} ({type(response.task.created_at).__name__})")
        
        # Example 2: Task with datetime deadlines  
        print("\n📅 Creating task with datetime deadlines...")
        task_with_dates = CreateTaskRequest(
            name="Project Deadline Task",
            description="Task with specific start and end dates",
            group=GROUP_ID,
            board=BOARD_ID,
            priority=TaskPriority.Medium,
            completed=False,
            due_start=datetime(2025, 2, 1, 9, 0, 0),    # February 1st, 9:00 AM
            due_end=datetime(2025, 2, 15, 17, 0, 0)     # February 15th, 5:00 PM
        )
        
        response2 = client.create_task(task_with_dates)
        print("✅ Task with deadlines created!")
        print(f"Due start: {response2.task.due_start} ({type(response2.task.due_start).__name__})")
        print(f"Due end: {response2.task.due_end} ({type(response2.task.due_end).__name__})")
        
        return response.task.id
    except Exception as e:
        print(f"Error creating task: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response content: {e.response.text}")
        return None

if __name__ == "__main__":
    create_task() 