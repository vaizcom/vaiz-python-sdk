# Changelog

## [1.0.0] - 2026-06-11

The SDK is now **Markdown-only** for rich content. All TipTap/JSON document APIs and the document structure DSL have been removed. Markdown is converted to native editor blocks on the server and can be read back as Markdown.

### Added

- **📝 Markdown Document API**: The only way to work with document content
  - `replace_markdown_document(document_id, markdown)` - Replace document content with Markdown
  - `append_markdown_document(document_id, markdown)` - Append Markdown to existing content
  - `get_markdown_document(document_id)` - Read document content back as a Markdown string
  - Markdown is converted to native rich editor blocks on the server (headings, lists, tables, code blocks, checklists, links, etc.)
- **🏷️ Markdown Mentions**: New `@[label](kind:id)` syntax for mentions in documents and comments
  - Supported kinds: `user`, `task`, `document`, `milestone`, `project`, `board`
  - Example: `@[John](user:6a29be79cb3b2bee09db40bd)` becomes a live mention chip and triggers notifications
  - Mentions survive markdown round-trips: `get_markdown_document()` exports them in the same syntax
- **💬 Markdown Comments**: New `markdown` parameter in `post_comment()` and `edit_comment()`
  - Markdown is converted to rich comment content on the server and stored with `content_version = 2`
  - `markdown` and `content` are mutually exclusive — provide exactly one (otherwise `ValueError` is raised)
  - New `Comment.content_version` field (`2` = rich/markdown-based, `None` = legacy HTML)
- New `Tree` icon in the `Icon` enum

### Removed (Breaking)

- **TipTap/JSON document methods**: `get_json_document()`, `replace_json_document()`, `append_json_document()`, `replace_document()`, `append_document()` and their request/response models
- **Document structure DSL** (`vaiz.helpers.document_structure`): all node builders (`paragraph()`, `heading()`, `bullet_list()`, `table()`, `image_block()`, `embed_block()`, `mention_*()`, etc.), all node types, and the `EmbedType` enum

### Changed (Breaking)

- `Task.get_task_description(client)` now returns the description as a Markdown string (previously a parsed JSON dict)
- `Task.update_task_description(client, markdown)` now accepts Markdown and uses `replace_markdown_document()` under the hood
- `post_comment()` and `edit_comment()`: the `content` parameter is now optional; provide exactly one of `content` (legacy HTML) or `markdown` (recommended)
- `get_space_members()` now excludes bot members (AI, automation, and integration bots) from the result
- `toggle_milestone()` no longer sets the task's main `milestone` field — only the `milestones` list is updated

### Migration Guide

| Removed (TipTap / JSON DSL) | Replacement (Markdown) |
| --- | --- |
| `client.replace_json_document(doc_id, [heading(1, "Title"), paragraph("text")])` | `client.replace_markdown_document(doc_id, "# Title\n\ntext")` |
| `client.append_json_document(doc_id, [paragraph("more")])` | `client.append_markdown_document(doc_id, "more")` |
| `client.replace_document(doc_id, "plain text")` | `client.replace_markdown_document(doc_id, "plain text")` |
| `client.append_document(doc_id, "plain text")` | `client.append_markdown_document(doc_id, "plain text")` |
| `client.get_json_document(doc_id)` | `client.get_markdown_document(doc_id)` |
| `paragraph("Hello ", text("World", bold=True))` | `"Hello **World**"` |
| `heading(2, "Section")` | `"## Section"` |
| `bullet_list("a", "b")` / `ordered_list("a", "b")` | `"- a\n- b"` / `"1. a\n2. b"` |
| `task_list(task_item("Do it", checked=True))` | `"- [x] Do it"` |
| `table(table_row(table_header("H")), table_row("v"))` | `"\| H \|\n\| --- \|\n\| v \|"` |
| `code_block("print(1)", language="python")` | <code>"```python\nprint(1)\n```"</code> |
| `link_text("Vaiz", "https://vaiz.app")` | `"[Vaiz](https://vaiz.app)"` |
| `mention_user("id")` / `mention_task("id")` / ... | `"@[label](user:id)"` / `"@[label](task:id)"` / ... |
| `embed_block(...)`, `image_block(...)`, `toc_block()`, etc. | No direct replacement; managed by the editor UI |
| `client.post_comment(doc_id, content="<p>Hi <strong>there</strong></p>")` | `client.post_comment(doc_id, markdown="Hi **there**")` |
| Rich `create_task(description=...)` | `description` is plain text only; for rich content: `task = client.create_task(...).task` then `client.replace_markdown_document(task.document, markdown)` |

