# Changelog

## [0.4.3] - 2024-06-XX
### Changed
- The `kind` field in all models (including `GetHistoryRequest`) now uses the `EKind` enum instead of a string.
- All usages, tests, and documentation updated to use `EKind` (e.g., `EKind.Task`) instead of string values.

### Fixed
- Improved type safety for entity kind selection in history and related APIs.

## [0.4.2] - 2024-06-XX
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

## [0.4.1] - 2024-06-XX
### Changed
- Improved datetime support in all models
- Updated examples and tests for new models

## [0.4.0] - 2024-06-XX
### Added
- Full comment system: create, edit, delete comments, reactions, attachments
- Automatic datetime conversion in all models
- New examples and documentation for working with dates

### Breaking Changes
- All date fields now return `datetime` objects instead of strings
- All models now inherit from `VaizBaseModel` for datetime support 