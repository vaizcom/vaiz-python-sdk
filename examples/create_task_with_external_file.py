"""
Example: Create a task with an external file uploaded from URL using the Vaiz SDK.

This example demonstrates the complete workflow:
1. Upload a file from an external URL
2. Create a TaskFile object from the uploaded file  
3. Create a task with the attached file
"""

from .config import get_client
from vaiz.models.enums import EUploadFileType
from vaiz.models import CreateTaskRequest, TaskPriority, TaskFile

def create_task_with_external_image():
    """
    Example: Create a task with an external image uploaded from URL.
    """
    client = get_client()
    
    # External image URL - you can replace with any image URL
    external_image_url = "https://httpbin.org/image/png"
    
    try:
        print("Step 1: Uploading external file from URL...")
        
        # Upload the external file
        upload_response = client.upload_file_from_url(
            file_url=external_image_url,
            file_type=EUploadFileType.Image,
            filename="project_mockup.png"
        )
        
        uploaded_file = upload_response.file
        print(f"✓ File uploaded successfully!")
        print(f"  File ID: {uploaded_file.id}")
        print(f"  File name: {uploaded_file.name}")
        print(f"  File URL: {uploaded_file.url}")
        print(f"  File type: {uploaded_file.type}")
        print(f"  File size: {uploaded_file.size} bytes")
        
        print("\nStep 2: Creating TaskFile object...")
        
        # Create TaskFile object from uploaded file
        task_file = TaskFile(
            url=uploaded_file.url,
            name=uploaded_file.name,
            dimension=uploaded_file.dimension,
            ext=uploaded_file.ext,
            _id=uploaded_file.id,
            type=uploaded_file.type
        )
        
        print("✓ TaskFile object created")
        
        print("\nStep 3: Creating task with attached file...")
        
        # Create task with the external file attached
        # Note: Replace these IDs with your actual board/group/project IDs
        task_request = CreateTaskRequest(
            name="Design Review Task",
            group="YOUR_GROUP_ID",      # Replace with actual group ID
            board="YOUR_BOARD_ID",      # Replace with actual board ID
            project="YOUR_PROJECT_ID",  # Replace with actual project ID
            priority=TaskPriority.High,
            completed=False,
            description=f"Please review the design mockup. Original source: {external_image_url}",
            files=[task_file]
        )
        
        task_response = client.create_task(task_request)
        created_task = task_response.payload["task"]
        
        print(f"✓ Task created successfully!")
        print(f"  Task ID: {created_task['_id']}")
        print(f"  Task name: {created_task['name']}")
        print(f"  Priority: {created_task['priority']}")
        print(f"  Files attached: 1")
        
        return created_task["_id"]
        
    except Exception as e:
        print(f"Error: {e}")
        return None

