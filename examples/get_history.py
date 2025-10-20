import os
from dotenv import load_dotenv
from vaiz import VaizClient
from vaiz.models import GetHistoryRequest, CreateTaskRequest, TaskPriority
from vaiz.models.enums import Kind

load_dotenv()

API_KEY = os.getenv("VAIZ_API_KEY", "your_api_key")
SPACE_ID = os.getenv("VAIZ_SPACE_ID", "your_space_id")
BOARD_ID = os.getenv("VAIZ_BOARD_ID")
GROUP_ID = os.getenv("VAIZ_GROUP_ID")
PROJECT_ID = os.getenv("VAIZ_PROJECT_ID")

client = VaizClient(api_key=API_KEY, space_id=SPACE_ID, base_url="https://api.vaiz.local:10000/v4", verify_ssl=False)

# Create a test task (or use an existing one)
if not all([BOARD_ID, GROUP_ID, PROJECT_ID]):
    raise RuntimeError("Set VAIZ_BOARD_ID, VAIZ_GROUP_ID, VAIZ_PROJECT_ID in your .env")

task = CreateTaskRequest(
    name="Example Task for History",
    group=str(GROUP_ID),
    board=str(BOARD_ID),
    project=str(PROJECT_ID),
    priority=TaskPriority.Medium,
    completed=False
)
response = client.create_task(task)
task_id = response.payload["task"]["_id"]

# Get history for the newly created task
request = GetHistoryRequest(
    kind=Kind.Task,
    kindId=task_id,
    excludeKeys=["TASK_COMMENTED", "MILESTONE_COMMENTED", "DOCUMENT_COMMENTED"],
    lastLoadedDate=0
)
history_response = client.get_history(request)

print(f"Type: {history_response.type}")
print(f"Number of histories: {len(history_response.payload.histories)}")
for history in history_response.payload.histories:
    print(f"History key: {history.key}, createdAt: {history.createdAt}, data: {history.data}") 