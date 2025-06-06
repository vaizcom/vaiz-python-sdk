from vaiz import VaizClient
from vaiz.models import CreateTaskRequest, TaskPriority, CustomField
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("VAIZ_API_KEY")
if not API_KEY:
    raise ValueError("Please set VAIZ_API_KEY environment variable or create a .env file with VAIZ_API_KEY=your_api_key")

SPACE_ID = os.getenv("VAIZ_SPACE_ID") 

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
        value='723565327a2d39495a613449'
    )],
    rightConnectors=[],
    leftConnectors=[]
)

try:
    response = client.create_task(task)
    print("Task created successfully!")
    print(f"Response type: {response.type}")
    print(f"Task data: {response.payload}")
except Exception as e:
    print(f"Error creating task: {e}")
    if hasattr(e, 'response') and e.response is not None:
        print(f"Response content: {e.response.text}")