"""
Module demonstrating task editing functionality with datetime objects.
"""

from datetime import datetime
from vaiz.models import EditTaskRequest, TaskPriority
from .config import get_client, ASSIGNEE_ID
from .create_task import create_task

def edit_task(task_id):
    """Edit an existing task using the Vaiz SDK with datetime objects."""
    client = get_client()
    
    # Get the current task to show before/after
    print("Before edit:")
    before_response = client.get_task(task_id)
    task_data = before_response.payload["task"]
    print(f"Name: {task_data.get('name')}")
    print(f"Priority: {task_data.get('priority')}")
    print(f"Due Start: {task_data.get('dueStart')}")
    print(f"Due End: {task_data.get('dueEnd')}")
    print(f"Completed: {task_data.get('completed')}")
    
    # Create an EditTaskRequest with updated information, including new datetime deadlines
    print("\n📝 Editing task...")
    edit_task = EditTaskRequest(
        task_id=task_id,
        name="Updated Task with New Deadlines",
        priority=TaskPriority.High,
        completed=False,
        assignees=[],
        due_start=datetime(2025, 4, 1, 9, 0, 0),    # April 1st, 9:00 AM
        due_end=datetime(2025, 4, 30, 17, 0, 0)     # April 30th, 5:00 PM
    )
    
    try:
        response = client.edit_task(edit_task)
        print("✅ Task edited successfully!")
        print(f"Response type: {response.type}")
        
        # Get the updated task data from response
        updated_task = response.payload["task"]
        print(f"Updated task name: {updated_task.get('name')}")
        print(f"Updated priority: {updated_task.get('priority')}")
        print(f"Updated assignees: {updated_task.get('assignees')}")
        print(f"Due Start: {updated_task.get('dueStart')}")
        print(f"Due End: {updated_task.get('dueEnd')}")
        
        return response
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