---
sidebar_position: 4
---

# Examples

Practical examples for common use cases with the Vaiz SDK.

## Basic Task Management

### Create a Simple Task

```python
from vaiz import VaizClient
from vaiz.models import CreateTaskRequest, TaskPriority

client = VaizClient(api_key="...", space_id="...")

task = CreateTaskRequest(
    name="Implement user authentication",
    board="board_id",
    group="group_id",
    project="project_id",
    priority=TaskPriority.High
)

response = client.create_task(task)
print(f"✅ Created task: {response.task.hrid}")
```

### Update Task Status

```python
from vaiz.models import EditTaskRequest

edit = EditTaskRequest(
    task_id="task_id",
    completed=True
)

client.edit_task(edit)
print("✅ Task marked as complete")
```

### Get My Tasks

```python
from vaiz.models import GetTasksRequest

request = GetTasksRequest(
    assignees=["my_user_id"],
    completed=False,
    limit=50
)

response = client.get_tasks(request)

print(f"You have {len(response.payload.tasks)} tasks:")
for task in response.payload.tasks:
    print(f"  - [{task.priority}] {task.name}")
```

## Working with Files

### Upload and Attach Files to Task

```python
from vaiz.models import CreateTaskRequest, TaskFile
from vaiz.models.enums import EUploadFileType

# Upload files
doc = client.upload_file("design.pdf", EUploadFileType.Pdf)
img = client.upload_file("mockup.png", EUploadFileType.Image)

# Create TaskFile objects
task_files = [
    TaskFile(
        url=doc.file.url,
        name=doc.file.name,
        ext=doc.file.ext,
        id=doc.file.id,
        type=doc.file.type,
        dimension=doc.file.dimension
    ),
    TaskFile(
        url=img.file.url,
        name=img.file.name,
        ext=img.file.ext,
        id=img.file.id,
        type=img.file.type,
        dimension=img.file.dimension
    )
]

# Create task with files
task = CreateTaskRequest(
    name="Review Design",
    board="board_id",
    group="group_id",
    files=task_files
)

response = client.create_task(task)
print(f"✅ Task created with {len(task_files)} files")
```

### Download Files from URL

```python
response = client.upload_file_from_url(
    "https://example.com/report.pdf",
    file_type=EUploadFileType.Pdf,
    filename="monthly_report.pdf"
)

print(f"✅ Uploaded: {response.file.name}")
print(f"🔗 URL: {response.file.url}")
```

## Comments and Discussions

### Add Comment with Files

```python
from vaiz.models.enums import EUploadFileType

# Upload screenshot
screenshot = client.upload_file(
    "bug_screenshot.png",
    EUploadFileType.Image
)

# Post comment
response = client.post_comment(
    document_id="task_document_id",
    content="<p>Found a bug, see screenshot</p>",
    file_ids=[screenshot.file.id]
)

print(f"✅ Comment posted: {response.comment.id}")
```

### Reply to Comment

```python
# Get original comment
comments = client.get_comments("document_id")
original = comments.comments[0]

# Reply
reply = client.post_comment(
    document_id="document_id",
    content="<p>Thanks, I'll fix it!</p>",
    reply_to=original.id
)
```

### Add Reactions

```python
from vaiz.models import CommentReactionType

# Add thumbs up
client.add_reaction(
    comment_id="comment_id",
    reaction=CommentReactionType.THUMBS_UP
)

# Add heart
client.add_reaction(
    comment_id="comment_id",
    reaction=CommentReactionType.HEART
)
```

## Milestones and Planning

### Create Quarterly Milestones

```python
from vaiz.models import CreateMilestoneRequest
from datetime import datetime

quarters = [
    ("Q1 2025", datetime(2025, 1, 1), datetime(2025, 3, 31)),
    ("Q2 2025", datetime(2025, 4, 1), datetime(2025, 6, 30)),
    ("Q3 2025", datetime(2025, 7, 1), datetime(2025, 9, 30)),
    ("Q4 2025", datetime(2025, 10, 1), datetime(2025, 12, 31)),
]

for name, start, end in quarters:
    milestone = CreateMilestoneRequest(
        name=name,
        board="board_id",
        project="project_id",
        due_start=start,
        due_end=end
    )
    
    response = client.create_milestone(milestone)
    print(f"✅ Created: {response.milestone.name}")
```

### Track Milestone Progress

```python
response = client.get_milestones()

for milestone in response.milestones:
    if milestone.total > 0:
        percentage = (milestone.completed / milestone.total) * 100
        print(f"{milestone.name}: {percentage:.0f}% complete")
        print(f"  {milestone.completed}/{milestone.total} tasks")
```

### Attach Milestone to Tasks

```python
from vaiz.models import ToggleMilestoneRequest

request = ToggleMilestoneRequest(
    task_id="task_id",
    milestone_ids=["milestone_id"]
)

response = client.toggle_milestone(request)
print(f"✅ Milestone attached to task: {response.task.name}")
```

## Custom Fields

### Create Custom Fields

