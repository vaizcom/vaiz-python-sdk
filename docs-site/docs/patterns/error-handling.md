---
sidebar_position: 8
---

# Error Handling

Robust error handling strategies for production applications.

## Robust File Upload

Handle file upload errors gracefully:

```python
import os
from requests.exceptions import HTTPError
from vaiz.models.enums import UploadFileType

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

## Retry Logic

Implement automatic retry with exponential backoff:

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

## Comprehensive Error Handling

Handle all common error scenarios:

```python
from requests.exceptions import HTTPError, ConnectionError, Timeout
from vaiz.models import CreateTaskRequest

def safe_create_task(task_data: dict):
    """Create task with comprehensive error handling."""
    try:
        task = CreateTaskRequest(**task_data)
        response = client.create_task(task)
        return {"success": True, "task": response.task}
        
    except ValidationError as e:
        # Pydantic validation error
        print(f"❌ Validation Error: {e}")
        return {"success": False, "error": "Invalid task data"}
        
    except HTTPError as e:
        # HTTP errors from API
        status = e.response.status_code
        if status == 400:
            print(f"❌ Bad Request: {e.response.json()}")
            return {"success": False, "error": "Invalid request"}
        elif status == 401:
            print("❌ Authentication failed")
            return {"success": False, "error": "Authentication error"}
        elif status == 403:
            print("❌ Permission denied")
            return {"success": False, "error": "Permission denied"}
        elif status == 404:
            print("❌ Resource not found")
            return {"success": False, "error": "Not found"}
        elif status >= 500:
            print(f"❌ Server error: {status}")
            return {"success": False, "error": "Server error"}
        else:
            print(f"❌ HTTP Error: {status}")
            return {"success": False, "error": f"HTTP {status}"}
            
    except ConnectionError:
        print("❌ Connection error - check network")
        return {"success": False, "error": "Connection error"}
        
    except Timeout:
        print("❌ Request timeout")
        return {"success": False, "error": "Timeout"}
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return {"success": False, "error": "Unexpected error"}
```

## Graceful Degradation

Continue operation even when some operations fail:

```python
def bulk_create_tasks(tasks_data: list):
    """Create multiple tasks with graceful error handling."""
    results = {
        "success": [],
        "failed": []
    }
    
    for task_data in tasks_data:
        try:
            task = CreateTaskRequest(**task_data)
            response = client.create_task(task)
            results["success"].append({
                "name": task.name,
                "hrid": response.task.hrid
            })
        except Exception as e:
            results["failed"].append({
                "name": task_data.get("name", "Unknown"),
                "error": str(e)
            })
    
    # Summary
    print(f"✅ Created: {len(results['success'])} tasks")
    print(f"❌ Failed: {len(results['failed'])} tasks")
    
    return results
```

## Best Practices

### Always Handle Errors

```python
# ✅ Good - Handle all errors
try:
    response = client.create_task(task)
    return response.task
except HTTPError as e:
    logger.error(f"Failed to create task: {e}")
    return None

# ❌ Bad - No error handling
response = client.create_task(task)  # Can crash
return response.task
```

### Log Errors Properly

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_task_with_logging(task_request):
    """Create task with proper logging."""
    try:
        response = client.create_task(task_request)
        logger.info(f"Task created: {response.task.hrid}")
        return response
    except HTTPError as e:
        logger.error(
            f"Failed to create task: {e.response.status_code}",
            extra={"task_name": task_request.name}
        )
        raise
```

## See Also

- [Performance Tips](./performance) - Optimize SDK usage
- [Integration Patterns](./integrations) - External system integration

