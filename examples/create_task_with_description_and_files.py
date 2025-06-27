"""
Example: Create a task with description and files using the Vaiz SDK.
This example shows the complete workflow: upload file first, then create task with file info.
"""

from vaiz.models import CreateTaskRequest, TaskPriority, TaskFile
from vaiz.models.enums import EUploadFileType
from .config import get_client, BOARD_ID, GROUP_ID, PROJECT_ID

def create_task_with_description_and_files():
    """Create a new task with description and files using the Vaiz SDK."""
    client = get_client()
    
    # Step 1: Upload a file first
    print("Step 1: Uploading file...")
    file_path = "./example.pdf"  # Replace with path to your file
    try:
        upload_response = client.upload_file(file_path, file_type=EUploadFileType.Pdf)
        uploaded_file = upload_response.file
        print(f"File uploaded successfully!")
        print(f"File ID: {uploaded_file.id}")
        print(f"File URL: {uploaded_file.url}")
        print(f"File name: {uploaded_file.name}")
        print(f"File type: {uploaded_file.type}")
    except FileNotFoundError:
        print(f"File {file_path} not found. Using mock file data for demonstration.")
        # Mock file data for demonstration
        uploaded_file = type('MockFile', (), {
            'id': 'mock_file_id_123',
            'url': 'http://example.com/mock_file.pdf',
            'name': 'mock_file.pdf',
            'type': EUploadFileType.Pdf,
            'ext': 'pdf',
            'dimension': [0, 0]
        })()
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
        _id=uploaded_file.id,
        type=uploaded_file.type
    )
    
    task = CreateTaskRequest(
        name="Task with Description and Files",
        group=GROUP_ID,
        board=BOARD_ID,
        project=PROJECT_ID,
        priority=TaskPriority.High,
        completed=False,
        description="This is a task with a detailed description and attached files. The task includes important documentation and resources.",
        files=[task_file]
    )

    try:
        response = client.create_task(task)
        print("Task with description and files created successfully!")
        print(f"Response type: {response.type}")
        print(f"Task ID: {response.payload['task']['_id']}")
        print(f"Task name: {response.payload['task']['name']}")
        print(f"Document ID: {response.payload['task']['document']}")
        print("Note: API accepts description and files but doesn't return them in response.")
        print("Description and files are stored and can be accessed via separate API calls.")
        return response.payload['task']['_id']
    except Exception as e:
        print(f"Error creating task with description and files: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response content: {e.response.text}")
        return None

def create_task_with_multiple_files():
    """Create a task with multiple files of different types."""
    client = get_client()
    
    # Mock files for demonstration (in real usage, you would upload actual files)
    mock_files = [
        {
            'id': 'file_1_123',
            'url': 'http://example.com/document.pdf',
            'name': 'document.pdf',
            'type': EUploadFileType.Pdf,
            'ext': 'pdf',
            'dimension': [0, 0]
        },
        {
            'id': 'file_2_456',
            'url': 'http://example.com/image.jpg',
            'name': 'image.jpg',
            'type': EUploadFileType.Image,
            'ext': 'jpg',
            'dimension': [1920, 1080]
        },
        {
            'id': 'file_3_789',
            'url': 'http://example.com/video.mp4',
            'name': 'video.mp4',
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
    
    task = CreateTaskRequest(
        name="Task with Multiple Files",
        group=GROUP_ID,
        board=BOARD_ID,
        project=PROJECT_ID,
        priority=TaskPriority.Medium,
        completed=False,
        description="This task contains multiple file attachments: PDF document, image, and video.",
        files=task_files
    )

    try:
        response = client.create_task(task)
        print("Task with multiple files created successfully!")
        print(f"Task ID: {response.payload['task']['_id']}")
        print(f"Document ID: {response.payload['task']['document']}")
        print("Note: API accepts multiple files but doesn't return them in response.")
        print("Files are stored and can be accessed via separate API calls.")
        return response.payload['task']['_id']
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
        print(f"Task ID: {response.payload['task']['_id']}")
        print(f"Document ID: {response.payload['task']['document']}")
        print("Note: API accepts description but doesn't return it in response.")
        print("Description is stored in a separate document and can be accessed via separate API calls.")
        return response.payload['task']['_id']
    except Exception as e:
        print(f"Error creating task with description only: {e}")
        return None

if __name__ == "__main__":
    print("Creating task with description and files...")
    create_task_with_description_and_files()
    
    print("\n" + "="*50 + "\n")
    
    print("Creating task with multiple files...")
    create_task_with_multiple_files()
    
    print("\n" + "="*50 + "\n")
    
    print("Creating task with description only...")
    create_task_with_description_only() 