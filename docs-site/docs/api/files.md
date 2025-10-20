---
sidebar_position: 4
---

# Files API

Upload and manage files in Vaiz SDK.

## Uploading Files

### From Local Disk

```python
from vaiz.models.enums import EUploadFileType

response = client.upload_file(
    "/path/to/file.pdf",
    file_type=EUploadFileType.Pdf
)

file = response.file
print(f"Uploaded: {file.name}")
print(f"URL: {file.url}")
```

### From URL

```python
response = client.upload_file_from_url(
    "https://example.com/image.png"
)

# With custom name
response = client.upload_file_from_url(
    file_url="https://example.com/doc.pdf",
    file_type=EUploadFileType.Pdf,
    filename="custom_name.pdf"
)
```

## File Types

### EUploadFileType Options

```python
EUploadFileType.Image    # Images - shows preview
EUploadFileType.Video    # Videos - shows player
EUploadFileType.Pdf      # PDFs - shows viewer
EUploadFileType.File     # Generic files - download link
```

### Display Differences

```python
# Image - preview thumbnail
img = client.upload_file("photo.jpg", EUploadFileType.Image)

# Video - embedded player
vid = client.upload_file("demo.mp4", EUploadFileType.Video)

# PDF - document viewer
pdf = client.upload_file("doc.pdf", EUploadFileType.Pdf)

# File - download button
file = client.upload_file("archive.zip", EUploadFileType.File)
```

## Attaching to Tasks

```python
from vaiz.models import CreateTaskRequest, TaskFile

# Upload file
upload = client.upload_file("doc.pdf", EUploadFileType.Pdf)

# Create TaskFile
task_file = TaskFile(
    url=upload.file.url,
    name=upload.file.name,
    ext=upload.file.ext,
    _id=upload.file.id,
    type=upload.file.type,
    dimension=upload.file.dimension
)

# Create task
task = CreateTaskRequest(
    name="Task with File",
    board="board_id",
    group="group_id",
    files=[task_file]
)

response = client.create_task(task)
```

## Multiple Files

```python
files_to_upload = [
    ("doc.pdf", EUploadFileType.Pdf),
    ("image.png", EUploadFileType.Image),
    ("video.mp4", EUploadFileType.Video)
]

task_files = []
for path, file_type in files_to_upload:
    upload = client.upload_file(path, file_type)
    
    task_file = TaskFile(
        url=upload.file.url,
        name=upload.file.name,
        ext=upload.file.ext,
        _id=upload.file.id,
        type=upload.file.type,
        dimension=upload.file.dimension
    )
    task_files.append(task_file)

# Create task with all files
task = CreateTaskRequest(
    name="Multi-file Task",
    board="board_id",
    group="group_id",
    files=task_files
)
```

## Files in Comments

```python
# Upload files
file1 = client.upload_file("report.pdf", EUploadFileType.Pdf)
file2 = client.upload_file("chart.png", EUploadFileType.Image)

# Add to comment
response = client.post_comment(
    document_id="document_id",
    content="<p>See attachments</p>",
    file_ids=[file1.file.id, file2.file.id]
)
```

## Response Model

### UploadedFile

```python
class UploadedFile:
    id: str                    # File ID
    url: str                   # Access URL
    name: str                  # Filename
    original_name: str         # Original name
    size: int                  # Size in bytes
    type: EUploadFileType      # File type
    ext: str                   # Extension
    dimension: Optional[dict]  # Dimensions (images/videos)
```

## Error Handling

```python
import os
from requests.exceptions import HTTPError

try:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    response = client.upload_file(file_path, file_type)
    print(f"✅ Uploaded: {response.file.name}")
    
except HTTPError as e:
    print(f"❌ HTTP Error: {e.response.status_code}")
except Exception as e:
    print(f"❌ Error: {e}")
```

## See Also

- [Tasks API](./tasks)
- [Comments API](./comments)
- [Examples](../examples)

