#!/usr/bin/env python3
"""
Example: Creating tasks with optional description and file upload using the unified create_task method
This example demonstrates how to use the create_task method with optional description and file parameters.
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from examples.config import GROUP_ID, BOARD_ID, PROJECT_ID, get_client
from vaiz.client import VaizClient
from vaiz.models import CreateTaskRequest, TaskPriority, TaskUploadFile
from vaiz.models.enums import UploadFileType


def main():
    print("=" * 60)
    print("CREATING TASKS WITH UNIFIED METHOD")
    print("=" * 60)
    
    # Initialize client
    client = get_client()
    
    print("\n1. Creating task with description only...")
    try:
        task = CreateTaskRequest(
            name="Task with Description",
            group=GROUP_ID,
            board=BOARD_ID,
            project=PROJECT_ID,
            completed=True
        )
        
        response = client.create_task(
            task, 
            description="This is a task with a description set via parameter."
        )
        print("✓ Task created successfully!")
        try:
            print(f"Task ID: {response.task.id}")
        except AttributeError:
            print(f"Task attributes: {dir(response.task)}")
        print(f"Task name: {response.task.name}")
        print(f"Document ID: {response.task.document}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "=" * 50)
    
    print("\n2. Creating task with automatic file upload (auto-detected type)...")
    try:
        task = CreateTaskRequest(
            name="Task with Auto-Uploaded PDF",
            group=GROUP_ID,
            board=BOARD_ID,
            project=PROJECT_ID,
            completed=True
        )
        
        file = TaskUploadFile(path='./assets/example.pdf')
        response = client.create_task(
            task, 
            description="This task has a PDF file uploaded automatically.",
            file=file
        )
        print("✓ Task created successfully!")
        try:
            print(f"Task ID: {response.task.id}")
        except AttributeError:
            print(f"Task attributes: {dir(response.task)}")
        print(f"Task name: {response.task.name}")
        print(f"Document ID: {response.task.document}")
        print("Note: File type was auto-detected as PDF")
        
    except FileNotFoundError as e:
        print(f"❌ File not found: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "=" * 50)
    
    print("\n3. Creating task with explicit file type...")
    try:
        task = CreateTaskRequest(
            name="Task with Explicit File Type",
            group=GROUP_ID,
            board=BOARD_ID,
            project=PROJECT_ID,
            completed=True
        )
        
        file = TaskUploadFile(path='./assets/example.png', type=EUploadFileType.Image)
        response = client.create_task(
            task, 
            description="This task has a PNG file with explicit type specification.",
            file=file
        )
        print("✓ Task created successfully!")
        try:
            print(f"Task ID: {response.task.id}")
        except AttributeError:
            print(f"Task attributes: {dir(response.task)}")
        print(f"Task name: {response.task.name}")
        print(f"Document ID: {response.task.document}")
        print("Note: File type was explicitly specified as Image")
        
    except FileNotFoundError as e:
        print(f"❌ File not found: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "=" * 50)
    
    print("\n4. Creating task with video file...")
    try:
        task = CreateTaskRequest(
            name="Task with Video File",
            group=GROUP_ID,
            board=BOARD_ID,
            project=PROJECT_ID,
            priority=TaskPriority.High,
            completed=True
        )
        
        file = TaskUploadFile(path='./assets/example.mp4')
        response = client.create_task(
            task, 
            description="This task has an MP4 video file.",
            file=file
        )
        print("✓ Task created successfully!")
        try:
            print(f"Task ID: {response.task.id}")
        except AttributeError:
            print(f"Task attributes: {dir(response.task)}")
        print(f"Task name: {response.task.name}")
        print(f"Priority: {response.task.priority}")
        print(f"Document ID: {response.task.document}")
        print("Note: File type was auto-detected as Video")
        
    except FileNotFoundError as e:
        print(f"❌ File not found: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "=" * 50)
    
    print("\n5. Creating task without description or file...")
    try:
        task = CreateTaskRequest(
            name="Simple Task",
            group=GROUP_ID,
            board=BOARD_ID,
            project=PROJECT_ID,
            completed=True
        )
        
        response = client.create_task(task)
        print("✓ Task created successfully!")
        print(f"Task ID: {response.task.id}")
        print(f"Task name: {response.task.name}")
        print(f"Document ID: {response.task.document}")
        print("Note: No description or file provided")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print("The unified create_task method supports:")
    print("• Creating tasks with description only")
    print("• Creating tasks with file upload only")
    print("• Creating tasks with both description and file")
    print("• Automatic file type detection")
    print("• Explicit file type specification")
    print("• All existing CreateTaskRequest functionality")
    print("• Type safety and proper error handling")


if __name__ == "__main__":
    main() 