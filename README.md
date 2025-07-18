# Vaiz SDK for Python

Python SDK for accessing the Vaiz platform API.

## 🚀 What's New

### v0.4.2
- **🕓 Task and Entity History**: New `get_history` method for retrieving the change history of tasks and other objects
- **📦 New Models**: `GetHistoryRequest`, `GetHistoryResponse`, `HistoryItem`, `HistoryData`
- **🧪 Usage Example**: see `examples/get_history.py`
- **🛠️ Improvements**: alias fixes, environment variable handling, test stability

### v0.4.1
- **Improved datetime support** in all models
- **Updated examples and tests** for new models

### v0.4.0
- **🔄 Automatic DateTime Conversion**: All date/time fields now automatically convert between Python `datetime` objects and ISO strings
- **💬 Full Comment System**: Post, edit, delete comments with file attachments, replies, and emoji reactions
- **🔧 Updated Examples**: All examples now demonstrate datetime best practices
- **📖 Comprehensive Documentation**: New DateTime Support section with examples

#### Breaking Changes
- Date fields now return `datetime` objects instead of strings (automatic parsing from API)
- All models updated to inherit from `VaizBaseModel` for datetime support

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

### DateTime Support

The Vaiz SDK provides **automatic datetime conversion** for all date/time fields. You can work with Python `datetime` objects instead of ISO strings:

#### Features

- **📥 Automatic Parsing**: ISO strings from API → Python `datetime` objects
- **📤 Automatic Serialization**: Python `datetime` objects → ISO strings for API
- **🔄 Bidirectional**: Works seamlessly in both directions
- **✨ Developer Friendly**: Use native Python datetime operations

#### Example

```python
from datetime import datetime
from vaiz.models import CreateTaskRequest, TaskPriority

# Create task with datetime objects (recommended)
task = CreateTaskRequest(
    name="Project Deadline",
    group="group_id",
    board="board_id",
    project="project_id",
    priority=TaskPriority.High,
    dueStart=datetime(2025, 2, 1, 9, 0, 0),    # February 1st, 9:00 AM
    dueEnd=datetime(2025, 2, 15, 17, 0, 0)     # February 15th, 5:00 PM
)

response = client.create_task(task)

# Access as datetime objects
print(f"Created: {response.task.createdAt}")     # datetime object
print(f"Due: {response.task.dueEnd}")           # datetime object
print(f"Year: {response.task.dueEnd.year}")     # 2025

# Automatic API serialization happens behind the scenes
# API receives: {"dueStart": "2025-02-01T09:00:00", "dueEnd": "2025-02-15T17:00:00"}
```

#### Supported Fields

All date/time fields across the SDK support datetime conversion:

- `created_at`, `updated_at`, `edited_at`, `deleted_at`
- `archived_at`, `completed_at`
- `due_start`, `due_end`, `dueStart`, `dueEnd`
- `registeredDate`, `passwordChangedDate`

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
from datetime import datetime
from vaiz.models import CreateMilestoneRequest

# Basic milestone
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

#### Create a Milestone with DateTime Ranges

You can create milestones with specific start and end dates using Python `datetime` objects:

```python
from datetime import datetime
from vaiz.models import CreateMilestoneRequest

# Milestone with datetime ranges (recommended approach)
milestone_with_dates = CreateMilestoneRequest(
    name="Q1 2025 Milestone",
    description="First quarter milestone with specific dates",
    board="board_id",
    project="project_id",
    due_start=datetime(2025, 3, 1, 9, 0, 0),      # March 1st, 9:00 AM
    due_end=datetime(2025, 3, 31, 17, 0, 0),      # March 31st, 5:00 PM
    color="#4CAF50"  # Green color
)

response = client.create_milestone(milestone_with_dates)
milestone = response.milestone

# Access datetime objects directly
print(f"Due start: {milestone.due_start}")  # datetime object
print(f"Due end: {milestone.due_end}")      # datetime object
print(f"Created at: {milestone.created_at}")  # datetime object
```

#### Edit a Milestone

```python
from datetime import datetime
from vaiz.models import EditMilestoneRequest

# Edit an existing milestone with datetime objects
edit_request = EditMilestoneRequest(
    milestone_id="milestone_id",
    name="Updated Milestone Name",  # Optional
    description="Updated description",  # Optional
    due_start=datetime(2025, 6, 1, 9, 0, 0),      # June 1st, 9:00 AM (Optional)
    due_end=datetime(2025, 12, 31, 23, 59, 59)    # December 31st, 11:59 PM (Optional)
)

response = client.edit_milestone(edit_request)
updated_milestone = response.milestone
print(f"Updated milestone: {updated_milestone.name}")
print(f"Description: {updated_milestone.description}")
print(f"Due start: {updated_milestone.due_start}")  # datetime object
print(f"Due end: {updated_milestone.due_end}")      # datetime object
print(f"Last edited by: {updated_milestone.editor}")
```

