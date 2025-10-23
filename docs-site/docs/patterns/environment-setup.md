---
sidebar_position: 2
sidebar_label: Environment Setup
title: Environment Setup — Configuration & Best Practices | Vaiz Python SDK
description: Learn how to configure your development environment for the Vaiz Python SDK. Includes environment variables, credentials, and security best practices.
---

# Environment Setup

Configure your development environment for the Vaiz SDK.

## Using Environment Variables

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

## Type Hints for Better IDE Support

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

## Best Practices

### ✅ Do's

- Use environment variables for all credentials
- Add type hints to your functions
- Use `.env` files for local development
- Keep `.env` files out of version control (add to `.gitignore`)

### ❌ Don'ts

- Never hardcode API keys in your code
- Don't commit `.env` files to Git
- Avoid storing credentials in plain text files

