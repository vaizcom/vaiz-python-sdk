---
sidebar_position: 5
---

# Contributing

Thank you for your interest in contributing to the Vaiz Python SDK! 🎉

## Development Setup

### 1. Clone the Repository

```bash
git clone https://github.com/vaizcom/vaiz-python-sdk.git
cd vaiz-python-sdk
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install in Development Mode

```bash
pip install -e .
pip install pytest pytest-mock python-dotenv
```

### 4. Configure Environment

Create a `.env` file with your test credentials:

```env
VAIZ_API_KEY=your_test_api_key
VAIZ_SPACE_ID=your_test_space_id
```

## Running Tests

### All Tests

```bash
PYTHONPATH=. pytest
```

### Specific Test File

```bash
PYTHONPATH=. pytest tests/test_tasks.py
```

### With Verbose Output

```bash
PYTHONPATH=. pytest -v
```

:::note
Tests run against a real API instance. Make sure your `.env` file contains valid credentials for a test workspace.
:::

## Code Style

### Type Hints

Always use type hints for better IDE support:

```python
from typing import List, Optional
from vaiz.models import Task

def get_tasks(completed: bool = False) -> List[Task]:
    """Get tasks with completion filter"""
    pass
```

### Pydantic Models

Use Pydantic v2 for all data models:

```python
from pydantic import BaseModel, Field
from typing import Optional

class MyModel(BaseModel):
    name: str = Field(..., description="Name field")
    value: Optional[int] = None
    
    class Config:
        populate_by_name = True
```

### Field Aliases

Use `alias` and `serialization_alias` for API field mapping:

```python
from pydantic import Field

class TaskModel(BaseModel):
    due_end: Optional[datetime] = Field(
        None,
        alias="dueEnd",
        serialization_alias="dueEnd"
    )
```

## Adding New Features

### 1. API Method

Add the method to the appropriate API class in `vaiz/api/`:

```python
# vaiz/api/tasks.py

def create_task(self, request: CreateTaskRequest) -> CreateTaskResponse:
    """
    Create a new task.
    
    Args:
        request: Task creation request
        
    Returns:
        CreateTaskResponse with created task
    """
    data = request.model_dump(by_alias=True, exclude_none=True)
    response = self._post("/api/tasks", data)
    return CreateTaskResponse(**response)
```

### 2. Request Model

Add request model to `vaiz/models/`:

```python
# vaiz/models/tasks.py

class CreateTaskRequest(BaseModel):
    """Request model for creating a task"""
    
    name: str = Field(..., description="Task name")
    board: str = Field(..., alias="board", serialization_alias="board")
    group: str = Field(..., alias="group", serialization_alias="group")
    
    class Config:
        populate_by_name = True
```

### 3. Response Model

```python
class CreateTaskResponse(BaseModel):
    """Response model for task creation"""
    
    task: Task
```

### 4. Tests

Add tests in `tests/`:

```python
# tests/test_new_feature.py

from tests.test_config import get_test_client

def test_create_task():
    client = get_test_client()
    
    task = CreateTaskRequest(
        name="Test Task",
        board="board_id",
        group="group_id"
    )
    
    response = client.create_task(task)
    
    assert response.task.id is not None
    assert response.task.name == "Test Task"
```

### 5. Documentation

Update the documentation in `docs-site/docs/`:

```markdown
## New Feature

Description of the new feature.

### Example

\`\`\`python
# Usage example
result = client.new_feature()
\`\`\`
```

### 6. Examples

Add practical example to `examples/`:

```python
# examples/new_feature_example.py

from vaiz import VaizClient
from examples.config import get_client

def main():
    client = get_client()
    
    # Demonstrate the new feature
    result = client.new_feature()
    print(f"Result: {result}")

if __name__ == "__main__":
    main()
```

## Pull Request Process

### 1. Create a Branch

```bash
git checkout -b feature/my-new-feature
```

### 2. Make Changes

- Write code
- Add tests
- Update documentation

### 3. Run Tests

```bash
PYTHONPATH=. pytest
```

### 4. Commit Changes

```bash
git add .
git commit -m "Add new feature: description"
```

Use clear, descriptive commit messages:

- ✅ `Add support for task templates`
- ✅ `Fix datetime serialization in milestones`
- ✅ `Update documentation for custom fields`
- ❌ `Update`
- ❌ `Fix bug`

### 5. Push and Create PR

```bash
git push origin feature/my-new-feature
```

Then create a Pull Request on GitHub with:

- Clear description of changes
- Link to related issues
- Test results
- Screenshots (if UI changes)

## Code Review

All PRs require:

1. ✅ Passing tests
2. ✅ Type hints
3. ✅ Documentation updates
4. ✅ Example code (for new features)
5. ✅ Clear commit messages

## Project Structure

```
vaiz-python-sdk/
├── vaiz/                    # Main package
│   ├── __init__.py
│   ├── client.py           # Main client class
│   ├── api/                # API method implementations
│   │   ├── base.py
│   │   ├── tasks.py
│   │   ├── comments.py
│   │   └── ...
│   ├── models/             # Pydantic models
│   │   ├── tasks.py
│   │   ├── comments.py
│   │   ├── enums.py
│   │   └── ...
│   └── helpers/            # Helper functions
│       └── custom_fields.py
├── tests/                  # Test files
│   ├── test_config.py
│   ├── test_tasks.py
│   └── ...
├── examples/               # Usage examples
│   ├── config.py
│   ├── create_task.py
│   └── ...
├── docs-site/             # Docusaurus documentation
│   └── docs/
└── README.md
```

## Release Process

1. Update version in `pyproject.toml`
2. Update `CHANGELOG.md`
3. Create git tag
4. Build package: `python -m build`
5. Upload to PyPI: `twine upload dist/*`

## Getting Help

- 💬 [GitHub Discussions](https://github.com/vaizcom/vaiz-python-sdk/discussions)
- 🐛 [Issue Tracker](https://github.com/vaizcom/vaiz-python-sdk/issues)
- 📧 Email: support@vaiz.com

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

