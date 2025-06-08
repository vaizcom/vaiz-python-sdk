"""
Main example demonstrating the complete workflow of creating and editing tasks.
"""

from .create_task import create_task
from .edit_task import edit_task

def main():
    """Run the complete example workflow."""
    print("Creating a new task...")
    task_id = create_task()
    
    if task_id:
        print("\nEditing the created task...")
        edit_task(task_id)

if __name__ == "__main__":
    main() 