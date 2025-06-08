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

## Development

### Project Structure

```
vaiz-python-sdk/
├── vaiz/                  # Main package directory
│   ├── __init__.py       # Package initialization
│   ├── client.py         # Main client implementation
│   └── models.py         # Data models
├── tests/                # Test directory
│   ├── __init__.py
│   ├── test_client.py    # Client tests
│   └── test_config.py    # Test configuration
├── examples/             # Example usage
│   ├── __init__.py
│   ├── config.py         # Example configuration
│   ├── create_task.py    # Task creation example
│   ├── edit_task.py      # Task editing example
│   └── get_task.py       # Task retrieval example
├── README.md             # This file
└── requirements.txt      # Project dependencies
```

### Testing

#### Setup

1. Install test dependencies:

```bash
pip install pytest pytest-mock python-dotenv
```

2. Create a `.env` file in the project root with your test credentials:

```env
VAIZ_API_KEY=your_test_api_key
VAIZ_SPACE_ID=your_test_space_id
```

The test configuration (`tests/test_config.py`) will automatically load these credentials.

#### Running Tests

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

#### Writing Tests

When writing tests for the SDK:

1. Use the test configuration from `tests/test_config.py`:

```python
from tests.test_config import get_test_client, TEST_BOARD_ID, TEST_GROUP_ID

def test_create_task(mocker):
    client = get_test_client()
    # Your test code here
```

2. Mock external API calls using `pytest-mock`:

```python
def test_create_task(mocker):
    # Mock the API response
    mock_response = mocker.Mock()
    mock_response.json.return_value = {
        "type": "success",
        "payload": {"task": {"_id": "test_task_id"}}
    }
    mocker.patch('requests.post', return_value=mock_response)

    # Test implementation
    client = get_test_client()
    # ... rest of the test
```

3. Test both success and error cases
4. Include proper assertions for response data

### Examples

The `examples/` directory contains working examples of SDK usage:

- `create_task.py`: Demonstrates task creation
- `edit_task.py`: Shows how to edit existing tasks
- `get_task.py`: Illustrates task retrieval
- `config.py`: Example configuration setup

To run an example:

```bash
python -m examples.create_task
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Write tests for your changes
4. Ensure all tests pass
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
