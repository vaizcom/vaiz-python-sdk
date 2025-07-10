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

# For production use (verify_ssl=True by default)
client = VaizClient(
    api_key="your_api_key",
    space_id="your_space_id"
    # verify_ssl=True is the default value
    # verbose=True  # Optional: set to True to enable debug output (request/response)
)

# For local development (when using self-signed certificates)
client = VaizClient(
    api_key="your_api_key",
    space_id="your_space_id",
    verify_ssl=False,  # Only for local development
    base_url="https://api.vaiz.local:10000/v4"  # Local development URL
)
```

### Enums

The SDK provides enums for icons and colors to ensure you are using valid values.

#### `EIcon`

```python
from vaiz.models.enums import EIcon

# Example usage
icon = EIcon.Cursor
```

#### `EColor`

```python
from vaiz.models.enums import EColor

# Example usage
color = EColor.Silver
```

### Working with Projects

#### Get All Projects

```python
response = client.get_projects()
```

### Working with Milestones

#### Get All Milestones

```python
response = client.get_milestones()
milestones = response.milestones

for milestone in milestones:
    print(f"Milestone: {milestone.name}")
    print(f"Progress: {milestone.completed}/{milestone.total}")
    print(f"Due Date: {milestone.due_end}")
```

#### Get a Single Milestone

```python
milestone_id = "your_milestone_id"
response = client.get_milestone(milestone_id)
milestone = response.milestone

print(f"Milestone: {milestone.name}")
print(f"Description: {milestone.description}")
print(f"Progress: {milestone.completed}/{milestone.total}")
print(f"Due Date: {milestone.due_end}")
print(f"Created by: {milestone.creator}")
print(f"Last edited by: {milestone.editor}")
```

#### Create a Milestone

```python
from vaiz.models import CreateMilestoneRequest

milestone = CreateMilestoneRequest(
    name="New Milestone",
    board="board_id",
    project="project_id"
)

response = client.create_milestone(milestone)
created_milestone = response.milestone
print(f"Created milestone: {created_milestone.name}")
print(f"Milestone ID: {created_milestone.id}")
```

**Note**: When creating a milestone, you can only set the name, board, and project. Additional fields like description and due dates should be set using the edit milestone method.

#### Edit a Milestone

```python
from vaiz.models import EditMilestoneRequest

# Edit an existing milestone
edit_request = EditMilestoneRequest(
    id="milestone_id",
    name="Updated Milestone Name",  # Optional
    description="Updated description",  # Optional
    due_start=None,  # Optional
    due_end="2025-12-31T23:59:59.999Z"  # Optional
)

response = client.edit_milestone(edit_request)
updated_milestone = response.milestone
print(f"Updated milestone: {updated_milestone.name}")
print(f"Description: {updated_milestone.description}")
print(f"Due date: {updated_milestone.due_end}")
print(f"Last edited by: {updated_milestone.editor}")
```

**Note**: All fields except `id` are optional in EditMilestoneRequest. Only provide the fields you want to update.

#### Toggle Milestone Assignment

```python
from vaiz.models import ToggleMilestoneRequest

# Attach/detach milestones to/from a task
toggle_request = ToggleMilestoneRequest(
    task_id="your_task_id",
    milestone_ids=["milestone_id_1", "milestone_id_2"]  # Can toggle multiple milestones at once
)

response = client.toggle_milestone(toggle_request)
updated_task = response.task

print(f"Task: {updated_task.name}")
print(f"Current milestones: {updated_task.milestones}")
print(f"Main milestone: {updated_task.milestone}")

# Check if milestone was attached or detached
if "milestone_id_1" in updated_task.milestones:
    print("✅ Milestone was attached to the task")
else:
    print("❌ Milestone was detached from the task")
```

**Note**: The `toggle_milestone` method works as a toggle - if the milestone is already assigned to the task, it will be removed; if not assigned, it will be added.

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
from vaiz.models.enums import EIcon, EColor

request = CreateBoardTypeRequest(
    boardId="board_id",
    label="New Type",
    icon=EIcon.Cursor,
    color=EColor.Silver
)

response = client.create_board_type(request)
board_type = response.board_type
```

#### Edit a Board Type

