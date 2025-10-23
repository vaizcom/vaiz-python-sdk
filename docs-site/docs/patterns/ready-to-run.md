---
sidebar_position: 9
---

# Ready-to-Run Examples

Complete, runnable examples from the SDK repository.

The SDK includes a collection of ready-to-run examples in the [`/examples`](https://github.com/vaizcom/vaiz-python-sdk/tree/main/examples) directory.

## Task Management

### Basic Operations
- **`create_task.py`** - Basic task creation
- **`edit_task.py`** - Update existing tasks  
- **`get_tasks.py`** - Query and filter tasks
- **`get_task.py`** - Get single task by ID

### Tasks with Files
- **`create_task_with_files.py`** - Tasks with file attachments
- **`create_task_with_file.py`** - Single file attachment
- **`create_task_with_external_file.py`** - Attach files from URLs
- **`edit_task_with_files.py`** - Update task files
- **`create_task_with_description_and_files.py`** - Description + files

## Documents

### Basic Operations
- **`get_documents.py`** - List documents by scope (Space/Member/Project)
- **`create_document.py`** - Create new documents
- **`get_document.py`** - Get single document
- **`replace_document.py`** - Replace document content with plain text
- **`replace_json_document.py`** - Replace document content with rich JSON (document structure format)
- **`replace_json_document_complex.py`** - Complex document with nested lists, inline code, links, and more
- **`replace_json_document_with_helpers.py`** - Type-safe content creation using document structure helper functions
- **`replace_json_document_with_table.py`** - Creating documents with tables for status reports and metrics
- **`append_json_document.py`** - Appending content to existing documents (incremental updates)

### Advanced Workflows
- **`document_hierarchy.py`** - Build nested document structures
- **`document_content_management.py`** - Work with document content
- **`advanced_document_workflows.py`** - Complex document scenarios
- **`mention_blocks.py`** - Create documents with user, task, document, and milestone mentions
- **`advanced_mention_usage.py`** - Advanced usage of mentions in tables, lists, and complex documents

## Custom Fields

- **`create_board_custom_field.py`** - Add custom fields to boards
- **`edit_board_custom_field.py`** - Modify custom fields
- **`custom_field_helpers_usage.py`** - Using helper functions
- **`advanced_custom_field_management.py`** - Complex custom field workflows
- **`create_task_with_multi_select_custom_field.py`** - Multi-select fields

## Files & Comments

### File Upload
- **`upload_file.py`** - Upload files from disk
- **`upload_file_from_url.py`** - Download and upload from URL

### Comments
- **`post_comment.py`** - Add comments to documents
- **`comment_files.py`** - Comments with file attachments

## Milestones & Projects

### Milestones
- **`create_milestone.py`** - Create milestones
- **`edit_milestone.py`** - Update milestones
- **`get_milestone.py`** - Get single milestone
- **`get_milestones.py`** - List all milestones
- **`toggle_milestone.py`** - Attach/detach milestones to tasks

### Projects
- **`get_project.py`** - Get single project
- **`get_projects.py`** - List all projects

## Boards

- **`get_board.py`** - Get single board
- **`get_boards.py`** - List all boards
- **`create_board_type.py`** - Create board types (Bug, Feature, etc.)
- **`edit_board_type.py`** - Modify board types
- **`create_board_group.py`** - Create board groups (columns)
- **`edit_board_group.py`** - Modify board groups

## Other

- **`get_profile.py`** - Get current user profile
- **`get_space.py`** - Get space information
- **`get_space_members.py`** - Get all space members
- **`get_history.py`** - Get change history
- **`test_helpers.py`** - Test helper functions
- **`test_caching_simple.py`** - Test caching behavior
- **`test_auth_error.py`** - Test authentication errors

## Running the Examples

**1. Clone the repository:**
   ```bash
   git clone https://github.com/vaizcom/vaiz-python-sdk.git
   cd vaiz-python-sdk
   ```

**2. Install dependencies:**
   ```bash
   pip install -e .
   pip install python-dotenv
   ```

**3. Configure environment:**
   ```bash
   cp example.env .env
   # Edit .env with your credentials
   ```

**4. Run an example:**
   ```bash
   cd examples
   python create_task.py
   ```

## Example Configuration

All examples use `config.py` for shared configuration:

```python
# examples/config.py
import os
from dotenv import load_dotenv
from vaiz import VaizClient

load_dotenv()

client = VaizClient(
    api_key=os.getenv("VAIZ_API_KEY"),
    space_id=os.getenv("VAIZ_SPACE_ID")
)

# Fetch dynamic IDs
profile = client.get_profile()
projects = client.get_projects()
boards = client.get_boards()

member_id = profile.profile.member_id
project_id = projects.projects[0].id if projects.projects else None
board_id = boards.boards[0].id if boards.boards else None
```

[View all examples on GitHub →](https://github.com/vaizcom/vaiz-python-sdk/tree/main/examples)

## See Also

- [Environment Setup](./environment-setup) - Configure your environment
- [Common Patterns](./common-patterns) - Essential patterns
- [Real-World Scenarios](./real-world) - Complete use cases

