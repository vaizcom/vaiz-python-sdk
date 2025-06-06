from vaiz import VaizClient
from vaiz.models import CreateTaskRequest
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
    priority=1,
    completed=False,
    types=["649bea169d17e4070e0337fa"],
    assignees=[],
    subtasks=[],
    milestones=[],
    customFields=[],
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