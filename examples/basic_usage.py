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

client = VaizClient(api_key=API_KEY, space_id=SPACE_ID)

task = CreateTaskRequest(
    name="Test task 123",
    group="649bea169d17e4070e0337f8",
    board="649bea169d17e4070e0337f7",
    project="649bea169d17e4070e0337f3",
    priority=TaskPriority.High,
    completed=True,
    types=["649bea169d17e4070e0337fa"],
    assignees=["6396e0b66aad7061fa174ea8"],
    subtasks=[],
    milestones=[],
    customFields=[CustomField(
        id='684308de140fff60952cd4ac',
        value=['723565327a2d39495a613449','713037655235784d52416368']
    )],
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
        assignees=["6396e0b66aad7061fa174ea8"],
        customFields=[CustomField(
            id='684308de140fff60952cd4ac',
            value='713037655235784d52416368'
        )]
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