Old SDK versions (≤ 0.19.x) keep working: the server-side JSON document endpoints are not removed, only the SDK surface.

## [0.19.0] - 2026-02-17

### Added

- **🔀 Move Tasks API**: New `move_tasks()` method for moving tasks between board groups
  - `MoveTaskItem` - Specify task, target group, and position
  - `MoveTasksRequest` - Batch move multiple tasks in one call
  - `MoveTasksResponse` - Response with success/failed task IDs
- **📜 History API**: Added missing filter parameters to `GetHistoryRequest`
  - `createdBy` - Filter by creator member IDs
  - `dateRangeStart` / `dateRangeEnd` - Date range filters
  - `limit` - Limit number of results
  - `keys` - Include only specific event keys
  - `tasksIds` - Filter by task IDs
  - `groupsIds` - Filter by group IDs

### Changed

- **🔧 Breaking**: Removed `group` field from `EditTaskRequest` — use `move_tasks()` instead
  - Migration: Replace `client.edit_task(EditTaskRequest(task_id=..., group=...))` with `client.move_tasks(MoveTasksRequest(moves=[MoveTaskItem(task_id=..., to_group_id=...)]))`

## [0.18.0] - 2025-10-29

### Added

- **📝 Edit Document API**: New method to edit document metadata
  - `edit_document` - Update document properties

## [0.17.0] - 2025-10-24

### Added

- **🎬 Embed Blocks**: Support for embedding external content (YouTube, Figma, CodeSandbox, etc.)
  - `embed_block(url, embed_type, size, is_content_hidden)` - Create embed blocks for external content
  - `EmbedType` enum - Type-safe embed types (YOUTUBE, FIGMA, VIMEO, CODESANDBOX, GITHUB_GIST, MIRO, IFRAME)

## [0.16.0] - 2025-10-24

### Changed

- **🔧 Breaking**: Simplified `image_block()` API - now accepts file object directly
  - **Old API** (deprecated): `image_block(file_id=..., src=..., file_name=..., file_size=..., extension=..., dimensions=...)`
  - **New API**: `image_block(file=uploaded.file, caption="...", width_percent=100)`
  - Reduces code by 80% - just pass the file object!
  - All file metadata extracted automatically from uploaded file
  - MIME type auto-detected from extension or file.mime
  - Aspect ratio auto-calculated from dimensions
  - Migration: Replace multiple parameters with single `file=uploaded.file` parameter

## [0.15.0] - 2025-10-24

### Added

- **✅ Task Lists (Checklists)**: Interactive checklists with checked/unchecked states
  - `task_list(*items)` - Create a checklist container
  - `task_item(content, checked=False)` - Create individual checklist items
  - Support for nested checklists (unlimited depth)
  - Each task item can contain paragraphs and nested task lists
  - `checked` attribute tracks completion status (boolean)
  - Auto-generated UIDs for task lists
  - Full integration with document API (`replace_json_document`, `append_json_document`)
  
- **New Document Structure Types**:
  - `TaskListNode` - Type for task list container
  - `TaskItemNode` - Type for individual checklist items
  - `TaskListAttrs` - Attributes for task lists (uid)
  - `TaskItemAttrs` - Attributes for task items (checked status)

## [0.14.0] - 2025-10-24

### Added

- **📑 TOC Block**: Automatic table of contents generation
  - `toc_block()` - Creates interactive document outline
  - Automatically indexes all headings (h1-h6)
  - Clickable navigation links to document sections
  - Auto-updates when document content changes

- **🔗 Anchors Block**: Related documents and backlinks
  - `anchors_block()` - Displays document relationships
  - Shows documents that this document links to
  - Shows backlinks (documents linking to this one)
  - Visualizes knowledge graph connections