**Note**: All fields except `milestone_id` are optional in EditMilestoneRequest. Only provide the fields you want to update. The SDK automatically converts `datetime` objects to ISO strings for the API.

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
from datetime import datetime
from vaiz.models import CreateTaskRequest, TaskPriority

# Basic task
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

#### Create a Task with DateTime Deadlines

The SDK automatically converts Python `datetime` objects to ISO strings for the API and parses ISO strings back to `datetime` objects:

```python
from datetime import datetime
from vaiz.models import CreateTaskRequest, TaskPriority

# Task with datetime deadlines (recommended approach)
task_with_dates = CreateTaskRequest(
    name="Project Deadline Task",
    description="Task with specific start and end dates",
    group="group_id",
    board="board_id",
    project="project_id",
    priority=TaskPriority.Medium,
    completed=False,
    dueStart=datetime(2025, 2, 1, 9, 0, 0),    # February 1st, 9:00 AM
    dueEnd=datetime(2025, 2, 15, 17, 0, 0)     # February 15th, 5:00 PM
)

response = client.create_task(task_with_dates)

# Access datetime objects directly
print(f"Due start: {response.task.dueStart}")  # datetime object
print(f"Created at: {response.task.createdAt}")  # datetime object
```

#### Edit a Task with DateTime Updates

You can update task deadlines and other fields using datetime objects:

```python
from datetime import datetime
from vaiz.models import EditTaskRequest, TaskPriority

# Edit an existing task with new datetime deadlines
edit_request = EditTaskRequest(
    taskId="existing_task_id",
    name="Updated Task with New Deadlines",
    priority=TaskPriority.High,
    completed=False,
    assignees=["user_id"],
    dueStart=datetime(2025, 4, 1, 9, 0, 0),    # April 1st, 9:00 AM
    dueEnd=datetime(2025, 4, 30, 17, 0, 0)     # April 30th, 5:00 PM
)

response = client.edit_task(edit_request)

# Access updated datetime objects
updated_task = response.payload["task"]
print(f"Updated due start: {updated_task['dueStart']}")  # ISO string from API
print(f"Updated due end: {updated_task['dueEnd']}")      # ISO string from API
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

### Retrieve Task or Entity History

You can retrieve the full change history for a task (or other supported entity) using the `get_history` method. This returns a list of history events with all relevant metadata.

```python
from vaiz import VaizClient
from vaiz.models import GetHistoryRequest
from vaiz.models.enums import EKind

client = VaizClient(api_key="...", space_id="...", base_url="https://api.vaiz.local:10000/v4", verify_ssl=False)

# Retrieve history by task ID
task_id = "your_task_id"
request = GetHistoryRequest(kind=EKind.Task, kindId=task_id)
response = client.get_history(request)

for history in response.payload.histories:
    print(history.key, history.createdAt, history.data)
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

### Working with Comments

**Important:** Comments require a valid `document_id` from an existing task. You can get this from getting or creating a task:

```python
# First, create a task to get a document ID
task_response = client.create_task(CreateTaskRequest(
    name="My Task",
    group="your_group_id",
    board="your_board_id",
    project="your_project_id"
))
document_id = task_response.task.document
```

#### Post a Comment

```python
# Post a simple text comment
response = client.post_comment(
    document_id="your_document_id",
    content="Simple text comment"
)

comment = response.comment
print(f"Comment ID: {comment.id}")
```

#### Post a Comment with HTML Content

```python
# Post a comment with HTML formatting
response = client.post_comment(
    document_id="your_document_id",
    content="<p>Comment with <em>italic</em> and <strong>bold</strong> text</p>"
)

comment = response.comment
print(f"Comment content: {comment.content}")
print(f"Author ID: {comment.author_id}")
print(f"Created at: {comment.created_at}")
```

#### Post a Comment with File Attachments

