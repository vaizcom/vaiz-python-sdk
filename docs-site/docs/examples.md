---
sidebar_position: 4
---

# Patterns & Best Practices

Common patterns, best practices, and real-world scenarios for using the Vaiz SDK effectively.

:::tip Quick Start
For basic usage examples of each API method, see the [API Guides](./api/overview).
For ready-to-run code examples, check the [`/examples`](https://github.com/vaizcom/vaiz-python-sdk/tree/main/examples) directory.
:::

## Environment Setup

### Using Environment Variables

Always use environment variables for credentials:

```python
import os
from dotenv import load_dotenv
from vaiz import VaizClient

# Load from .env file
load_dotenv()

client = VaizClient(
    api_key=os.getenv("VAIZ_API_KEY"),
    space_id=os.getenv("VAIZ_SPACE_ID")
)
```

Create a `.env` file:
```bash
VAIZ_API_KEY=your_api_key_here
VAIZ_SPACE_ID=your_space_id_here
```

### Type Hints for Better IDE Support

```python
from vaiz import VaizClient
from vaiz.models import Task, GetTasksRequest, GetTasksResponse
from typing import List

def get_user_tasks(client: VaizClient, user_id: str) -> List[Task]:
    """Get all tasks assigned to a specific user."""
    request = GetTasksRequest(
        assignees=[user_id],
        completed=False
    )
    
    response: GetTasksResponse = client.get_tasks(request)
    return response.payload.tasks

# Full IDE autocomplete and type checking
tasks = get_user_tasks(client, "user_id")
```

## Common Patterns

### Pagination

Handle large result sets with pagination:

```python
from vaiz.models import GetTasksRequest

def get_all_tasks(client, project_id: str):
    """Get all tasks from a project using pagination."""
    all_tasks = []
    skip = 0
    limit = 50  # Max per request
    
    while True:
        response = client.get_tasks(
            GetTasksRequest(
                project=project_id,
                limit=limit,
                skip=skip
            )
        )
        
        tasks = response.payload.tasks
        if not tasks:
            break
        
        all_tasks.extend(tasks)
        skip += limit
        
        # Last page if less than limit
        if len(tasks) < limit:
            break
    
    return all_tasks

# Usage
all_project_tasks = get_all_tasks(client, "project_id")
print(f"Total tasks: {len(all_project_tasks)}")
```

### Getting Dynamic IDs

Never hardcode IDs - always fetch them dynamically:

```python
# ✅ Good - Get IDs from API
profile = client.get_profile()
member_id = profile.profile.member_id  # For Member documents

projects = client.get_projects()
project_id = projects.projects[0].id

space_id = client.space_id  # From client initialization

# ❌ Bad - Hardcoded IDs
member_id = "68f7519ca65f977ddb66db8e"  # Don't do this!
```

### Caching Considerations

The SDK automatically caches `get_tasks()` for 5 minutes:

```python
from vaiz.models import GetTasksRequest

# First call - hits API
response1 = client.get_tasks(GetTasksRequest(limit=10))

# Second call within 5 min - returns cached data
response2 = client.get_tasks(GetTasksRequest(limit=10))

# Clear cache manually if needed
client.clear_tasks_cache()

# This will hit API again
response3 = client.get_tasks(GetTasksRequest(limit=10))
```

## Working with Documents

### Getting the Right Member ID

For Member (personal) documents, use `member_id` from profile, not user `id`:

```python
# ✅ Correct way
profile = client.get_profile()
member_id = profile.profile.member_id  # Use this!

# Get personal documents
from vaiz.models import GetDocumentsRequest, Kind

docs = client.get_documents(
    GetDocumentsRequest(
        kind=Kind.Member,
        kind_id=member_id  # Use member_id
    )
)

# ❌ Wrong way
user_id = profile.profile.id  # This won't work for Member documents!
```

### Creating Document Hierarchies

Organize documents in nested structures:

```python
from vaiz.models import CreateDocumentRequest, Kind

# 1. Create parent
parent = client.create_document(
    CreateDocumentRequest(
        kind=Kind.Project,
        kind_id=project_id,
        title="Documentation",
        index=0
    )
).payload.document

# 2. Create children
for idx, title in enumerate(["Getting Started", "API Ref", "Examples"]):
    child = client.create_document(
        CreateDocumentRequest(
            kind=Kind.Project,
            kind_id=project_id,
            title=title,
            index=idx,
            parent_document_id=parent.id  # Link to parent
        )
    ).payload.document
    
    print(f"Created: {child.title}")
```

## Real-World Scenarios

### Automated Task Creation from Issues

```python
def create_task_from_github_issue(issue_data: dict):
    """Convert GitHub issue to Vaiz task."""
    from vaiz.models import CreateTaskRequest, TaskPriority
    
    # Map priority
    priority_map = {
        "critical": TaskPriority.High,
        "high": TaskPriority.High,
        "medium": TaskPriority.Medium,
        "low": TaskPriority.Low
    }
    
    priority = priority_map.get(
        issue_data.get("priority", "medium"),
        TaskPriority.General
    )
    
    # Create task
    task = CreateTaskRequest(
        name=issue_data["title"],
        board=board_id,
        group=group_id,
        project=project_id,
        priority=priority,
        description=f"""
# GitHub Issue #{issue_data['number']}

**Author**: {issue_data['author']}
**URL**: {issue_data['url']}

## Description
{issue_data['body']}
"""
    )
    
    response = client.create_task(task)
    return response.task

# Usage
task = create_task_from_github_issue({
    "number": 123,
    "title": "Fix login bug",
    "author": "john_doe",
    "url": "https://github.com/org/repo/issues/123",
    "body": "Users can't login with email",
    "priority": "high"
})
```

### Daily Standup Report Generator

```python
from vaiz.models import GetTasksRequest
from datetime import datetime, timedelta

def generate_standup_report(client, user_id: str):
    """Generate daily standup report for a user."""
    
    # Get user's tasks
    response = client.get_tasks(
        GetTasksRequest(
            assignees=[user_id],
            completed=False
        )
    )
    
    # Categorize by due date
    today = datetime.now().date()
    overdue = []
    due_today = []
    upcoming = []
    
    for task in response.payload.tasks:
        if task.due_end:
            due_date = task.due_end.date()
            if due_date < today:
                overdue.append(task)
            elif due_date == today:
                due_today.append(task)
            else:
                upcoming.append(task)
    
    # Generate report
    report = f"""
# Standup Report - {today.strftime("%Y-%m-%d")}

## 🔴 Overdue ({len(overdue)})
{chr(10).join(f"- {t.name} (due: {t.due_end.strftime('%Y-%m-%d')})" for t in overdue)}

## ⚡ Due Today ({len(due_today)})
{chr(10).join(f"- {t.name}" for t in due_today)}

## 📋 Upcoming ({len(upcoming[:5])})
{chr(10).join(f"- {t.name} (due: {t.due_end.strftime('%Y-%m-%d')})" for t in upcoming[:5])}
"""
    
    return report

# Usage
report = generate_standup_report(client, user_id)
print(report)
```

### Project Knowledge Base Builder

```python
from vaiz.models import CreateDocumentRequest, Kind

def create_project_wiki(client, project_id: str):
    """Create a structured knowledge base for a project."""
    
    # Create wiki root
    wiki = client.create_document(
        CreateDocumentRequest(
            kind=Kind.Project,
            kind_id=project_id,
            title="Project Wiki",
            index=0
        )
    ).payload.document
    
    # Define wiki structure
    sections = {
        "Getting Started": ["Setup", "Configuration", "First Steps"],
        "Development": ["Coding Standards", "Git Workflow", "Testing"],
        "Deployment": ["Environments", "CI/CD", "Monitoring"],
        "Team": ["Contacts", "Roles", "Meetings"]
    }
    
    # Create sections and pages
    for section_idx, (section_name, pages) in enumerate(sections.items()):
        # Create section
        section = client.create_document(
            CreateDocumentRequest(
                kind=Kind.Project,
                kind_id=project_id,
                title=section_name,
                index=section_idx,
                parent_document_id=wiki.id
            )
        ).payload.document
        
        # Create pages
        for page_idx, page_name in enumerate(pages):
            page = client.create_document(
                CreateDocumentRequest(
                    kind=Kind.Project,
                    kind_id=project_id,
                    title=page_name,
                    index=page_idx,
                    parent_document_id=section.id
                )
            ).payload.document
            
            # Add initial content
            content = f"# {page_name}\n\n[Add content here]"
            client.replace_document(page.id, content)
    
    return wiki

# Usage
wiki = create_project_wiki(client, project_id)
print(f"✅ Created wiki: {wiki.id}")
```

## Performance Tips

### Batch Operations Wisely

```python
# ✅ Good - Batch related operations
documents_to_create = [
    "Requirements", "Design Spec", "Test Plan", "Deployment Guide"
]

created = []
for idx, title in enumerate(documents_to_create):
    doc = client.create_document(
        CreateDocumentRequest(
            kind=Kind.Project,
            kind_id=project_id,
            title=title,
            index=idx
        )
    ).payload.document
    created.append(doc)

# ❌ Bad - Making unnecessary API calls in loops
for task in tasks:
    # Don't fetch profile in every iteration!
    profile = client.get_profile()
    # ... use profile
```

### Minimize API Calls

```python
# ✅ Good - Fetch once, use many times
projects = client.get_projects()
project_map = {p.id: p for p in projects.projects}

# Use cached data
for task in tasks:
    project = project_map.get(task.project)
    print(f"{task.name} - {project.name if project else 'Unknown'}")

# ❌ Bad - Fetching same data repeatedly
for task in tasks:
    project = client.get_project(task.project)  # Repeated API calls!
    print(f"{task.name} - {project.project.name}")
```

### Use Task Cache Effectively

```python
from vaiz.models import GetTasksRequest

# Cache is automatic for identical requests
request = GetTasksRequest(project=project_id, completed=False)

# First call - hits API (slow)
tasks1 = client.get_tasks(request)

# Within 5 minutes - uses cache (fast)
tasks2 = client.get_tasks(request)

# Different request - hits API again
tasks3 = client.get_tasks(GetTasksRequest(project=project_id, completed=True))
```

## Integration Patterns

### Webhook Handler for Task Updates

```python
from flask import Flask, request, jsonify
from vaiz import VaizClient
from vaiz.models import EditTaskRequest

app = Flask(__name__)
client = VaizClient(api_key="...", space_id="...")

@app.route('/webhook/task-update', methods=['POST'])
def handle_task_update():
    """Handle external webhook and update Vaiz task."""
    data = request.json
    
    # Update task based on webhook
    edit = EditTaskRequest(
        task_id=data['task_id'],
        completed=data.get('status') == 'done',
        description=f"Updated via webhook at {datetime.now()}"
    )
    
    response = client.edit_task(edit)
    return jsonify({"success": True, "task": response.task.hrid})
```

### Sync Tasks with External System

```python
from vaiz.models import GetTasksRequest, EditTaskRequest

def sync_task_status_to_external(client, project_id: str):
    """Sync task statuses to external tracking system."""
    
    # Get all tasks
    tasks = client.get_tasks(
        GetTasksRequest(project=project_id, limit=50)
    ).payload.tasks
    
    # Prepare batch update for external system
    updates = []
    for task in tasks:
        updates.append({
            'external_id': task.hrid,
            'status': 'completed' if task.completed else 'active',
            'assignees': task.assignees,
            'updated_at': task.updated_at.isoformat()
        })
    
    # Send to external system (pseudocode)
    # external_api.batch_update(updates)
    
    print(f"✅ Synced {len(updates)} tasks")
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
file = safe_upload("large_file.pdf", UploadFileType.Pdf)
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

## Ready-to-Run Examples

The SDK includes complete, runnable examples in the `/examples` directory:

### Task Management
- `create_task.py` - Basic task creation
- `edit_task.py` - Update existing tasks  
- `get_tasks.py` - Query and filter tasks
- `create_task_with_files.py` - Tasks with file attachments

### Documents
- `get_documents.py` - List documents by scope
- `create_document.py` - Create documents
- `document_hierarchy.py` - Build nested document structures
- `document_content_management.py` - Work with document content
- `advanced_document_workflows.py` - Complex scenarios

### Custom Fields
- `create_board_custom_field.py` - Add custom fields to boards
- `custom_field_helpers_usage.py` - Using helper functions
- `advanced_custom_field_management.py` - Complex workflows

### Files & Comments
- `upload_file.py` - Upload files from disk
- `upload_file_from_url.py` - Download and upload from URL
- `post_comment.py` - Add comments to documents
- `comment_files.py` - Comments with file attachments

### Milestones & Boards
- `create_milestone.py` - Create milestones
- `toggle_milestone.py` - Attach milestones to tasks
- `create_board_type.py` - Create board types
- `create_board_group.py` - Create board groups

[View all examples on GitHub →](https://github.com/vaizcom/vaiz-python-sdk/tree/main/examples)

## See Also

- [API Overview](./api/overview) - Complete API documentation
- [Tasks Guide](./api/tasks) - Task management
- [Documents Guide](./api/documents) - Document management
- [Helper Functions](./api/helpers) - Utility functions