- **📄 Siblings Block**: Previous/Next document navigation
  - `siblings_block()` - Creates Previous/Next navigation buttons
  - Shows Previous and Next documents in sequence
  - Typically placed at the bottom of the page
  - Perfect for tutorial series and sequential guides
  - Maintains document order in branch

- **💻 Code Block**: Syntax-highlighted code snippets
  - `code_block(code, language)` - Display code with highlighting
  - Support for Python, JavaScript, TypeScript, Java, C++, Go, Rust, SQL, Bash, and many more
  - Multiline code support
  - Optional language specification

### Changed

- **🔧 Headings now auto-generate UIDs**: All headings created with `heading()` now automatically get unique IDs for TOC navigation support
  - UIDs are 12-character alphanumeric strings (e.g., "sEeaN9ddIDsL")
  - Required for TOC block to create working navigation links
  - No breaking changes - UIDs added automatically

---

## [0.13.0] - 2025-10-23

### Changed

- **🔧 Breaking**: `mention_user()` now accepts `member_id` instead of `user_id`
  - **Migration**: Update your code to use `member_id` from `get_profile().profile.member_id` or `get_space_members()`
  - **Why**: Clarifies that the parameter should be member ID, not user ID
  - **Example**: `mention_user(profile.profile.member_id)`

---

## [0.12.0] - 2025-10-23

### Added

- **👤 Mention Blocks**: Create interactive references to users, documents, tasks, and milestones
  - `mention_user(member_id)` - Mention a team member
  - `mention_document(id)` - Reference a document
  - `mention_task(id)` - Reference a task
  - `mention_milestone(id)` - Reference a milestone
  - `mention(id, kind)` - Generic mention with explicit kind
  - Mentions work in paragraphs, lists, tables, and all document structures
  - Full type safety with TypedDict definitions

- **📸 Image Blocks**: Embed images in documents
  - `image_block()` - Create image block with uploaded file
  - Support for dimensions, captions, and custom width
  - Automatic aspect ratio calculation
  - Works with uploaded images via `upload_file()`

- **📎 Files Blocks**: Attach files to documents
  - `files_block()` - Create files block with multiple attachments
  - Support for PDFs, images, videos, and other file types
  - Automatic unique ID generation for each file
  - Works with uploaded files via `upload_file()`

---

## [0.11.0] - 2025-10-23

### Added

- **💬 Blockquote**: New `blockquote()` function for creating quoted text and callouts
  - Simple quotes: `blockquote("Quote text")`
  - Multi-paragraph quotes with formatting
  - Perfect for important notes, warnings, and citations

- **📂 Details (Collapsible Sections)**: New collapsible content blocks
  - `details(summary, content)` - Create expandable/collapsible sections
  - `details_summary()` - Always visible header
  - `details_content()` - Hidden content that expands on click
  - Great for FAQs, technical details, and optional information

---

## [0.10.0] - 2025-10-23

### Added

- **📊 Table Headers**: New `table_header()` function for creating semantic table header cells

### Fixed

- **🐛 Test Improvements**: Fixed `test_get_milestone` to create milestone before fetching (no longer depends on existing data)

---

## [0.9.1] - 2025-10-22

### Added

- **📏 Horizontal Rule**: Added `horizontal_rule()` helper for creating horizontal dividers

### Changed

- **🔧 Breaking**: Removed `separator()` - use `horizontal_rule()` instead for true HTML-style dividers
  - Migration: Replace `separator()` with `horizontal_rule()`

---

## [0.9.0] - 2025-10-22

### Added

- **📝 Document Content API**: New methods for working with rich document content
  - `get_json_document(document_id)` - Get document JSON content (renamed from `get_document_body`)
  - `replace_json_document(document_id, content)` - Replace with structured content
  - `append_document(document_id, description, files)` - Append plain text
  - `append_json_document(document_id, content)` - Append structured content
  
- **🛠 Document Structure Helpers**: 11 type-safe builder functions for creating rich content
  - Text & paragraphs: `text()`, `paragraph()`, `heading()`
  - Lists: `bullet_list()`, `ordered_list()`, `list_item()`
  - Tables: `table()`, `table_row()`, `table_cell()`
  - Utilities: `link_text()`, `horizontal_rule()`