```python
from vaiz.models import EditBoardTypeRequest
from vaiz.models.enums import EIcon, EColor

request = EditBoardTypeRequest(
    boardTypeId="board_type_id",
    boardId="board_id",
    label="Updated Type",
    icon=EIcon.Cursor,
    color=EColor.Silver,
    description="Updated description",
    hidden=True
)

response = client.edit_board_type(request)
board_type = response.board_type
```

#### Create a Board Custom Field

```python
from vaiz import VaizClient, CreateBoardCustomFieldRequest, CustomFieldType

client = VaizClient(api_key="your-api-key", space_id="your-space-id")

# Create a new custom field
request = CreateBoardCustomFieldRequest(
    name="Date",
    type=CustomFieldType.DATE,
    boardId="your-board-id",
    description="Date field for tracking deadlines",
    hidden=False
)

response = client.create_board_custom_field(request)
custom_field = response.custom_field

print(f"Created custom field: {custom_field.name} (ID: {custom_field.id})")
```

#### Edit a Board Custom Field

```python
from vaiz import VaizClient, EditBoardCustomFieldRequest

client = VaizClient(api_key="your-api-key", space_id="your-space-id")

# Edit an existing custom field
request = EditBoardCustomFieldRequest(
    fieldId="your-field-id",
    boardId="your-board-id",
    hidden=True,
    description="Updated field description"
)

response = client.edit_board_custom_field(request)
custom_field = response.custom_field

print(f"Updated custom field: {custom_field.name} (ID: {custom_field.id})")
print(f"Hidden: {custom_field.hidden}")
print(f"Description: {custom_field.description}")
```

#### Create a Board Group

```python
from vaiz.models import CreateBoardGroupRequest

request = CreateBoardGroupRequest(
    name="New Group",
    boardId="your-board-id",
    description="This is a new group."
)

response = client.create_board_group(request)
board_groups = response.board_groups
print(f"Board groups: {[g.name for g in board_groups]}")
```

#### Edit a Board Group

```python
from vaiz.models import EditBoardGroupRequest

request = EditBoardGroupRequest(
    boardGroupId="your-group-id",
    boardId="your-board-id",
    name="Updated Group Name",
    description="This is an updated description.",
    limit=20,
    hidden=False
)

response = client.edit_board_group(request)
board_groups = response.board_groups
print(f"Updated board groups: {[g.name for g in board_groups]}")
```

#### Available custom field types:

- `CustomFieldType.TEXT` - Text field
- `CustomFieldType.NUMBER` - Number field
- `CustomFieldType.CHECKBOX` - Checkbox field
- `CustomFieldType.DATE` - Date field
- `CustomFieldType.MEMBER` - Member field
- `CustomFieldType.TASK_RELATIONS` - Task relations field
- `CustomFieldType.SELECT` - Select field
- `CustomFieldType.URL` - Url field

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

#### Create a Task with Description and Files

```python
from vaiz.models import CreateTaskRequest, TaskPriority, TaskFile
from vaiz.models.enums import EUploadFileType

# First, upload a file
upload_response = client.upload_file("/path/to/file.pdf", file_type=EUploadFileType.Pdf)
uploaded_file = upload_response.file

# Create TaskFile object from uploaded file
task_file = TaskFile(
    url=uploaded_file.url,
    name=uploaded_file.name,
    dimension=uploaded_file.dimension,
    ext=uploaded_file.ext,
    _id=uploaded_file.id,
    type=uploaded_file.type
)

# Create task with description and files
task = CreateTaskRequest(
    name="Task with Files",
    group="group_id",
    board="board_id",
    project="project_id",
    priority=TaskPriority.High,
    completed=False,
    description="This task includes a detailed description and attached files for reference.",
    files=[task_file]
)

response = client.create_task(task)
```

**Note:** The examples in the `examples/` folder use real files from the `assets/` directory:

- `assets/example.pdf` - PDF document
- `assets/example.png` - PNG image
- `assets/example.mp4` - MP4 video

These files are used in tests and examples to demonstrate real file upload functionality.

#### Create a Task with Multiple Files

