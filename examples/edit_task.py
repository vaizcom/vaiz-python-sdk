"""
Module demonstrating task editing functionality.
"""

from vaiz.models import EditTaskRequest
from .config import get_client, ASSIGNEE_ID
from .create_task import create_task

def edit_task(task_id):
    """Edit an existing task using the Vaiz SDK."""
    client = get_client()
    
    edit_task = EditTaskRequest(
        taskId=task_id,
        name="Updated task name",
        assignees=[ASSIGNEE_ID]
    )

    try:
        edit_response = client.edit_task(edit_task)
        print("Task updated successfully!")
        print(f"Response type: {edit_response.type}")
        print(f"Updated task data: {edit_response.payload}")
        return edit_response
    except Exception as e:
        print(f"Error updating task: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response content: {e.response.text}")
        return None

if __name__ == "__main__":
    # First create a task
    print("Creating a new task...")
    task_id = create_task()
    
    if task_id:
        print(f"\nEditing task with ID: {task_id}")
        edit_task(task_id)
    else:
        print("Failed to create task, cannot proceed with editing.") 