### Changed

- **🔧 Breaking**: Renamed `get_document_body()` → `get_json_document()` for API consistency
  - Migration: Update `client.get_document_body(id)` to `client.get_json_document(id)`

---

## [0.8.1] - 2025-10-21

### Fixed

- **♻️ Refactor**: Consolidated color models - replaced `SpaceColor` and `MemberColor` with shared `ColorInfo` model

---

## [0.8.0] - 2025-10-21

### Added

- **🏢 Spaces API**: New `get_space(space_id)` method for retrieving space information
- **👥 Members API**: New `get_space_members()` method for listing all space members

### Changed

- **🔧 Breaking**: Renamed `EAvatarMode` → `AvatarMode` for consistency with TypeScript API
  - Migration: Update `from vaiz.models import EAvatarMode` to `from vaiz.models import AvatarMode`

---

## [0.7.3] - 2025-10-21

### Added

- **📝 Document Creation API**: New `create_document()` method for creating documents programmatically

### Models

- **📦 New Request Model**: `CreateDocumentRequest`

## [0.7.2] - 2025-01-20

### Changed

- **🔧 Models**: Enhanced color field types to support both Color enum values and string values for API compatibility
- **✅ Examples**: All code examples now use Color enum for better type safety and IDE support

### Fixed

- **🔧 API Compatibility**: Fixed color validation to accept both enum values and string colors returned by API
- **📝 Documentation**: Removed all references to hex color support in documentation

## [0.7.0] - 2025-10-20

### Breaking Changes

- **✨ Changed Enum Names**: Renamed all enum classes for consistency:
- `EColor` → `Color`
- `EIcon` → `Icon`
- `EKind` → `Kind`
- `EUploadFileType` → `UploadFileType`
- **Migration**: Update imports and usage: `from vaiz.models.enums import Color, Icon, Kind, UploadFileType`

### Added

- **🎨 Color Palette**: Added:
  - `Color.Silver` - silver color
  - `Color.Mint` - mint/cyan color
  - `Color.Lavender` - lavender color

---

## [0.6.0] - 2025-10-20

### Breaking Changes

- **🔗 Renamed Task Connector Fields** for better clarity:
  - `right_connectors` → `blocking` (tasks that this task blocks)
  - `left_connectors` → `blockers` (tasks that block this task)
  - API mapping is automatic - SDK uses intuitive names, API receives technical names
  - **Migration**: Replace `rightConnectors` with `blocking` and `leftConnectors` with `blockers` in your code

### Added

- **🔗 Task Blockers API**: New documentation page explaining blocker relationships
- **📖 Updated Examples**: Updated all code examples with new field names

### Changed

- **Documentation**: Moved from README to dedicated Docusaurus site
- **README**: Simplified to quick start guide with links to full documentation
- **CONTRIBUTING.md**: Moved to project root as standard practice

### Documentation

- Site: https://docs-python-sdk.vaiz.com
- Getting Started: https://docs-python-sdk.vaiz.com/getting-started
- API Reference: https://docs-python-sdk.vaiz.com/api/overview

---

## [0.5.0] - 2025-09-17

### Added

- **📋 New getTasks Method**: Comprehensive task retrieval with filtering and pagination
  - **🔍 Advanced Filtering**: Filter by assignees, board, project, completion status, archived status, parent task, milestones, and specific task IDs
  - **📄 Pagination Support**: Retrieve tasks in pages with `limit` (max 50) and `skip` parameters

### Changed

- **🐛 Fixed Comment Reactions**: Made `native` field optional in `CommentReaction` model to match API behavior
- **⚙️ Modernized Pydantic**: Updated deprecated `class Config:` to modern `model_config = ConfigDict()` syntax

### Technical Details

- **Request Model**: `GetTasksRequest` with comprehensive filtering options
- **Response Models**: `GetTasksResponse` and `GetTasksPayload` for structured data access

### Examples Added

- **📖 `examples/get_tasks.py`**: Comprehensive examples demonstrating all filtering options and pagination

---

## [0.4.10] - 2025-01-27

### Added

