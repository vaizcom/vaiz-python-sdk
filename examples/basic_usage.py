"""
Basic usage example of the Vaiz Python SDK.

This example demonstrates how to:
1. Initialize the Vaiz client
2. Create a new task
3. Edit an existing task

The SDK is organized into modules:
- vaiz.client: Main client interface
- vaiz.api.base: Base API client with common functionality
- vaiz.api.tasks: Task-specific API operations
"""

from vaiz import VaizClient
from vaiz.models import CreateTaskRequest, TaskPriority, CustomField, EditTaskRequest
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variable
API_KEY = os.getenv("VAIZ_API_KEY")
if not API_KEY:
    raise ValueError("Please set VAIZ_API_KEY environment variable or create a .env file with VAIZ_API_KEY=your_api_key")

SPACE_ID = os.getenv("VAIZ_SPACE_ID")  # Replace with your actual space ID
BOARD_ID = "68455de3e48da05d905c51e1"
GROUP_ID = "68455de3e48da05d905c51e2"
PROJECT_ID = "676d6758c6ea65cbc1f06d81"
ASSIGNEE_ID = "676d6758c6ea65cbc1f06d70"

client = VaizClient(api_key=API_KEY, space_id=SPACE_ID, verify_ssl=False, base_url="https://api.vaiz.local:10000/v4")

task = CreateTaskRequest(
    name="Test task 123",
    group=GROUP_ID,
    board=BOARD_ID,
    project=PROJECT_ID,
    priority=TaskPriority.High,
    completed=True,
    types=["649bea169d17e4070e0337fa"],
    # assignees=[ASSIGNEE_ID],
    subtasks=[],
    milestones=[],
    # customFields=[CustomField(
    #     id='684308de140fff60952cd4ac',
    #     value=['723565327a2d39495a613449','713037655235784d52416368']
    # )],
    rightConnectors=[],
    leftConnectors=[]
)

try:
    response = client.create_task(task)
    print("Task created successfully!")
    print(f"Response type: {response.type}")
    print(f"Task data: {response.payload}")

    # Get the task ID from the response
    task_id = response.payload['task']['_id']
    
    # Example of editing a task
    print("\nEditing task...")
    edit_task = EditTaskRequest(
        taskId=task_id,
        name="Updated task name",
        assignees=[ASSIGNEE_ID],
        # customFields=[CustomField(
        #     id='684308de140fff60952cd4ac',
        #     value='713037655235784d52416368'
        # )]
    )

    try:
        edit_response = client.edit_task(edit_task)
        print("Task updated successfully!")
        print(f"Response type: {edit_response.type}")
        print(f"Updated task data: {edit_response.payload}")
    except Exception as e:
        print(f"Error updating task: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response content: {e.response.text}")
except Exception as e:
    print(f"Error creating task: {e}")
    if hasattr(e, 'response') and e.response is not None:
        print(f"Response content: {e.response.text}")