```python
from vaiz.models import CreateTaskRequest, TaskPriority, TaskFile
from vaiz.models.enums import EUploadFileType

# Upload multiple files
files_to_upload = [
    ("/path/to/document.pdf", EUploadFileType.Pdf),
    ("/path/to/image.png", EUploadFileType.Image),
    ("/path/to/video.mp4", EUploadFileType.Video)
]

task_files = []
for file_path, file_type in files_to_upload:
    try:
        upload_response = client.upload_file(file_path, file_type=file_type)
        uploaded_file = upload_response.file

        task_file = TaskFile(
            url=uploaded_file.url,
            name=uploaded_file.name,
            dimension=uploaded_file.dimension,
            ext=uploaded_file.ext,
            _id=uploaded_file.id,
            type=uploaded_file.type
        )
        task_files.append(task_file)
    except Exception as e:
        print(f"Error uploading {file_path}: {e}")

# Create task with multiple files
task = CreateTaskRequest(
    name="Task with Multiple Files",
    group="group_id",
    board="board_id",
    project="project_id",
    priority=TaskPriority.Medium,
    completed=False,
    description="This task contains multiple file attachments of different types.",
    files=task_files
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

#### Edit a Task to Add Description and Files

**Note: This functionality is not yet supported by the API. The examples below demonstrate the intended usage when the API supports these features.**

```python
from vaiz.models import EditTaskRequest, TaskFile
from vaiz.models.enums import EUploadFileType

# First, upload a file
upload_response = client.upload_file("/path/to/file.pdf", file_type=EUploadFileType.Pdf)
uploaded_file = upload_response.file

# Create TaskFile object from uploaded file
task_file = TaskFile(
    url=uploaded_file.url,
    name=uploaded_file.name,
    dimension=uploaded_file.dimension,
    ext=uploaded_file.ext,
    _id=uploaded_file.id,
    type=uploaded_file.type
)

# Edit task to add description and files
edit_task = EditTaskRequest(
    taskId="task_id",
    name="Updated Task with Files",
    description="This task has been updated to include a description and attached files.",
    files=[task_file]
)

response = client.edit_task(edit_task)
```

#### Edit a Task to Update Description Only

**Note: This functionality is not yet supported by the API. The examples below demonstrate the intended usage when the API supports these features.**

```python
from vaiz.models import EditTaskRequest

edit_task = EditTaskRequest(
    taskId="task_id",
)

response = client.edit_task(edit_task)
```

#### Get Task Information

```python
response = client.get_task("task_id")
```

### Working with Files

#### Upload a File

```python
from vaiz.models.enums import EUploadFileType

# Upload a PDF file
response = client.upload_file("/path/to/file.pdf", file_type=EUploadFileType.Pdf)

file = response.file
print(file.url)
```

#### Available File Types

The SDK provides an enum for file types to ensure you are using valid values:

```python
from vaiz.models.enums import EUploadFileType

# Available file types:
# EUploadFileType.Image  - For image files (jpg, png, gif, etc.)
# EUploadFileType.File   - For generic files
# EUploadFileType.Video  - For video files (mp4, avi, mov, etc.)
# EUploadFileType.Pdf    - For PDF documents
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

Tests in this project are designed to run against a real API and database, which requires a valid `VAIZ_API_KEY` and `VAIZ_SPACE_ID` to be configured in your `.env` file. The tests do not use mocks for API calls; instead, they interact with the live environment specified in your configuration.

When writing tests for the SDK:

1. Use the test configuration from `tests/test_config.py` to get a pre-configured client:

```python
from tests.test_config import get_test_client, TEST_BOARD_ID

def test_get_board():
    client = get_test_client()
    response = client.get_board(TEST_BOARD_ID)
    # ... assertions to verify the response
```

2. Structure your tests to perform real operations and validate the responses from the API. For example, a test might create a resource, then retrieve it to ensure it was created correctly.

3. Include proper assertions to verify the state and data of the responses.

4. Be mindful that tests will create, modify, or delete real data in the configured Vaiz space.

### Examples

The SDK includes comprehensive examples demonstrating various API operations:

- **Task Management**: Create and edit tasks with descriptions and file attachments
- **File Upload**: Upload real files from the `assets/` folder (example.pdf, example.png, example.mp4)
- **Board Operations**: Create, edit, and manage boards with custom fields and groups
- **Project Management**: Retrieve project information and board lists
- **Profile Management**: Get user profile information

## Contributing

1. Fork the repository
2. Create a feature branch
3. Write tests for your changes
4. Ensure all tests pass
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
