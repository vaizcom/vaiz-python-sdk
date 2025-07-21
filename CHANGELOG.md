# Changelog

## [0.4.4] - 2025-01-21

### Changed

- **🐍 Unified Python Style**: All SDK models now use Python snake_case convention (`due_start`, `due_end`, `task_id`, `board_id`, etc.)
- **🔄 Backward Compatibility**: Full support for legacy camelCase fields through aliases (`dueStart`, `dueEnd`, `taskId`, `boardId`, etc.)
- **📖 Updated Documentation**: All README examples and documentation now use snake_case style
- **🔧 Enhanced Examples**: All example files updated to demonstrate proper Python conventions
- **✅ Improved Tests**: Fixed test infrastructure and enhanced coverage

### Fixed

- Fixed API serialization in board operations (now properly sends camelCase to API)
- Fixed missing client fixture in board type creation test
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
