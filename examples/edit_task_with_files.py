"""
Example: Edit a task to add description and files using the Vaiz SDK.
This example shows how to modify an existing task to include files and description.
"""

from vaiz.models import EditTaskRequest, TaskFile, CreateTaskRequest, TaskPriority
from vaiz.models.enums import EUploadFileType
from .config import get_client, BOARD_ID, GROUP_ID, PROJECT_ID
import os

def edit_task_with_files():
    """Edit an existing task to add description and files."""
    client = get_client()
    
    # First, create a simple task
    print("Step 1: Creating a simple task...")
    simple_task = CreateTaskRequest(
        name="Task to be edited",
        group=GROUP_ID,
        board=BOARD_ID,
        project=PROJECT_ID,
        priority=TaskPriority.Medium,
        completed=True
    )
    
    try:
        create_response = client.create_task(simple_task)
        task_id = create_response.payload['task']['_id']
        print(f"Task created with ID: {task_id}")
    except Exception as e:
        print(f"Error creating initial task: {e}")
        return None
    
    # Step 2: Upload a real file from assets
    print("\nStep 2: Uploading real file from assets...")
    file_path = "./assets/example.png"  # Using real PNG file
    
    try:
        upload_response = client.upload_file(file_path, file_type=EUploadFileType.Image)
        uploaded_file = upload_response.file
        print(f"File uploaded successfully!")
        print(f"File ID: {uploaded_file.id}")
        print(f"File URL: {uploaded_file.url}")
        print(f"File name: {uploaded_file.name}")
        print(f"File type: {uploaded_file.type}")
        print(f"File size: {uploaded_file.size} bytes")
    except FileNotFoundError:
        print(f"File {file_path} not found. Please ensure the assets folder contains example.png")
        return None
    except Exception as e:
        print(f"Error uploading file: {e}")
        return None
    
    # Step 3: Edit the task to add description and files
    print("\nStep 3: Editing task to add description and files...")
    
    # Create TaskFile object from uploaded file
    task_file = TaskFile(
        url=uploaded_file.url,
        name=uploaded_file.name,
        dimension=uploaded_file.dimension,
        ext=uploaded_file.ext,
        _id=uploaded_file.id,
        type=uploaded_file.type
    )
    
    edit_task = EditTaskRequest(
        taskId=task_id,
        name="Updated Task with Real File",
        description="This task has been updated to include a description and attached real file from assets folder. The file provides additional context and resources for completing the task.",
        files=[task_file]
    )

    try:
        response = client.edit_task(edit_task)
        print("Task updated successfully!")
        print(f"Updated task name: {response.payload['task']['name']}")
        print(f"Document ID: {response.payload['task']['document']}")
        print("Note: API accepts description and files but doesn't return them in response.")
        return response.payload['task']['_id']
    except Exception as e:
        print(f"Error updating task: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response content: {e.response.text}")
        return None

def edit_task_add_multiple_files():
    """Edit a task to add multiple real files."""
    client = get_client()
    
    # First, create a simple task
    print("Step 1: Creating a simple task...")
    simple_task = CreateTaskRequest(
        name="Task for Multiple Real Files",
        group=GROUP_ID,
        board=BOARD_ID,
        project=PROJECT_ID,
        priority=TaskPriority.High,
        completed=True
    )
    
    try:
        create_response = client.create_task(simple_task)
        task_id = create_response.payload['task']['_id']
        print(f"Task created with ID: {task_id}")
    except Exception as e:
        print(f"Error creating initial task: {e}")
        return None
    
    # Step 2: Upload multiple real files from assets
    print("\nStep 2: Uploading multiple real files from assets...")
    files_to_upload = [
        ("./assets/example.pdf", EUploadFileType.Pdf),
        ("./assets/example.png", EUploadFileType.Image),
        ("./assets/example.mp4", EUploadFileType.Video)
    ]
    
    task_files = []
    for file_path, file_type in files_to_upload:
        print(f"\nUploading {os.path.basename(file_path)}...")
        try:
            upload_response = client.upload_file(file_path, file_type=file_type)
            uploaded_file = upload_response.file
            
            task_file = TaskFile(
                url=uploaded_file.url,
                name=uploaded_file.name,
                dimension=uploaded_file.dimension,
                ext=uploaded_file.ext,
                _id=uploaded_file.id,
                type=uploaded_file.type
            )
            task_files.append(task_file)
            print(f"✓ {uploaded_file.name} uploaded successfully (ID: {uploaded_file.id})")
        except FileNotFoundError:
            print(f"✗ File {file_path} not found. Skipping...")
        except Exception as e:
            print(f"✗ Error uploading {file_path}: {e}")
    
    if not task_files:
        print("No files were uploaded successfully. Cannot update task with files.")
        return None
    
    # Step 3: Edit the task to add multiple files
    print(f"\nStep 3: Editing task to add {len(task_files)} files...")
    
    edit_task = EditTaskRequest(
        taskId=task_id,
        name="Task with Multiple Real Attachments",
        description="This task now includes multiple real file attachments from assets folder: PDF document, PNG image, and MP4 video.",
        files=task_files
    )

    try:
        response = client.edit_task(edit_task)
        print("Task updated with multiple files successfully!")
        print(f"Updated task name: {response.payload['task']['name']}")
        print(f"Document ID: {response.payload['task']['document']}")
        print(f"Files attached: {len(task_files)}")
        for i, file in enumerate(task_files):
            print(f"  - File {i+1}: {file.name} ({file.type.value})")
        print("Note: API accepts multiple files but doesn't return them in response.")
        return response.payload['task']['_id']
    except Exception as e:
        print(f"Error updating task with multiple files: {e}")
        return None

def edit_task_update_description_only():
    """Edit a task to update only the description."""
    client = get_client()
    
    # First, create a simple task
    print("Step 1: Creating a simple task...")
    simple_task = CreateTaskRequest(
        name="Task for Description Update",
        group=GROUP_ID,
        board=BOARD_ID,
        project=PROJECT_ID,
        priority=TaskPriority.Low,
        completed=True
    )
    
    try:
        create_response = client.create_task(simple_task)
        task_id = create_response.payload['task']['_id']
        print(f"Task created with ID: {task_id}")
    except Exception as e:
        print(f"Error creating initial task: {e}")
        return None
    
    # Step 2: Edit the task to add description
    print("\nStep 2: Updating task description...")
    
    edit_task = EditTaskRequest(
        taskId=task_id,
        description="This task has been updated with a new description. The description provides important context and requirements for the task."
    )

    try:
        response = client.edit_task(edit_task)
        print("Task description updated successfully!")
        print(f"Task name: {response.payload['task']['name']}")
        print(f"Document ID: {response.payload['task']['document']}")
        print("Note: API accepts description but doesn't return it in response.")
        return response.payload['task']['_id']
    except Exception as e:
        print(f"Error updating task description: {e}")
        return None

if __name__ == "__main__":
    print("="*60)
    print("EDITING TASKS WITH REAL FILES FROM ASSETS")
    print("="*60)
    
    print("\n1. Editing task to add real PNG file and description...")
    edit_task_with_files()
    
    print("\n" + "="*50 + "\n")
    
    print("2. Editing task to add multiple real files (PDF, PNG, MP4)...")
    edit_task_add_multiple_files()
    
    print("\n" + "="*50 + "\n")
    
    print("3. Editing task to update description only...")
    edit_task_update_description_only() 