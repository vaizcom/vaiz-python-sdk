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

### Working with Projects

#### Get All Projects

```python
response = client.get_projects()
```

### Working with Boards

#### Get All Boards

```python
response = client.get_boards()
```

#### Get a Single Board

```python
response = client.get_board("board_id")
board = response.payload["board"]
```

#### Create a Board Type

```python
from vaiz.models import CreateBoardTypeRequest

request = CreateBoardTypeRequest(
    boardId="board_id",
    label="New Type",
    icon="Cursor",
    color="silver"
)

response = client.create_board_type(request)
board_type = response.board_type
```

#### Edit a Board Type

```python
from vaiz.models import EditBoardTypeRequest

request = EditBoardTypeRequest(
    boardTypeId="board_type_id",
    boardId="board_id",
    label="Updated Type",
    icon="Cursor",
    color="silver",
    description="Updated description",
    hidden=True
)

response = client.edit_board_type(request)
board_type = response.board_type
```

### Working with Profile

#### Get User Profile

```python
response = client.get_profile()
profile = response.payload["profile"]
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
```

## Development

### Setting Up Development Environment

1. Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

2. Install the package in development mode:

```bash
pip install -e .
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
PYTHONPATH=. pytest
```

Run specific test file:

```bash
PYTHONPATH=. pytest tests/test_client.py
```

Run with verbose output:

```bash
PYTHONPATH=. pytest -v
```

Note: Setting `PYTHONPATH=.` is required to ensure Python can find the package modules during testing.

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

The `examples/` directory contains working examples of SDK usage. You can run any example using the following command:

```bash
python -m examples.<example_file_name>
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Write tests for your changes
4. Ensure all tests pass
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
