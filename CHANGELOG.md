# Changelog

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
- **🎨 Enhanced Project Colors**: Project `color` field now accepts both hex color codes (e.g., `#1F36AD`) and `EColor` enum values for maximum flexibility

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
  - Fallback to `EUploadFileType.File` for unknown types
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
- Support for both `EColor`/`EIcon` enums and string values for maximum flexibility
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

- The `kind` field in all models (including `GetHistoryRequest`) now uses the `EKind` enum instead of a string.
- All usages, tests, and documentation updated to use `EKind` (e.g., `EKind.Task`) instead of string values.

### Fixed

- Improved type safety for entity kind selection in history and related APIs.

## [0.4.2] - 2024-06-17

### Added

- New `get_history` method for retrieving history of tasks and other entities
- Models: `GetHistoryRequest`, `GetHistoryResponse`, `HistoryItem`, `HistoryData`
- Enum: `EKind` for supported entity types (Space, Project, Task, Document, Board, Milestone)
- Usage example: `examples/get_history.py`
- Tests for the new method

### Changed

- All models and API now use `EKind` enum for the `kind` field instead of string
- All usages, tests, and documentation updated to use `EKind` (e.g., `EKind.Task`) instead of string values

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
