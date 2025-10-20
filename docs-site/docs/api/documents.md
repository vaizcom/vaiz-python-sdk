---
sidebar_position: 9
---

# Documents

Manage task descriptions and rich content.

## Get Document Content

Documents store task descriptions as structured JSON:

```python
# Get from task
task_response = client.get_task("PRJ-123")
document_id = task_response.payload["task"]["document"]

# Get document content
doc = client.get_document_body(document_id)
print(doc)  # JSON structure
```

## Replace Document Content

Update task descriptions by replacing the entire document:

```python
document_id = "document_id"

new_content = """
# Updated Description

This completely replaces the previous content.

## Features
- Complete replacement
- Plain text support
- Direct API access

## Notes
Use this for programmatic updates.
"""

client.replace_document(
    document_id=document_id,
    description=new_content
)
```

## Using Task Helper Methods

The SDK provides convenient helper methods on Task objects:

### Get Task Description

```python
from vaiz.models import CreateTaskRequest

# Create task
task = CreateTaskRequest(
    name="Task with Description",
    board="board_id",
    group="group_id"
)
response = client.create_task(task)

# Get description using helper
task_obj = response.task
description = task_obj.get_task_description(client)
print(description)
```

### Update Task Description

```python
# Update description using helper
task_obj.update_task_description(
    client, 
    "New task description content"
)
```

## Working with Task Documents

### Full Workflow Example

```python
# 1. Create task
from vaiz.models import CreateTaskRequest

task = CreateTaskRequest(
    name="Documentation Task",
    board="board_id",
    group="group_id"
)
response = client.create_task(task)

# 2. Get document ID
document_id = response.task.document

# 3. Add initial description
client.replace_document(
    document_id=document_id,
    description="Initial task description"
)

# 4. Later, update it
client.replace_document(
    document_id=document_id,
    description="Updated task description with more details"
)

# 5. Read current content
content = client.get_document_body(document_id)
print(content)
```

### Programmatic Description Updates

```python
def update_task_description(task_id: str, new_description: str):
    """Update task description programmatically"""
    # Get task
    task_response = client.get_task(task_id)
    document_id = task_response.payload["task"]["document"]
    
    # Update description
    client.replace_document(
        document_id=document_id,
        description=new_description
    )
    
    print(f"✅ Updated description for {task_id}")

# Usage
update_task_description(
    "PRJ-123",
    "New automated description"
)
```

## Document Format

Documents are stored as JSON structures. When you use `replace_document`, the content is converted to the appropriate format:

```python
# Plain text input
client.replace_document(
    document_id="doc_id",
    description="Simple text description"
)

# Markdown-style input
client.replace_document(
    document_id="doc_id",
    description="""
# Header
## Subheader

- List item 1
- List item 2

**Bold text** and *italic text*
"""
)
```

## Use Cases

### Automated Status Updates

```python
def add_status_update(task_id: str, status: str):
    """Append status update to task description"""
    from datetime import datetime
    
    task = client.get_task(task_id)
    doc_id = task.payload["task"]["document"]
    
    # Get current content
    current = client.get_document_body(doc_id)
    
    # Add status update
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    new_content = f"""
{current}

---
**Status Update ({timestamp})**: {status}
"""
    
    client.replace_document(doc_id, new_content)
```

### Template-Based Descriptions

```python
def create_task_from_template(name: str, template: dict):
    """Create task with templated description"""
    task = CreateTaskRequest(
        name=name,
        board=template["board_id"],
        group=template["group_id"]
    )
    response = client.create_task(task)
    
    # Apply template description
    description = template["description_template"].format(
        task_name=name,
        created_date=datetime.now().strftime("%Y-%m-%d")
    )
    
    client.replace_document(
        response.task.document,
        description
    )
    
    return response.task
```

## See Also

- [Tasks API](./tasks) - Task operations
- [Comments](./comments) - Add comments to tasks

