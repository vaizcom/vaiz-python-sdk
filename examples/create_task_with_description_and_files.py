"""
Example: Create a task with description and files using the Vaiz SDK.
This example shows the complete workflow: upload file first, then create task with file info.
"""

from vaiz.models import CreateTaskRequest, TaskPriority, TaskFile
from vaiz.models.enums import UploadFileType
from .config import get_client, BOARD_ID, GROUP_ID, PROJECT_ID
import os

def create_task_with_description_and_files():
    """Create a new task with description and files using the Vaiz SDK."""
    client = get_client()
    
    # Step 1: Upload a real file from assets folder
    print("Step 1: Uploading real file from assets...")
    file_path = "./assets/example.pdf"  # Using real PDF file
    
    try:
        upload_response = client.upload_file(file_path, file_type=UploadFileType.Pdf)
        uploaded_file = upload_response.file
        print(f"File uploaded successfully!")
        print(f"File ID: {uploaded_file.id}")
        print(f"File URL: {uploaded_file.url}")
        print(f"File name: {uploaded_file.name}")
        print(f"File type: {uploaded_file.type}")
        print(f"File size: {uploaded_file.size} bytes")
    except FileNotFoundError:
        print(f"File {file_path} not found. Please ensure the assets folder contains example.pdf")
        return None
    except Exception as e:
        print(f"Error uploading file: {e}")
        return None
    
    # Step 2: Create task with description and file information
    print("\nStep 2: Creating task with description and files...")
    
    # Create TaskFile object from uploaded file
    task_file = TaskFile(
        url=uploaded_file.url,
        name=uploaded_file.name,
        dimension=uploaded_file.dimension,
        ext=uploaded_file.ext,
        id=uploaded_file.id,
        type=uploaded_file.type
    )
    
    task = CreateTaskRequest(
        name="Task with Description and Real File",
        group=GROUP_ID,
        board=BOARD_ID,
        project=PROJECT_ID,
        priority=TaskPriority.High,
        completed=True,
        description="This is a detailed description of the task with a real PDF file attached.",
        files=[task_file]
    )

    try:
        response = client.create_task(task)
        print("Task with description and files created successfully!")
        print(f"Response type: {response.type}")
        print(f"Task ID: {response.task.id}")
        print(f"Task name: {response.payload['task']['name']}")
        print(f"Document ID: {response.payload['task']['document']}")
        print("Note: API accepts description and files but doesn't return them in response.")
        print("Description and files are stored and can be accessed via separate API calls.")
        return response.task.id
    except Exception as e:
        print(f"Error creating task with description and files: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response content: {e.response.text}")
        return None

def create_task_with_multiple_files():
    """Create a task with multiple real files of different types."""
    client = get_client()
    
    # Real files from assets folder
    files_to_upload = [
        ("./assets/example.pdf", UploadFileType.Pdf),
        ("./assets/example.png", UploadFileType.Image),
        ("./assets/example.mp4", UploadFileType.Video)
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
                id=uploaded_file.id,
                type=uploaded_file.type
            )
            task_files.append(task_file)
            print(f"✓ {uploaded_file.name} uploaded successfully (ID: {uploaded_file.id})")
        except FileNotFoundError:
            print(f"✗ File {file_path} not found. Skipping...")
        except Exception as e:
            print(f"✗ Error uploading {file_path}: {e}")
    
    if not task_files:
        print("No files were uploaded successfully. Cannot create task with files.")
        return None
    
    print(f"\nCreating task with {len(task_files)} files...")
    
    task = CreateTaskRequest(
        name="Task with Multiple Real Files",
        group=GROUP_ID,
        board=BOARD_ID,
        project=PROJECT_ID,
        priority=TaskPriority.Medium,
        completed=True,
        description="This task contains multiple real file attachments from assets folder: PDF document, PNG image, and MP4 video.",
        files=task_files
    )

    try:
        response = client.create_task(task)
        print("Task with multiple files created successfully!")
        print(f"Task ID: {response.task.id}")
        print(f"Document ID: {response.payload['task']['document']}")
        print(f"Files attached: {len(task_files)}")
        for i, file in enumerate(task_files):
            print(f"  - File {i+1}: {file.name} ({file.type.value})")
        print("Note: API accepts multiple files but doesn't return them in response.")
        print("Files are stored and can be accessed via separate API calls.")
        return response.task.id
    except Exception as e:
        print(f"Error creating task with multiple files: {e}")
        return None

def create_task_with_description_only():
    """Create a task with description but without files."""
    client = get_client()
    
    task = CreateTaskRequest(
        name="Task with Description Only",
        group=GROUP_ID,
        board=BOARD_ID,
        project=PROJECT_ID,
        priority=TaskPriority.Low,
        completed=True,
        description="This is a simple task with only a description. No files are attached to this task."
    )

    try:
        response = client.create_task(task)
        print("Task with description only created successfully!")
        print(f"Task ID: {response.task.id}")
        print(f"Document ID: {response.payload['task']['document']}")
        print("Note: API accepts description but doesn't return it in response.")
        print("Description is stored in a separate document and can be accessed via separate API calls.")
        return response.task.id
    except Exception as e:
        print(f"Error creating task with description only: {e}")
        return None

if __name__ == "__main__":
    print("="*60)
    print("CREATING TASKS WITH REAL FILES FROM ASSETS")
    print("="*60)
    
    print("\n1. Creating task with description and real PDF file...")
    create_task_with_description_and_files()
    
    print("\n" + "="*50 + "\n")
    
    print("2. Creating task with multiple real files (PDF, PNG, MP4)...")
    create_task_with_multiple_files()
    
    print("\n" + "="*50 + "\n")
    
    print("3. Creating task with description only...")
    create_task_with_description_only() 