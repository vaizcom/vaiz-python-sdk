"""
Main example demonstrating the complete workflow of creating and editing tasks.
"""

from .create_task import create_task
from .edit_task import edit_task
from .create_task_with_description_and_files import (
    create_task_with_description_and_files,
    create_task_with_multiple_files,
    create_task_with_description_only
)
from .edit_task_with_files import (
    edit_task_with_files,
    edit_task_add_multiple_files,
    edit_task_update_description_only
)

def main():
    """Run the complete example workflow."""
    print("="*60)
    print("VAIZ SDK EXAMPLES")
    print("="*60)
    
    print("\n1. Basic task creation and editing...")
    print("-" * 40)
    task_id = create_task()
    
    if task_id:
        edit_task(task_id)
    
    print("\n" + "="*60)
    print("2. Creating tasks with description and files...")
    print("-" * 40)
    create_task_with_description_and_files()
    
    print("\n" + "="*60)
    print("3. Creating tasks with multiple files...")
    print("-" * 40)
    create_task_with_multiple_files()
    
    print("\n" + "="*60)
    print("4. Creating tasks with description only...")
    print("-" * 40)
    create_task_with_description_only()
    
    print("\n" + "="*60)
    print("5. Editing tasks to add files and description...")
    print("-" * 40)
    edit_task_with_files()
    
    print("\n" + "="*60)
    print("6. Editing tasks to add multiple files...")
    print("-" * 40)
    edit_task_add_multiple_files()
    
    print("\n" + "="*60)
    print("7. Editing tasks to update description only...")
    print("-" * 40)
    edit_task_update_description_only()
    
    print("\n" + "="*60)
    print("All examples completed!")
    print("="*60)

if __name__ == "__main__":
    main() 