def create_task_with_multiple_external_files():
    """
    Example: Create a task with multiple external files from different URLs.
    """
    client = get_client()
    
    # Multiple external files to upload
    external_files = [
        {
            "url": "https://httpbin.org/image/png",
            "type": EUploadFileType.Image,
            "filename": "screenshot_1.png"
        },
        {
            "url": "https://httpbin.org/image/png",
            "type": EUploadFileType.Image,
            "filename": "screenshot_2.png"
        },
        {
            "url": "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf",
            "type": EUploadFileType.Pdf,
            "filename": "requirements_doc.pdf"
        }
    ]
    
    try:
        print(f"Step 1: Uploading {len(external_files)} external files...")
        
        task_files = []
        
        for i, file_info in enumerate(external_files, 1):
            print(f"  Uploading file {i}/{len(external_files)}: {file_info['filename']}")
            
            # Upload each external file
            upload_response = client.upload_file_from_url(
                file_url=file_info["url"],
                file_type=file_info["type"],
                filename=file_info["filename"]
            )
            
            uploaded_file = upload_response.file
            
            # Create TaskFile object
            task_file = TaskFile(
                url=uploaded_file.url,
                name=uploaded_file.name,
                dimension=uploaded_file.dimension,
                ext=uploaded_file.ext,
                _id=uploaded_file.id,
                type=uploaded_file.type
            )
            
            task_files.append(task_file)
            print(f"    ✓ {file_info['filename']} uploaded ({uploaded_file.size} bytes)")
        
        print(f"\n✓ All {len(task_files)} files uploaded successfully!")
        
        print("\nStep 2: Creating task with multiple attached files...")
        
        # Create task with multiple external files attached
        # Note: Replace these IDs with your actual board/group/project IDs
        task_request = CreateTaskRequest(
            name="Multi-Asset Review Task", 
            group="YOUR_GROUP_ID",      # Replace with actual group ID
            board="YOUR_BOARD_ID",      # Replace with actual board ID
            project="YOUR_PROJECT_ID",  # Replace with actual project ID
            priority=TaskPriority.Medium,
            completed=False,
            description="Review all attached assets and provide feedback. All files were downloaded from external sources.",
            files=task_files
        )
        
        task_response = client.create_task(task_request)
        created_task = task_response.payload["task"]
        
        print(f"✓ Task created successfully!")
        print(f"  Task ID: {created_task['_id']}")
        print(f"  Task name: {created_task['name']}")
        print(f"  Priority: {created_task['priority']}")
        print(f"  Files attached: {len(task_files)}")
        
        print("\n  Attached files:")
        for i, task_file in enumerate(task_files, 1):
            print(f"    {i}. {task_file.name} ({task_file.type})")
        
        return created_task["_id"]
        
    except Exception as e:
        print(f"Error: {e}")
        return None

def create_task_with_auto_detected_file():
    """
    Example: Create a task with an external file using automatic type detection.
    """
    client = get_client()
    
    # External file URL without explicit type specification
    external_file_url = "https://httpbin.org/image/png"
    
    try:
        print("Step 1: Uploading external file with auto-detection...")
        
        # Upload with automatic type detection (no file_type specified)
        upload_response = client.upload_file_from_url(external_file_url)
        
        uploaded_file = upload_response.file
        print(f"✓ File uploaded with auto-detected type!")
        print(f"  Detected type: {uploaded_file.type}")
        print(f"  File name: {uploaded_file.name}")
        print(f"  File size: {uploaded_file.size} bytes")
        
        # Create TaskFile object
        task_file = TaskFile(
            url=uploaded_file.url,
            name=uploaded_file.name,
            dimension=uploaded_file.dimension,
            ext=uploaded_file.ext,
            _id=uploaded_file.id,
            type=uploaded_file.type
        )
        
        print("\nStep 2: Creating task...")
        
        # Create task
        # Note: Replace these IDs with your actual board/group/project IDs
        task_request = CreateTaskRequest(
            name="Auto-Detected File Task",
            group="YOUR_GROUP_ID",      # Replace with actual group ID
            board="YOUR_BOARD_ID",      # Replace with actual board ID  
            project="YOUR_PROJECT_ID",  # Replace with actual project ID
            priority=TaskPriority.Low,
            completed=False,
            description=f"Task created with auto-detected file type: {uploaded_file.type}",
            files=[task_file]
        )
        
        task_response = client.create_task(task_request)
        created_task = task_response.payload["task"]
        
        print(f"✓ Task created successfully!")
        print(f"  Task ID: {created_task['_id']}")
        print(f"  File type was auto-detected as: {uploaded_file.type}")
        
        return created_task["_id"]
        
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    print("=== Create Task with External Image ===")
    task_id_1 = create_task_with_external_image()
    
    print("\n" + "="*50)
    print("=== Create Task with Multiple External Files ===")
    task_id_2 = create_task_with_multiple_external_files()
    
    print("\n" + "="*50)
    print("=== Create Task with Auto-Detected File ===")
    task_id_3 = create_task_with_auto_detected_file()
    
    print("\n" + "="*50)
    print("Summary:")
    if task_id_1:
        print(f"  ✓ Single file task created: {task_id_1}")
    if task_id_2:
        print(f"  ✓ Multiple files task created: {task_id_2}")
    if task_id_3:
        print(f"  ✓ Auto-detected file task created: {task_id_3}") 