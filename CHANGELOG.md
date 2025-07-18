# Changelog

## [0.4.2] - 2024-06-XX
### Added
- New `get_history` method for retrieving history of tasks and other entities
- Models: `GetHistoryRequest`, `GetHistoryResponse`, `HistoryItem`, `HistoryData`
- Usage example: `examples/get_history.py`
- Tests for the new method

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