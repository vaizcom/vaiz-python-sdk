---
sidebar_position: 8
---

# Error Handling

Robust error handling strategies for production applications.

## Robust File Upload

Handle file upload errors gracefully:

```python
import os
from vaiz.api.base import VaizSDKError
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
        
    except VaizSDKError as e:
        print(f"❌ SDK Error: {e}")
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
from vaiz.api.base import VaizSDKError

def create_task_with_retry(task_request, max_retries=3):
    """Create task with automatic retry on failure"""
    for attempt in range(max_retries):
        try:
            response = client.create_task(task_request)
            print(f"✅ Task created: {response.task.id}")
            return response
            
        except VaizSDKError as e:
            # Retry on SDK errors (can check specific error types if needed)
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff
                print(f"⚠️ Error, retrying in {wait_time}s...")
                time.sleep(wait_time)
            else:
                raise
    
    raise Exception("Max retries exceeded")
```

## Comprehensive Error Handling

Handle all common error scenarios:

```python
from pydantic import ValidationError
from vaiz.api.base import (
    VaizSDKError,
    VaizAuthError,
    VaizValidationError,
    VaizNotFoundError,
    VaizPermissionError,
    VaizRateLimitError
)
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
        
    except VaizAuthError as e:
        print(f"❌ Authentication failed: {e}")
        return {"success": False, "error": "Authentication error"}
        
    except VaizValidationError as e:
        print(f"❌ Validation error from API: {e}")
        return {"success": False, "error": "Invalid request"}
        
    except VaizPermissionError as e:
        print(f"❌ Permission denied: {e}")
        return {"success": False, "error": "Permission denied"}
        
    except VaizNotFoundError as e:
        print(f"❌ Resource not found: {e}")
        return {"success": False, "error": "Not found"}
        
    except VaizRateLimitError as e:
        print(f"❌ Rate limit exceeded: {e}")
        return {"success": False, "error": "Rate limit exceeded"}
        
    except VaizSDKError as e:
        # Catch-all for other SDK errors
        print(f"❌ SDK Error: {e}")
        return {"success": False, "error": "SDK error"}
        
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
from vaiz.api.base import VaizSDKError

try:
    response = client.create_task(task)
    return response.task
except VaizSDKError as e:
    logger.error(f"Failed to create task: {e}")
    return None

# ❌ Bad - No error handling
response = client.create_task(task)  # Can crash
return response.task
```

### Log Errors Properly

```python
import logging
from vaiz.api.base import VaizSDKError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_task_with_logging(task_request):
    """Create task with proper logging."""
    try:
        response = client.create_task(task_request)
        logger.info(f"Task created: {response.task.hrid}")
        return response
    except VaizSDKError as e:
        logger.error(
            f"Failed to create task: {e}",
            extra={"task_name": task_request.name}
        )
        raise
```

## See Also

- [Performance Tips](./performance) - Optimize SDK usage
- [Integration Patterns](./integrations) - External system integration

