"""
Module demonstrating task creation functionality.
"""

from vaiz.models import CreateTaskRequest, TaskPriority
from .config import get_client, BOARD_ID, GROUP_ID, PROJECT_ID

def create_task():
    """Create a new task using the Vaiz SDK."""
    client = get_client()
    
    task = CreateTaskRequest(
        name="Test task 123",
        group=GROUP_ID,
        board=BOARD_ID,
        project=PROJECT_ID,
        priority=TaskPriority.High,
        completed=True,
        types=["649bea169d17e4070e0337fa"],
        subtasks=[],
        milestones=[],
        rightConnectors=[],
        leftConnectors=[]
    )

    try:
        response = client.create_task(task)
        print("Task created successfully!")
        print(f"Response type: {response.type}")
        print(f"Task data: {response.payload}")
        return response.payload['task']['_id']
    except Exception as e:
        print(f"Error creating task: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response content: {e.response.text}")
        return None

if __name__ == "__main__":
    create_task() 