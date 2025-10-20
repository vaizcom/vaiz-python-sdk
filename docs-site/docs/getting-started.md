---
sidebar_position: 2
slug: /
---

# Getting Started

Get up and running with Vaiz SDK in minutes! 🚀

## Installation

Install the SDK using pip:

```bash
pip install vaiz-sdk
```

Or add to your `requirements.txt`:

```txt
vaiz-sdk>=0.5.0
```

## Environment Setup

### Environment Variables

Create a `.env` file in your project root:

```env
VAIZ_API_KEY=your_api_key
VAIZ_SPACE_ID=your_space_id
```

:::tip Where to get API key?
You can get your API key from your workspace settings on the Vaiz platform.
:::

### Loading Variables

```python
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("VAIZ_API_KEY")
space_id = os.getenv("VAIZ_SPACE_ID")
```

## Creating a Client

### Production Environment

```python
from vaiz import VaizClient

# For production use (verify_ssl=True by default)
client = VaizClient(
    api_key="your_api_key",
    space_id="your_space_id"
)
```

### Local Development

If you're using self-signed certificates for local development:

```python
client = VaizClient(
    api_key="your_api_key",
    space_id="your_space_id",
    verify_ssl=False,  # Only for local development!
    base_url="http://localhost:3000"  # Local server URL
)
```

:::warning Important
Use `verify_ssl=False` only in local development. Always use `verify_ssl=True` (default) in production.
:::

## Your First Task

Let's create your first task:

```python
from vaiz import VaizClient
from vaiz.models import CreateTaskRequest, TaskPriority
from datetime import datetime

# Create client
client = VaizClient(
    api_key="your_api_key",
    space_id="your_space_id"
)

# Create task
task = CreateTaskRequest(
    name="My First Task",
    board="your_board_id",
    group="your_group_id",
    project="your_project_id",
    priority=TaskPriority.High,
    description="Task description",
    due_start=datetime(2025, 2, 1),
    due_end=datetime(2025, 2, 15)
)

# Send request
response = client.create_task(task)

# Get created task
created_task = response.task
print(f"✅ Task created: {created_task.name}")
print(f"📅 Deadline: {created_task.due_end}")
print(f"🆔 ID: {created_task.id}")
```

## Fetching Tasks

```python
from vaiz.models import GetTasksRequest

# Get all incomplete tasks
request = GetTasksRequest(
    completed=False,
    limit=50
)

response = client.get_tasks(request)

print(f"Found {len(response.payload.tasks)} tasks")
for task in response.payload.tasks:
    print(f"- {task.hrid}: {task.name}")
```

## Getting Projects

```python
# Get all projects
response = client.get_projects()

for project in response.projects:
    print(f"📁 Project: {project.name}")
    print(f"   Color: {project.color}")
```

## Working with Milestones

```python
from vaiz.models import CreateMilestoneRequest
from datetime import datetime

# Create milestone
milestone = CreateMilestoneRequest(
    name="Q1 2025",
    board="board_id",
    project="project_id",
    description="First quarter tasks",
    due_start=datetime(2025, 1, 1),
    due_end=datetime(2025, 3, 31)
)

response = client.create_milestone(milestone)
print(f"✅ Milestone created: {response.milestone.name}")
```

## Uploading Files

```python
from vaiz.models.enums import EUploadFileType

# Upload file
response = client.upload_file(
    "/path/to/document.pdf",
    file_type=EUploadFileType.Pdf
)

file = response.file
print(f"✅ File uploaded: {file.name}")
print(f"🔗 URL: {file.url}")
```

## Error Handling

```python
from requests.exceptions import HTTPError

try:
    response = client.get_task("invalid_task_id")
except HTTPError as e:
    print(f"❌ HTTP Error: {e}")
    print(f"   Status: {e.response.status_code}")
    print(f"   Response: {e.response.text}")
except Exception as e:
    print(f"❌ Unknown error: {e}")
```

## Next Steps

Now you know the basics of working with Vaiz SDK! Here's what to explore next:

- 📖 [API Reference](./api/client) - Complete documentation of all methods
- 🎛️ [Custom Fields](./guides/custom-fields) - Working with custom fields
- 💬 [Comments](./api/comments) - Create and manage comments
- 📁 [Files](./api/files) - Upload and attach files
- 💡 [Examples](./examples) - Ready-to-use examples for different scenarios

## Useful Links

- [GitHub Repository](https://github.com/vaizcom/vaiz-python-sdk)
- [PyPI Package](https://pypi.org/project/vaiz-sdk/)
- [Changelog](https://github.com/vaizcom/vaiz-python-sdk/blob/main/CHANGELOG.md)

