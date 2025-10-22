---
sidebar_position: 2
---

# Tasks

Complete reference for task-related methods and models.

## Methods

### `create_task`

```python
create_task(
    task: CreateTaskRequest,
    description: str = None,
    file: TaskUploadFile = None
) -> TaskResponse
```

Create a new task with optional description and file upload.

**Parameters:**
- `task` - Task configuration (name, board required; group, project optional)
- `description` - Optional task description (plain text). For rich content, use `replace_json_document` with [document structure format](./document-structure)
- `file` - Optional file to upload and attach

**Returns:** `TaskResponse` with created task

**Note:** To add rich formatted content to task descriptions, create the task first, then use `replace_json_document(task.document, content)`. See [Document Structure](./document-structure) for details.

---

### `edit_task`

```python
edit_task(task: EditTaskRequest) -> TaskResponse
```

Edit an existing task. Only provide fields you want to update.

**Parameters:**
- `task` - Edit request with task_id and fields to update

**Returns:** `TaskResponse` with updated task

---

### `get_task`

```python
get_task(slug: str) -> TaskResponse
```

Get task by HRID or database ID.

**Parameters:**
- `slug` - Task HRID (e.g., "PRJ-123") or database ID

**Returns:** `TaskResponse` with task data

---

### `get_tasks`

```python
get_tasks(request: GetTasksRequest) -> GetTasksResponse
```

Get multiple tasks with filtering and pagination (max 50 per request).

**Parameters:**
- `request` - Filter and pagination parameters

**Returns:** `GetTasksResponse` with list of tasks

**Note:** Results are automatically cached for 5 minutes. Use `clear_tasks_cache()` to clear.

---

### `clear_tasks_cache`

```python
clear_tasks_cache() -> None
```

Clear the get_tasks() cache manually.

---

## Models

### Task

Main task model representing a task in the system.

```python
class Task:
    id: str                             # Task ID
    name: str                           # Task name
    hrid: str                           # Human-readable ID (e.g., "PRJ-123")
    board: str                          # Board ID
    group: str                          # Group ID
    project: str                        # Project ID
    priority: TaskPriority              # Priority level
    completed: bool                     # Completion status
    assignees: List[str]                # Assignee IDs
    types: List[str]                    # Type IDs
    parent_task: Optional[str]          # Parent task ID
    subtasks: List[str]                 # Subtask IDs
    milestones: List[str]               # Milestone IDs
    milestone: Optional[str]            # Main milestone ID
    due_start: Optional[datetime]       # Start date
    due_end: Optional[datetime]         # Due date
    blockers: List[str]                 # Blocker task IDs
    blocking: List[str]                 # Blocked task IDs
    custom_fields: List[TaskCustomField]  # Custom field values
    document: str                       # Document ID
    creator: str                        # Creator ID
    editor: Optional[str]               # Last editor ID
    archiver: Optional[str]             # Archiver ID (if archived)
    deleter: Optional[str]              # Deleter ID (if deleted)
    created_at: datetime                # Creation timestamp
    updated_at: datetime                # Last update timestamp
    completed_at: Optional[datetime]    # Completion timestamp
    archived_at: Optional[datetime]     # Archive timestamp
    deleted_at: Optional[datetime]      # Deletion timestamp
    followers: Dict[str, str]           # Follower mapping
```

---

### TaskCustomField

```python
class TaskCustomField:
    id: str                             # Custom field ID
    value: Any                          # Field value
    _id: str                            # Database ID
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
    dimension: Optional[List[int]]      # Dimensions [width, height]
    size: Optional[int]                 # File size in bytes
    dominant_color: Optional[Dict]      # Dominant color info
    mime: Optional[str]                 # MIME type
    original_name: Optional[str]        # Original filename
    date: Optional[datetime]            # Upload date
    owner: Optional[str]                # Owner ID
    access_kind: Optional[str]          # Access kind
    access_kind_id: Optional[str]       # Access kind ID
```

---

### TaskUploadFile

```python
class TaskUploadFile:
    path: str                           # File path
    type: Optional[UploadFileType]     # File type (auto-detected if not provided)
```

---

## Request Models

### CreateTaskRequest

```python
class CreateTaskRequest:
    name: str                           # Required - Task name
    board: str                          # Required - Board ID
    group: Optional[str]                # Optional - Group ID
    project: Optional[str]              # Optional - Project ID
    description: Optional[str]          # Task description
    priority: TaskPriority              # Priority (default: General)
    completed: bool                     # Completion status (default: False)
    assignees: List[str]                # Assignee user IDs
    types: List[str]                    # Task type IDs
    parent_task: Optional[str]          # Parent task ID (for subtasks)
    subtasks: List[str]                 # Subtask IDs
    milestones: List[str]               # Milestone IDs
    due_start: Optional[datetime]       # Start date
    due_end: Optional[datetime]         # Due date
    blockers: List[str]                 # Task IDs that block this task
    blocking: List[str]                 # Task IDs this task blocks
    custom_fields: List[CustomField]    # Custom field values
    files: List[TaskFile]               # Attached files
```

---

### EditTaskRequest

```python
class EditTaskRequest:
    task_id: str                        # Required - Task ID to edit
    name: Optional[str]                 # New name
    priority: Optional[TaskPriority]    # New priority
    completed: Optional[bool]           # New completion status
    assignees: Optional[List[str]]      # New assignees
    types: Optional[List[str]]          # New types
    parent_task: Optional[str]          # New parent task
    subtasks: Optional[List[str]]       # New subtasks
    milestones: Optional[List[str]]     # New milestones
    due_start: Optional[datetime]       # New start date
    due_end: Optional[datetime]         # New due date
    blockers: Optional[List[str]]       # New blockers
    blocking: Optional[List[str]]       # New blocking
    custom_fields: Optional[List[CustomField]]  # New custom fields
    description: Optional[str]          # New description
    files: Optional[List[TaskFile]]     # New files
```

---

### GetTasksRequest

```python
class GetTasksRequest:
    ids: Optional[List[str]]            # Filter by task IDs
    limit: int                          # Results per page (1-50, default: 50)
    skip: int                           # Skip N tasks (default: 0)
    board: Optional[str]                # Filter by board ID
    project: Optional[str]              # Filter by project ID
    assignees: Optional[List[str]]      # Filter by assignee IDs
    parent_task: Optional[str]          # Filter by parent task ID
    milestones: Optional[List[str]]     # Filter by milestone IDs
    completed: Optional[bool]           # Filter by completion status
    archived: Optional[bool]            # Filter by archived status
```

---

## Response Models

### TaskResponse

```python
class TaskResponse:
    payload: Dict[str, Any]             # Response payload
    type: str                           # Response type ("CreateTask", "EditTask", "GetTask")
    
    @property
    def task(self) -> Task:             # Parsed task object
        ...
```

---

### GetTasksResponse

```python
class GetTasksResponse:
    type: str                           # Response type ("GetTasks")
    payload: GetTasksPayload            # Response payload
```

---

### GetTasksPayload

```python
class GetTasksPayload:
    tasks: List[Task]                   # List of tasks
```

---

## See Also

- [Tasks Guide](../guides/tasks) - Usage examples and patterns
- [Document Structure](./document-structure) - Format for task descriptions with rich content
- [Enums](./enums) - TaskPriority and other enums

