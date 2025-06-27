"""
Example: Edit a task to add description and files using the Vaiz SDK.
This example shows how to modify an existing task to include files and description.
"""

from vaiz.models import EditTaskRequest, TaskFile, CreateTaskRequest, TaskPriority
from vaiz.models.enums import EUploadFileType
from .config import get_client, BOARD_ID, GROUP_ID, PROJECT_ID

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
        completed=False
    )
    
    try:
        create_response = client.create_task(simple_task)
        task_id = create_response.payload['task']['_id']
        print(f"Task created with ID: {task_id}")
    except Exception as e:
        print(f"Error creating initial task: {e}")
        return None
    
    # Step 2: Upload a file
    print("\nStep 2: Uploading file...")
    file_path = "./example.pdf"  # Replace with path to your file
    try:
        upload_response = client.upload_file(file_path, file_type=EUploadFileType.Pdf)
        uploaded_file = upload_response.file
        print(f"File uploaded successfully!")
        print(f"File ID: {uploaded_file.id}")
        print(f"File URL: {uploaded_file.url}")
    except FileNotFoundError:
        print(f"File {file_path} not found. Using mock file data for demonstration.")
        # Mock file data for demonstration
        uploaded_file = type('MockFile', (), {
            'id': 'mock_file_id_456',
            'url': 'http://example.com/mock_file.pdf',
            'name': 'mock_file.pdf',
            'type': EUploadFileType.Pdf,
            'ext': 'pdf',
            'dimension': [0, 0]
        })()
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
        name="Updated Task with Files",
        description="This task has been updated to include a description and attached files. The files provide additional context and resources for completing the task.",
        files=[task_file]
    )

    try:
        response = client.edit_task(edit_task)
        print("Task updated successfully!")
        print(f"Updated task name: {response.payload['task']['name']}")
        print(f"Description: {response.payload['task'].get('description', 'No description')}")
        print(f"Number of files: {len(response.payload['task'].get('files', []))}")
        return response.payload['task']['_id']
    except Exception as e:
        print(f"Error updating task: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response content: {e.response.text}")
        return None

def edit_task_add_multiple_files():
    """Edit a task to add multiple files."""
    client = get_client()
    
    # First, create a simple task
    print("Step 1: Creating a simple task...")
    simple_task = CreateTaskRequest(
        name="Task for Multiple Files",
        group=GROUP_ID,
        board=BOARD_ID,
        project=PROJECT_ID,
        priority=TaskPriority.High,
        completed=False
    )
    
    try:
        create_response = client.create_task(simple_task)
        task_id = create_response.payload['task']['_id']
        print(f"Task created with ID: {task_id}")
    except Exception as e:
        print(f"Error creating initial task: {e}")
        return None
    
    # Step 2: Create mock files (in real usage, you would upload actual files)
    print("\nStep 2: Preparing multiple files...")
    mock_files = [
        {
            'id': 'file_1_789',
            'url': 'http://example.com/specification.pdf',
            'name': 'specification.pdf',
            'type': EUploadFileType.Pdf,
            'ext': 'pdf',
            'dimension': [0, 0]
        },
        {
            'id': 'file_2_101',
            'url': 'http://example.com/wireframe.png',
            'name': 'wireframe.png',
            'type': EUploadFileType.Image,
            'ext': 'png',
            'dimension': [1200, 800]
        },
        {
            'id': 'file_3_112',
            'url': 'http://example.com/demo.mp4',
            'name': 'demo.mp4',
            'type': EUploadFileType.Video,
            'ext': 'mp4',
            'dimension': [1920, 1080]
        }
    ]
    
    # Convert mock files to TaskFile objects
    task_files = [
        TaskFile(
            url=file['url'],
            name=file['name'],
            dimension=file['dimension'],
            ext=file['ext'],
            _id=file['id'],
            type=file['type']
        )
        for file in mock_files
    ]
    
    # Step 3: Edit the task to add multiple files
    print("\nStep 3: Editing task to add multiple files...")
    
    edit_task = EditTaskRequest(
        taskId=task_id,
        name="Task with Multiple Attachments",
        description="This task now includes multiple file attachments: specification document, wireframe image, and demo video.",
        files=task_files
    )

    try:
        response = client.edit_task(edit_task)
        print("Task updated with multiple files successfully!")
        print(f"Updated task name: {response.payload['task']['name']}")
        print(f"Description: {response.payload['task'].get('description', 'No description')}")
        print(f"Number of files: {len(response.payload['task'].get('files', []))}")
        for i, file in enumerate(response.payload['task'].get('files', [])):
            print(f"File {i+1}: {file.get('name')} ({file.get('type')})")
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
        completed=False
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
        print(f"New description: {response.payload['task'].get('description', 'No description')}")
        return response.payload['task']['_id']
    except Exception as e:
        print(f"Error updating task description: {e}")
        return None

if __name__ == "__main__":
    print("Editing task to add files and description...")
    edit_task_with_files()
    
    print("\n" + "="*50 + "\n")
    
    print("Editing task to add multiple files...")
    edit_task_add_multiple_files()
    
    print("\n" + "="*50 + "\n")
    
    print("Editing task to update description only...")
    edit_task_update_description_only() 