---
sidebar_position: 4
sidebar_label: Files
title: Files API — Upload & Manage Files | Vaiz Python SDK
description: Learn how to use the Vaiz Python SDK to upload files, manage attachments, and work with external URLs. Supports images, videos, PDFs, and more.
---

# Files

Complete reference for file upload methods and models.

## Methods

### `upload_file`

```python
upload_file(
    file_path: str,
    file_type: UploadFileType
) -> UploadFileResponse
```

Upload a file from local disk.

**Parameters:**
- `file_path` - Path to file
- `file_type` - File type (Image, Video, Pdf, File)

**Returns:** `UploadFileResponse` with uploaded file info

---

### `upload_file_from_url`

```python
upload_file_from_url(
    file_url: str,
    file_type: UploadFileType = None,
    filename: str = None
) -> UploadFileResponse
```

Upload a file from URL.

**Parameters:**
- `file_url` - URL of file to download
- `file_type` - Optional file type (auto-detected if not provided)
- `filename` - Optional custom filename

**Returns:** `UploadFileResponse` with uploaded file info

---

## Models

### UploadedFile

Main uploaded file model.

```python
class UploadedFile:
    id: str                             # File ID
    url: str                            # Access URL
    name: str                           # Filename
    original_name: str                  # Original filename
    size: int                           # Size in bytes
    type: UploadFileType               # File type
    ext: str                            # Extension
    dimension: Optional[dict]           # Dimensions (images/videos)
```

---

### TaskFile

```python
class TaskFile:
    id: str                             # File ID
    url: str                            # File URL
    name: str                           # Filename
    ext: str                            # File extension
    type: UploadFileType               # File type
    dimension: Optional[List[int]]      # Dimensions [width, height] for images/videos
    size: Optional[int]                 # File size in bytes
```

---

### TaskUploadFile

```python
class TaskUploadFile:
    path: str                           # Path to file
    type: Optional[UploadFileType]     # File type (auto-detected if not provided)
```

---

## Response Models

### UploadFileResponse

```python
class UploadFileResponse:
    type: str                           # Response type
    payload: UploadFilePayload          # Response payload
    
    @property
    def file(self) -> UploadedFile:    # Convenience property
        ...
```

---

### UploadFilePayload

```python
class UploadFilePayload:
    file: UploadedFile                 # Uploaded file object
```

---

## See Also

- [Files Guide](../guides/files) - Usage examples and patterns
- [Enums](./enums) - UploadFileType enum