- **👤 Profile Model Enhancements**: 
  - Added `EAvatarMode` enum
  - Added new profile fields

### Changed

- **🐍 Python Naming Convention**: All profile model fields now use snake_case naming with proper API aliases

---

## [0.4.9] - 2025-08-26

### Added

- **🔢 New Custom Field Type**: Added `ESTIMATION` field type to `CustomFieldType` enum for project estimation fields
- **🎨 Enhanced Project Colors**: Project `color` field now accepts `Color` enum values for consistent color management

---

## [0.4.8] - 2025-08-12

### Added

- 🧾 Documents API:
  - `get_document_body(document_id)` — get JSON document body
  - `replace_document(document_id, description)` — replace document content (plain text)
  - Task model convenience: `Task.get_task_description(client)`
  - Task model convenience: `Task.update_task_description(client, description)`

---

## [0.4.7] - 2025-01-21

### Added

- **🌐 File Upload from URL**: New `upload_file_from_url()` method for uploading files directly from external URLs
  - **📥 Direct URL Upload**: Upload files without downloading them locally first
  - **🔍 Auto Type Detection**: Automatically detect file types from URL extensions and HTTP content-type headers
  - **📝 Custom Filenames**: Specify custom filenames for uploaded files
  - **🎯 Task Integration**: Complete workflow examples for creating tasks with external files
  - **🛠️ Error Handling**: Robust handling of network issues, invalid URLs, and missing MIME types
  - **🔧 Helper Methods**: Private `_detect_file_type_from_url_and_content()` method for intelligent type detection
  - **📦 Temporary File Management**: Automatic cleanup of temporary files during upload process

### Improved

- **📄 Documentation**: Updated README with comprehensive examples of URL upload functionality
- **🧪 Test Coverage**: Added extensive test suite for URL upload functionality including:
  - Auto-detection tests for different file types
  - Explicit type specification tests
  - Multiple file upload tests
  - Integration tests for task creation with external files
  - Edge case handling for files without extensions
  - Invalid URL error handling tests
- **🎯 Examples**: New example files demonstrating URL upload usage:
  - `examples/upload_file_from_url.py` - Basic URL upload examples
  - `examples/create_task_with_external_file.py` - Task creation with external files

### Technical Details

- **🔗 URL Support**: Supports any publicly accessible HTTP/HTTPS URL
- **📋 File Type Detection**:
  - URL extension matching for common formats (.jpg, .png, .pdf, .mp4, etc.)
  - HTTP Content-Type header analysis
  - Fallback to `UploadFileType.File` for unknown types
- **💾 Memory Efficient**: Streams file downloads to temporary files
- **🧹 Resource Management**: Automatic cleanup of temporary files even on errors
- **🔒 Security**: Respects SSL verification settings from client configuration

### Fixed

- **🏷️ Model Fields**: Made `UploadedFile.mime` field optional to handle API responses that don't include MIME type
- **🌐 URL Reliability**: Replaced unstable external URLs in tests with reliable httpbin.org and w3.org endpoints

## [0.4.6] - 2025-01-21

### Added

- **🎛️ Custom Field Helper Functions**: Complete set of strongly-typed helper functions for creating and managing custom fields
  - **Field creation helpers**: `make_text_field()`, `make_number_field()`, `make_checkbox_field()`, `make_date_field()`, `make_member_field()`, `make_task_relations_field()`, `make_select_field()`, `make_url_field()`
  - **Field editing helpers**: `edit_custom_field_name()`, `edit_custom_field_description()`, `edit_custom_field_visibility()`, `edit_custom_field_complete()`
  - **Select option helpers**: `make_select_option()`, `SelectOption` class for typed option creation
  - **Option management**: `add_board_custom_field_select_option()`, `remove_board_custom_field_select_option()`, `edit_board_custom_field_select_field_option()`
  - **Task relations helpers**: `make_task_relation_value()`, `add_task_relation()`, `remove_task_relation()`
  - **Member field helpers**: `make_member_value()`, `add_member_to_field()`, `remove_member_from_field()`
  - **Date field helpers**: `make_date_value()`, `make_date_range_value()` with datetime support
  - **Value formatting helpers**: `make_text_value()`, `make_number_value()`, `make_checkbox_value()`, `make_url_value()`

