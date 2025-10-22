---
sidebar_position: 1
---

# Introduction

Welcome to the **Vaiz Python SDK** documentation! 🎉

The Vaiz SDK is the official Python library for interacting with the Vaiz platform API. It provides a convenient, fully-typed interface to all platform features.

## Key Features

### ✨ Fully Typed

The SDK uses **Pydantic v2** for automatic data validation and complete type support:

```python
from vaiz import VaizClient
from vaiz.models import CreateTaskRequest, TaskPriority

client = VaizClient(api_key="your_api_key", space_id="your_space_id")

# Full IDE autocomplete support
task = CreateTaskRequest(
    name="My Task",
    board="board_id",
    group="group_id",
    priority=TaskPriority.High  # Enum for priorities
)
```

### 📅 Automatic DateTime Handling

All date fields automatically convert between ISO strings and Python `datetime` objects:

```python
from datetime import datetime

task = CreateTaskRequest(
    name="Task with Deadline",
    due_start=datetime(2025, 2, 1, 9, 0, 0),
    due_end=datetime(2025, 2, 15, 17, 0, 0)
)

# SDK automatically converts datetime to ISO strings for API
response = client.create_task(task)

# And back - ISO strings from API to datetime objects
print(response.task.created_at)  # datetime object
print(response.task.due_end.year)  # 2025
```

### 🎨 Enums for Icons and Colors

The SDK provides enums for all valid values:

```python
from vaiz.models.enums import Icon, Color

# Use enums instead of strings
icon = Icon.Cursor
color = Color.Blue
```

### 🎛️ Custom Field Helpers

Powerful helper functions for working with custom fields:

```python
from vaiz import make_text_field, make_select_field, make_select_option

# Create text field
text_field = make_text_field(
    name="Customer Name",
    board_id="board_id",
    description="Customer name for this project"
)

# Create select field with options
priority_options = [
    make_select_option("🔥 Critical", Color.Red, Icon.Fire),
    make_select_option("⚡ High", Color.Orange, Icon.Flag),
    make_select_option("📋 Medium", Color.Blue, Icon.Circle)
]

select_field = make_select_field(
    name="Priority Level",
    board_id="board_id",
    options=priority_options
)
```

### 📁 File Handling

Upload files from local disk or URL:

```python
from vaiz.models.enums import UploadFileType

# Upload local file
response = client.upload_file("/path/to/file.pdf", file_type=UploadFileType.Pdf)

# Upload from URL
response = client.upload_file_from_url("https://example.com/image.png")

# Attach to task
task = CreateTaskRequest(
    name="Task with Files",
    files=[TaskFile(...)]
)
```

### 💬 Full Comment Support

Create, edit, delete comments with files and reactions:

```python
# Create comment with HTML formatting
response = client.post_comment(
    document_id="document_id",
    content="<p>Comment with <strong>bold</strong> text</p>",
    file_ids=["file1", "file2"]
)

# Add reaction
client.add_reaction(
    comment_id=response.comment.id,
    reaction=CommentReactionType.THUMBS_UP
)
```

## What's Next?

- 🚀 [Getting Started](/) - Install the SDK and create your first task
- 📖 [API Reference](./api-reference/overview) - Complete reference of methods, models, and enums
- 📚 [Guides](./guides/basics) - Detailed guides for each API category
- 💡 [Examples](./patterns/introduction) - Ready-to-use code examples
- ⚡ [Common Patterns](./patterns/common-patterns) - Best practices and type-safe patterns

## Requirements

- Python 3.8 or higher
- `requests` >= 2.31.0
- `pydantic` >= 2.0
- `python-dotenv` >= 0.9.0

## License

This project is licensed under the MIT License.