```python
from vaiz.models.enums import EUploadFileType

# First upload files with explicit type specification
upload_response1 = client.upload_file("path/to/image.png", EUploadFileType.Image)  # Will display as image preview
upload_response2 = client.upload_file("path/to/document.pdf", EUploadFileType.Pdf)  # Will display as PDF viewer
upload_response3 = client.upload_file("path/to/video.mp4", EUploadFileType.Video)  # Will display as video player

# You can also upload the same file as different types:
upload_response4 = client.upload_file("path/to/image.png", EUploadFileType.File)  # Will display as downloadable file

file_ids = [upload_response1.file.id, upload_response2.file.id, upload_response3.file.id]

# Post comment with file attachments
response = client.post_comment(
    document_id="your_document_id",
    content="<p>Comment with <strong>multiple files</strong> attached</p>",
    file_ids=file_ids
)

comment = response.comment
print(f"Attached files: {len(comment.files)}")
for file in comment.files:
    print(f"  - {file.original_name} ({file.size} bytes) [Type: {file.type.value}]")
```

**File Type Options:**

- `EUploadFileType.Image` - Displays as image preview/thumbnail
- `EUploadFileType.Video` - Displays as video player with controls
- `EUploadFileType.Pdf` - Displays as PDF viewer/preview
- `EUploadFileType.File` - Displays as downloadable file attachment

**Important:** You must explicitly specify the file type to control how it appears in the interface. The same file can be uploaded with different types for different display purposes.

**Example - Same Image File, Different Display Types:**

```python
from vaiz.models.enums import EUploadFileType

# Upload same image file with different types
image_as_preview = client.upload_file("screenshot.png", EUploadFileType.Image)    # Shows preview thumbnail
image_as_file = client.upload_file("screenshot.png", EUploadFileType.File)       # Shows download link

# In comments, users will see:
# - Image type: Preview thumbnail that can be clicked to view full size
# - File type: File icon with filename for download only

# Use Image type for: photos, diagrams, screenshots you want to display
# Use File type for: images you want to share as downloadable assets
```

#### Post a Reply to a Comment

```python
# First, create an original comment
original_response = client.post_comment(
    document_id="your_document_id",
    content="<p>Original comment</p>"
)

# Now post a reply to that comment
reply_response = client.post_comment(
    document_id="your_document_id",
    content="<p>This is a reply to the original comment</p>",
    reply_to=original_response.comment.id
)

reply_comment = reply_response.comment
print(f"Reply ID: {reply_comment.id}")
print(f"Replying to: {reply_comment.reply_to}")
print(f"Is reply: {reply_comment.reply_to is not None}")
```

#### React to a Comment (Simplified API)

```python
from vaiz.models import CommentReactionType

# First, create a comment to react to
comment_response = client.post_comment(
    document_id="your_document_id",
    content="<p>This comment will get reactions!</p>"
)

# Add popular reactions using the simplified API
reaction_response = client.add_reaction(
    comment_id=comment_response.comment.id,
    reaction=CommentReactionType.THUMBS_UP
)

# Add more reactions
client.add_reaction(comment_response.comment.id, CommentReactionType.HEART)
client.add_reaction(comment_response.comment.id, CommentReactionType.LAUGHING)
client.add_reaction(comment_response.comment.id, CommentReactionType.WOW)
client.add_reaction(comment_response.comment.id, CommentReactionType.CRYING)
client.add_reaction(comment_response.comment.id, CommentReactionType.ANGRY)
client.add_reaction(comment_response.comment.id, CommentReactionType.PARTY)

# Access the reactions
for reaction in reaction_response.reactions:
    print(f"Reaction: {reaction.native} ({reaction.emoji_id})")
    print(f"Members who reacted: {len(reaction.member_ids)}")
```

#### Available Reactions

The SDK provides 7 popular emoji reactions based on emoji-picker-react standards:

- `CommentReactionType.THUMBS_UP` - 👍 Thumbs Up Sign
- `CommentReactionType.HEART` - ❤️ Red Heart
- `CommentReactionType.LAUGHING` - 😂 Face with Tears of Joy
- `CommentReactionType.WOW` - 😮 Face with Open Mouth
- `CommentReactionType.CRYING` - 😢 Crying Face
- `CommentReactionType.ANGRY` - 😡 Pouting Face
- `CommentReactionType.PARTY` - 🎉 Party Popper

#### React to a Comment (Advanced API)

For custom emoji reactions not in the popular list, use the advanced API:

```python
# Add a custom reaction
reaction_response = client.react_to_comment(
    comment_id=comment_response.comment.id,
    emoji_id="kissing_smiling_eyes",
    emoji_name="Kissing Face with Smiling Eyes",
    emoji_native="😙",
    emoji_unified="1f619",
    emoji_keywords=["affection", "valentines", "infatuation", "kiss"],
    emoji_shortcodes=":kissing_smiling_eyes:"
)
```

