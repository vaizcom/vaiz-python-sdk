# Vaiz SDK for Python

Python SDK for accessing the Vaiz platform.

## Installation

```bash
pip install vaiz-sdk
```

## Usage

### Basic Setup

First, you need to set up your environment variables. Create a `.env` file in your project root with the following variables:

```env
VAIZ_API_KEY=your_api_key
VAIZ_SPACE_ID=your_space_id
```

### Creating a Client

```python
from vaiz import VaizClient

client = VaizClient(
    api_key="your_api_key",
    space_id="your_space_id",
    verify_ssl=False,  # Set to True in production
    base_url="https://api.vaiz.local:10000/v4"  # Use appropriate base URL for your environment
)
```

### Working with Tasks

#### Create a Task

```python
from vaiz.models import CreateTaskRequest, TaskPriority

task = CreateTaskRequest(
    name="My Task",
    group="group_id",
    board="board_id",
    project="project_id",
    priority=TaskPriority.High,
    completed=False,
    types=["type_id"],
    subtasks=[],
    milestones=[],
    rightConnectors=[],
    leftConnectors=[]
)

response = client.create_task(task)
task_id = response.payload['task']['_id']
```

#### Edit a Task

```python
from vaiz.models import EditTaskRequest

edit_task = EditTaskRequest(
    taskId="task_id",
    name="Updated Task Name",
    assignees=["assignee_id"]
)

response = client.edit_task(edit_task)
```

#### Get Task Information

```python
response = client.get_task("task_id")
task_data = response.payload
```

## Testing

### Setup

1. Install test dependencies:

```bash
pip install pytest pytest-mock
```

2. Create a test configuration file (e.g., `test_config.py`) with your test credentials:

```python
TEST_API_KEY = "your_test_api_key"
TEST_SPACE_ID = "your_test_space_id"
TEST_BOARD_ID = "your_test_board_id"
TEST_GROUP_ID = "your_test_group_id"
TEST_PROJECT_ID = "your_test_project_id"
TEST_ASSIGNEE_ID = "your_test_assignee_id"
```

### Running Tests

Run all tests:

```bash
pytest
```

Run specific test file:

```bash
pytest tests/test_client.py
```

Run with verbose output:

```bash
pytest -v
```

### Writing Tests

When writing tests for the SDK:

1. Use pytest fixtures for common setup
2. Mock external API calls using `pytest-mock`
3. Test both success and error cases
4. Include proper assertions for response data

Example test structure:

```python
import pytest
from vaiz import VaizClient
from vaiz.models import CreateTaskRequest

def test_create_task(mocker):
    # Mock the API response
    mock_response = mocker.Mock()
    mock_response.json.return_value = {
        "type": "success",
        "payload": {"task": {"_id": "test_task_id"}}
    }
    mocker.patch('requests.post', return_value=mock_response)

    # Create client and test
    client = VaizClient(api_key="test_key", space_id="test_space")
    task = CreateTaskRequest(name="Test Task")
    response = client.create_task(task)

    assert response.type == "success"
    assert response.payload["task"]["_id"] == "test_task_id"
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Write tests for your changes
4. Ensure all tests pass
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
