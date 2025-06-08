"""
Module demonstrating how to get task information using the Vaiz SDK.
"""

from .config import get_client

def get_task(task_id):
    """Get task information using the Vaiz SDK."""
    client = get_client()
    
    try:
        response = client.get_task(task_id)
        print("Task retrieved successfully!")
        print(f"Response type: {response.type}")
        print(f"Task data: {response.payload}")
        return response
    except Exception as e:
        print(f"Error getting task: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response content: {e.response.text}")
        return None

if __name__ == "__main__":
    # First create a task
    print("Creating a new task...")
    task_id = "PRJ-75"
    
    if task_id:
        print(f"\nGetting information for task with ID: {task_id}")
        get_task(task_id)
    else:
        print("Failed to create task, cannot proceed with getting task information.") 