### Improved

- **🔧 Enhanced API**: Complete CRUD operations for custom fields with strongly-typed helpers
- **🔗 Relations Management**: Simplified task relationship handling with add/remove functions
- **👥 Member Management**: Easy member assignment with single/multiple member support
- **📅 Date Handling**: Automatic datetime formatting and range support
- **📝 Value Formatting**: Type-safe value preparation for all field types
- **🎨 Better UX**: Automatic ID generation for select options with collision-safe hashing

### Fixed

- **🐛 Model Compatibility**: Made `BoardCustomField.name` optional to match API response behavior
- **✅ Test Stability**: Fixed board custom field tests to handle API response variations

### Technical Details

- All helper functions return properly typed request objects ready for API calls
- All value helpers return properly formatted data for immediate use with CustomField
- Smart member field management maintains appropriate data types (string vs list)
- Date helpers support both datetime objects and ISO strings
- Field editing helpers allow partial updates with optional parameters
- Enhanced EditBoardCustomFieldRequest model with name field support
- Support for both `Color`/`Icon` enums and string values for maximum flexibility
- Helper functions handle option format conversion automatically
- Full backward compatibility with existing custom field APIs

## [0.4.5] - 2025-01-21

### Fixed

- **🔧 Pydantic v2 Compatibility**: Fixed Optional field definitions to use `Field(default=None, alias="...")` instead of `Field(None, alias="...")`
- **🛠️ Linter Issues**: Resolved linter warnings about missing default values for Optional fields
- **📝 Code Quality**: Improved code clarity by using explicit named parameters in Field definitions

### Technical Details

- Follows Pydantic v2 best practices for Optional field definitions

## [0.4.4] - 2025-01-21

### Changed

- **🐍 Unified Python Style**: All SDK models now use Python snake_case convention (`due_start`, `due_end`, `task_id`, `board_id`, etc.)
- **🔄 Backward Compatibility**: Full support for legacy camelCase fields through aliases (`dueStart`, `dueEnd`, `taskId`, `boardId`, etc.)
- **📖 Updated Documentation**: All README examples and documentation now use snake_case style
- **🔧 Enhanced Examples**: All example files updated to demonstrate proper Python conventions
- **✅ Improved Tests**: Fixed test infrastructure and enhanced coverage

### Fixed

- Corrected field aliases for all models to ensure proper API communication

### Technical Details

- Added Field aliases to all models: `Task`, `CreateTaskRequest`, `EditTaskRequest`, board models, etc.
- Updated API methods to use `by_alias=True` where needed for proper camelCase serialization
- Enhanced VaizBaseModel inheritance for consistent field handling
- Maintained 100% test coverage

## [0.4.3] - 2024-06-18

### Changed

- The `kind` field in all models (including `GetHistoryRequest`) now uses the `Kind` enum instead of a string.
- All usages, tests, and documentation updated to use `Kind` (e.g., `Kind.Task`) instead of string values.

### Fixed

- Improved type safety for entity kind selection in history and related APIs.

## [0.4.2] - 2024-06-17

### Added

- New `get_history` method for retrieving history of tasks and other entities
- Models: `GetHistoryRequest`, `GetHistoryResponse`, `HistoryItem`, `HistoryData`
- Enum: `Kind` for supported entity types (Space, Project, Task, Document, Board, Milestone)
- Usage example: `examples/get_history.py`
- Tests for the new method

### Changed

- All models and API now use `Kind` enum for the `kind` field instead of string
- All usages, tests, and documentation updated to use `Kind` (e.g., `Kind.Task`) instead of string values

### Fixed

- Fixed aliases and types for file and task models
- Improved environment variable handling in examples

## [0.4.1] - 2024-06-16

### Changed

- Improved datetime support in all models
- Updated examples and tests for new models

## [0.4.0] - 2024-06-16

### Added

- Full comment system: create, edit, delete comments, reactions, attachments
- Automatic datetime conversion in all models
- New examples and documentation for working with dates

### Breaking Changes

- All date fields now return `datetime` objects instead of strings
- All models now inherit from `VaizBaseModel` for datetime support
