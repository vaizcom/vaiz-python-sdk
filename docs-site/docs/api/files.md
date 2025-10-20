---
sidebar_position: 4
---

# Working with Files

Files in Vaiz are always attached to either [tasks](./tasks) or [comments](./comments). You upload files and then attach them to content.

## File Types

Choose the right type for proper display:

```python
from vaiz.models.enums import EUploadFileType

EUploadFileType.Image    # Shows preview thumbnail
EUploadFileType.Video    # Shows embedded player
EUploadFileType.Pdf      # Shows document viewer
EUploadFileType.File     # Shows download link
```

:::tip File Type Matters
The same file uploaded as `Image` shows a preview, while `File` shows only a download button. Choose based on how you want users to see it.
:::

## Files in Tasks

Upload and attach files when creating or updating tasks:

```python
from vaiz.models import CreateTaskRequest, TaskFile
from vaiz.models.enums import EUploadFileType

# 1. Upload file
upload = client.upload_file("design.pdf", EUploadFileType.Pdf)

# 2. Create TaskFile object
task_file = TaskFile(
    url=upload.file.url,
    name=upload.file.name,
    ext=upload.file.ext,
    _id=upload.file.id,
    type=upload.file.type,
    dimension=upload.file.dimension
)

# 3. Create task with file
task = CreateTaskRequest(
    name="Review Design Document",
    board="board_id",
    group="group_id",
    files=[task_file]
)

response = client.create_task(task)
```

### Multiple Files in Task

```python
from vaiz.models.enums import EUploadFileType

# Upload multiple files
files = [
    ("requirements.pdf", EUploadFileType.Pdf),
    ("mockup.png", EUploadFileType.Image),
    ("demo.mp4", EUploadFileType.Video)
]

task_files = []
for path, file_type in files:
    upload = client.upload_file(path, file_type)
    task_files.append(TaskFile(
        url=upload.file.url,
        name=upload.file.name,
        ext=upload.file.ext,
        _id=upload.file.id,
        type=upload.file.type,
        dimension=upload.file.dimension
    ))

# Create task with all files
task = CreateTaskRequest(
    name="Project Kickoff",
    board="board_id",
    group="group_id",
    files=task_files
)

response = client.create_task(task)
```

## Files in Comments

Files are commonly used in comments for discussions:

```python
from vaiz.models.enums import EUploadFileType

# Upload files
screenshot = client.upload_file("bug.png", EUploadFileType.Image)
log = client.upload_file("error.log", EUploadFileType.File)

# Attach to comment
response = client.post_comment(
    document_id="document_id",
    content="<p>Found a bug, see screenshot and logs</p>",
    file_ids=[screenshot.file.id, log.file.id]
)
```

### Upload from URL

Skip local files and upload directly from URLs:

```python
# Upload external file
upload = client.upload_file_from_url(
    file_url="https://example.com/report.pdf",
    file_type=EUploadFileType.Pdf,
    filename="monthly_report.pdf"
)

# Use in comment
response = client.post_comment(
    document_id="document_id",
    content="<p>External report attached</p>",
    file_ids=[upload.file.id]
)
```

## See Also

- [Tasks API](./tasks)
- [Comments API](./comments)
- [Examples](../examples)

