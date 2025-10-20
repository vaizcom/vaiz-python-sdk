# Known Issues and Future Tasks

This document tracks known inconsistencies between the Python SDK, documentation, and the shared backend contracts. These issues should be addressed in future releases to ensure full compatibility and feature parity.

## Icon Enumeration Inconsistencies

**Issue:** The SDK defines `Icon.Percent25` and `Icon.Percent50` in `vaiz.models.enums.Icon`, but these constants are not present in the shared `EStylerIcon` type. This may cause discrepancies when selecting icons through the SDK.

**Task:**
- [ ] Verify which icon values are actually supported by the backend
- [ ] Either remove `Icon.Percent25` and `Icon.Percent50` from the SDK if not supported, or add them to the shared types
- [ ] Update documentation to reflect the accurate list of supported icons

---

## CreateTaskRequest: Unnecessary Project Requirement

**Issue:** Both documentation and SDK require `project` as a mandatory field in `CreateTaskRequest`, but the backend's `CreateTaskInputDto` does not include project in the payload—it is computed from `boardId` on the server side. This forces users to provide an unnecessary parameter.

**Task:**
- [ ] Remove `project` as a required field from `CreateTaskRequest` model
- [ ] Update documentation to reflect that `project` is optional or not needed
- [ ] Add migration notes if this is a breaking change
- [ ] Verify that tasks can be created without explicitly specifying project

---

## GetTasksRequest: Limited Filtering Options

**Issue:** The `GetTasksRequest` in both documentation and SDK only supports basic filters, while the backend's `GetTasksInputDto` provides filtering by assignee, dates, archive status, sorting, and connector operations. These powerful filtering capabilities are unavailable to Python SDK users.

**Task:**
- [ ] Extend `GetTasksRequest` model to include all backend-supported filters:
  - Assignee filtering
  - Date range filtering
  - Archive status filtering
  - Custom sorting options
  - Connector operations
- [ ] Update the `get_tasks` method to accept and forward these parameters
- [ ] Add comprehensive documentation with examples for advanced filtering
- [ ] Add tests for new filtering capabilities

---

## GetHistoryRequest: Missing Filter Parameters

**Issue:** `GetHistoryRequest` is documented and implemented with only four fields, but the shared contract allows filtering by authors, date ranges, keys, task lists, and groups. These options are missing from both SDK and documentation.

**Task:**
- [ ] Extend `GetHistoryRequest` to support:
  - Author filtering
  - Date range filtering
  - Key-based filtering
  - Task list filtering
  - Group filtering
- [ ] Update history-related methods to accept new parameters
- [ ] Document all available history filtering options
- [ ] Add examples demonstrating advanced history queries

---

## Comment Reactions: Excessive Metadata Requirements

**Issue:** The `react_to_comment` method is documented as requiring full emoji metadata, and the SDK sends complete emoji objects. However, the backend contract only expects `commentId`, `id`, and `shortcodes`. The extra fields in documentation and model are misleading and add unnecessary complexity.

**Task:**
- [ ] Simplify the reaction model to only include required fields:
  - `commentId`
  - `id`
  - `shortcodes`
- [ ] Update `react_to_comment` method to send minimal required data
- [ ] Update documentation to reflect the simplified interface
- [ ] Ensure backward compatibility if needed

---

## File Models: Incomplete and Incorrect Attributes

**Issue:** The `UploadedFile` and `TaskFile` models in documentation list only basic attributes and incorrectly type `dimension` as `dict` instead of a list. The actual shared types include an extended set of attributes such as `dominantColor`, `owner`, `accessKind`, etc.

**Task:**
- [ ] Update `UploadedFile` model to include all attributes from shared types:
  - `dominantColor`
  - `owner`
  - `accessKind`
  - Other missing fields
- [ ] Fix `dimension` type from `dict` to correct type (likely `list` or specific dimension type)
- [ ] Update `TaskFile` model with complete attributes
- [ ] Document all file-related fields with descriptions and examples
- [ ] Add type hints and validation for file models

---

## Milestone Model: Field Inconsistencies and Missing Filters

**Issue:** Documentation and SDK add `tags`, `color`, `is_active`, and `is_completed` fields to the Milestone model, but the shared types don't support these. Additionally, the `get_milestones` method doesn't allow filtering by `boardId`/`projectId` as provided in the backend contract.

**Task:**
- [ ] Verify which milestone fields are actually supported by backend:
  - Remove unsupported fields (`tags`, `color`, `is_active`, `is_completed`) if not in shared types
  - Or add them to shared types if they should be supported
- [ ] Extend `get_milestones` method to support filtering by:
  - `boardId`
  - `projectId`
- [ ] Update documentation to accurately reflect milestone model structure
- [ ] Add examples for filtering milestones by board and project
- [ ] Add tests for milestone filtering functionality

---

## General Recommendations

### Alignment Strategy
- [ ] Conduct a comprehensive audit of all SDK models against shared backend contracts
- [ ] Establish a process for keeping SDK types in sync with backend changes
- [ ] Consider auto-generating SDK models from shared types where possible
- [ ] Set up validation tests that compare SDK types with backend contracts

### Documentation Improvements
- [ ] Review all API documentation for accuracy against actual backend behavior
- [ ] Add a "Differences from Backend" section for transparency
- [ ] Include more complete examples showing all available options
- [ ] Document any intentional simplifications or abstractions

### Testing and Validation
- [ ] Add integration tests that verify SDK requests match backend expectations
- [ ] Set up CI/CD checks to catch type mismatches early
- [ ] Create test cases for all filtering and querying options
- [ ] Validate that optional fields are truly optional

---

## Priority Levels

**High Priority:**
- GetTasksRequest filtering options (impacts usability significantly)
- CreateTaskRequest project requirement (causes confusion)
- File models type correctness (may cause runtime errors)

**Medium Priority:**
- GetHistoryRequest filtering options
- Milestone filtering capabilities
- Icon enumeration alignment

**Low Priority:**
- Comment reaction metadata simplification (works but suboptimal)

---

*Last Updated: 2025-10-20*

