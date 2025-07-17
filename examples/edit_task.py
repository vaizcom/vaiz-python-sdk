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
    
    # Edit the task with datetime objects
    edit_task = EditTaskRequest(
        taskId=task_id,
        name="Updated Task with New Deadlines",
        priority=TaskPriority.High,
        completed=False,
        assignees=[ASSIGNEE_ID],
        dueStart=datetime(2025, 4, 1, 9, 0, 0),    # April 1st, 9:00 AM
        dueEnd=datetime(2025, 4, 30, 17, 0, 0)     # April 30th, 5:00 PM
    )

    try:
        edit_response = client.edit_task(edit_task)
        print("\n✅ Task updated successfully!")
        print(f"Response type: {edit_response.type}")
        
        updated_task = edit_response.payload["task"] 
        print(f"\nAfter edit:")
        print(f"Name: {updated_task.get('name')}")
        print(f"Priority: {updated_task.get('priority')}")
        print(f"Due Start: {updated_task.get('dueStart')}")
        print(f"Due End: {updated_task.get('dueEnd')}")
        print(f"Completed: {updated_task.get('completed')}")
        print(f"Assignees: {updated_task.get('assignees')}")
        
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