#### Get Comments for a Document

```python
# Get all comments for a document
comments_response = client.get_comments(document_id="your_document_id")

print(f"Total comments: {len(comments_response.comments)}")

# Iterate through comments
for comment in comments_response.comments:
    print(f"Comment: {comment.content}")
    print(f"Author: {comment.author_id}")
    print(f"Created: {comment.created_at}")

    # Check if it's a reply
    if comment.reply_to:
        print(f"Reply to: {comment.reply_to}")

    # Show reactions
    if comment.reactions:
        for reaction in comment.reactions:
            print(f"Reaction: {reaction.native} - {len(reaction.member_ids)} member(s)")
```

#### Edit a Comment

```python
# Edit comment content
edit_response = client.edit_comment(
    comment_id="your_comment_id",
    content="<p><strong>Updated</strong> comment content</p>"
)

print(f"Comment edited at: {edit_response.comment.edited_at}")
print(f"New content: {edit_response.comment.content}")

# Edit comment with file operations
edit_response = client.edit_comment(
    comment_id="your_comment_id",
    content="<p>Updated content</p>",
    add_file_ids=["507f1f77bcf86cd799439011"],      # Add files (valid MongoDB IDs)
    order_file_ids=["507f1f77bcf86cd799439011"],     # Reorder files
    remove_file_ids=["507f1f77bcf86cd799439012"]     # Remove files
)

# Access file information from edited comment
for file in edit_response.comment.files:
    print(f"File: {file.original_name} (ID: {file.id})")
```

**File Operations:**

- `add_file_ids`: Upload files first, then add their IDs to the comment
- `order_file_ids`: Specify the desired order of all files in the comment
- `remove_file_ids`: Remove specific files from the comment

**Note:** Files are `UploadedFile` objects with properties like `id`, `original_name`, `size`, `url`, etc.

#### Delete a Comment

```python
# Soft delete (content cleared but comment preserved in system)
delete_response = client.delete_comment(comment_id="your_comment_id")

deleted_comment = delete_response.comment
print(f"Deleted at: {deleted_comment.deleted_at}")
print(f"Content: '{deleted_comment.content}'")  # Empty string after deletion
```

All comment models support field aliases and automatic serialization:

```python
from vaiz.models import PostCommentRequest, ReactToCommentRequest

# Create a comment request manually
request = PostCommentRequest(
    document_id="your_document_id",
    content="<p>Manual comment request</p>",
    file_ids=["file1", "file2"]
)

# The request will be automatically serialized with correct field names
data = request.model_dump()
# Results in: {"documentId": "...", "content": "...", "fileIds": [...]}

# Create a reply request
reply_request = PostCommentRequest(
    document_id="your_document_id",
    content="<p>Reply to comment</p>",
    reply_to="original_comment_id"
)

reply_data = reply_request.model_dump()
# Results in: {"documentId": "...", "content": "...", "fileIds": [], "replyTo": "..."}

# Create a reaction request
reaction_request = ReactToCommentRequest(
    comment_id="comment_id",
    id="heart_eyes",
    name="Smiling Face with Heart-Eyes",
    native="😍",
    unified="1f60d",
    keywords=["love", "crush", "heart"],
    shortcodes=":heart_eyes:"
)

reaction_data = reaction_request.model_dump()
# Results in: {"commentId": "...", "id": "heart_eyes", "name": "...", "native": "😍", ...}
```

### Examples

The SDK includes comprehensive examples demonstrating various API operations:

- **Task Management**: Create and edit tasks with descriptions and file attachments
- **File Upload**: Upload real files from the `assets/` folder (example.pdf, example.png, example.mp4)
- **Board Operations**: Create, edit, and manage boards with custom fields and groups
- **Comment System**: Complete CRUD operations with HTML content, reactions, replies, file attachments, and soft delete

#### Testing and Development

For testing or development purposes, the examples use dynamic document IDs via helper functions in `examples/test_helpers.py`:

```python
from examples.test_helpers import get_or_create_document_id

# This will create a test task and return its document_id
document_id = get_or_create_document_id()

# Now you can use this document_id for comment operations
response = client.post_comment(
    document_id=document_id,
    content="Test comment"
)
```

This approach ensures that examples and tests work across different environments without hardcoded IDs.

- **Project Management**: Retrieve project information and board lists
- **Profile Management**: Get user profile information
- **Comment Management**: Post comments with HTML content, file attachments, replies, and reactions

## Contributing

1. Fork the repository
2. Create a feature branch
3. Write tests for your changes
4. Ensure all tests pass
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