```python
from vaiz import make_text_field, make_select_field, make_select_option
from vaiz.models.enums import EColor, EIcon

# Text field
text_field = make_text_field(
    name="Customer Email",
    board_id="board_id",
    description="Customer contact email"
)
client.create_board_custom_field(text_field)

# Select field with options
status_options = [
    make_select_option("🟢 Active", EColor.Green, EIcon.Circle),
    make_select_option("🟡 Pending", EColor.Gold, EIcon.Clock),
    make_select_option("🔴 Blocked", EColor.Red, EIcon.Cancel)
]

select_field = make_select_field(
    name="Status",
    board_id="board_id",
    options=status_options
)
client.create_board_custom_field(select_field)
```

### Set Custom Field Values

```python
from vaiz import make_text_value, make_date_value
from vaiz.models import CreateTaskRequest, CustomField
from datetime import datetime

custom_fields = [
    CustomField(
        id="email_field_id",
        value=make_text_value("customer@example.com")
    ),
    CustomField(
        id="date_field_id",
        value=make_date_value(datetime(2025, 6, 1))
    )
]

task = CreateTaskRequest(
    name="Task with Custom Fields",
    board="board_id",
    group="group_id",
    custom_fields=custom_fields
)

response = client.create_task(task)
```

## Batch Operations

### Create Multiple Tasks

```python
from vaiz.models import CreateTaskRequest, TaskPriority

tasks_to_create = [
    ("Design mockups", TaskPriority.High),
    ("Implement backend", TaskPriority.High),
    ("Write tests", TaskPriority.Medium),
    ("Update documentation", TaskPriority.Low),
]

created_tasks = []

for name, priority in tasks_to_create:
    task = CreateTaskRequest(
        name=name,
        board="board_id",
        group="group_id",
        priority=priority
    )
    
    response = client.create_task(task)
    created_tasks.append(response.task)
    print(f"✅ Created: {name}")

print(f"\nTotal created: {len(created_tasks)} tasks")
```

### Bulk Update Tasks

```python
from vaiz.models import GetTasksRequest, EditTaskRequest

# Get all incomplete tasks
request = GetTasksRequest(
    completed=False,
    project="project_id"
)

response = client.get_tasks(request)

# Update all to high priority
for task in response.payload.tasks:
    edit = EditTaskRequest(
        task_id=task.id,
        priority=TaskPriority.High
    )
    
    client.edit_task(edit)
    print(f"✅ Updated: {task.name}")
```

## Advanced Workflows

### Task with Full Setup

```python
from vaiz.models import CreateTaskRequest, TaskPriority, CustomField, TaskFile
from vaiz.models.enums import EUploadFileType
from vaiz import make_text_value
from datetime import datetime, timedelta

# Upload file
file_response = client.upload_file(
    "requirements.pdf",
    EUploadFileType.Pdf
)

# Prepare task file
task_file = TaskFile(
    url=file_response.file.url,
    name=file_response.file.name,
    ext=file_response.file.ext,
    id=file_response.file.id,
    type=file_response.file.type,
    dimension=file_response.file.dimension
)

# Prepare custom fields
custom_fields = [
    CustomField(
        id="client_field_id",
        value=make_text_value("Acme Corp")
    )
]

# Create comprehensive task
task = CreateTaskRequest(
    name="Build client dashboard",
    description="Create dashboard with real-time analytics",
    board="board_id",
    group="group_id",
    project="project_id",
    priority=TaskPriority.High,
    assignees=["user_id_1", "user_id_2"],
    due_start=datetime.now(),
    due_end=datetime.now() + timedelta(days=14),
    types=["feature_type_id"],
    milestones=["q1_milestone_id"],
    files=[task_file],
    custom_fields=custom_fields
)

response = client.create_task(task)
print(f"✅ Created comprehensive task: {response.task.hrid}")
```

## Error Handling Patterns

### Robust File Upload

```python
import os
from requests.exceptions import HTTPError

def safe_upload(file_path, file_type):
    """Safely upload a file with error handling"""
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        file_size = os.path.getsize(file_path)
        if file_size > 50 * 1024 * 1024:  # 50 MB limit
            raise ValueError(f"File too large: {file_size / 1024 / 1024:.2f} MB")
        
        response = client.upload_file(file_path, file_type=file_type)
        print(f"✅ Uploaded: {response.file.name}")
        return response.file
        
    except HTTPError as e:
        print(f"❌ HTTP Error {e.response.status_code}: {e.response.text}")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

# Usage
file = safe_upload("large_file.pdf", EUploadFileType.Pdf)
```

### Retry Logic

```python
import time
from requests.exceptions import HTTPError

def create_task_with_retry(task_request, max_retries=3):
    """Create task with automatic retry on failure"""
    for attempt in range(max_retries):
        try:
            response = client.create_task(task_request)
            print(f"✅ Task created: {response.task.id}")
            return response
            
        except HTTPError as e:
            if e.response.status_code >= 500 and attempt < max_retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff
                print(f"⚠️ Server error, retrying in {wait_time}s...")
                time.sleep(wait_time)
            else:
                raise
    
    raise Exception("Max retries exceeded")
```

## More Examples

Check out the `/examples` directory in the repository for more code samples:

- Task management examples
- Custom field workflows  
- File upload patterns
- Comment system usage
- Milestone tracking
- Batch operations

[View on GitHub →](https://github.com/vaizcom/vaiz-python-sdk/tree/main/examples)

