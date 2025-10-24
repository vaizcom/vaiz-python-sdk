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

## Enum Naming Inconsistency

**Issue:** The `CommentReactionType` and `CustomFieldType` enums use SCREAMING_SNAKE_CASE for their members (e.g., `THUMBS_UP`, `TEXT`, `TASK_RELATIONS`), while all other enums in the SDK follow PascalCase convention (e.g., `Icon.Square`, `Color.Red`, `Kind.Task`, `UploadFileType.Image`). This inconsistency creates a confusing developer experience.

**Current State:**
```python
# Inconsistent - SCREAMING_SNAKE_CASE
class CommentReactionType(Enum):
    THUMBS_UP = "thumbs_up"
    HEART = "heart"
    LAUGHING = "joy"
    # ...

class CustomFieldType(str, Enum):
    TEXT = "Text"
    NUMBER = "Number"
    CHECKBOX = "Checkbox"
    TASK_RELATIONS = "TaskRelations"
    # ...
```

**Expected State:**
```python
# Consistent - PascalCase
class CommentReactionType(Enum):
    ThumbsUp = "thumbs_up"
    Heart = "heart"
    Laughing = "joy"
    # ...

class CustomFieldType(str, Enum):
    Text = "Text"
    Number = "Number"
    Checkbox = "Checkbox"
    TaskRelations = "TaskRelations"
    # ...
```

**Task:**
- [ ] Rename `CommentReactionType` enum members to PascalCase:
  - `THUMBS_UP` → `ThumbsUp`
  - `HEART` → `Heart`
  - `LAUGHING` → `Laughing`
  - `WOW` → `Wow`
  - `CRYING` → `Crying`
  - `ANGRY` → `Angry`
  - `PARTY` → `Party`
- [ ] Rename `CustomFieldType` enum members to PascalCase:
  - `TEXT` → `Text`
  - `NUMBER` → `Number`
  - `CHECKBOX` → `Checkbox`
  - `DATE` → `Date`
  - `MEMBER` → `Member`
  - `TASK_RELATIONS` → `TaskRelations`
  - `SELECT` → `Select`
  - `URL` → `Url`
  - `ESTIMATION` → `Estimation`
- [ ] Update all references in code, tests, and examples
- [ ] Update documentation with migration guide
- [ ] Update `COMMENT_REACTION_METADATA` dictionary keys to use new enum members
- [ ] Add deprecation warnings for old names (if backward compatibility is needed)
- [ ] Add this as a breaking change in CHANGELOG

---

## Task Group Movement: taskOrderByGroups Not Updated

**Issue:** When changing a task's `group` field via `edit_task` API, the backend updates the task's `group` property but does not update the `taskOrderByGroups` dictionary on the board. This causes a discrepancy where:
- The API returns the task with the new `group` value
- The UI displays the task in the old group (based on `taskOrderByGroups`)
- Task appears "orphaned" - has correct group in settings but wrong position on board

**Example:**
```python
# Task PRJ-2 moved from Backlog to Todo
client.edit_task(EditTaskRequest(task_id="...", group=todo_group_id))

# After edit:
task.group == todo_group_id  # ✅ Correct
board.task_order_by_groups[todo_group_id]  # ❌ Task not in this list
board.task_order_by_groups[backlog_group_id]  # ❌ Task still in old list
```

**Root Cause:** Backend's `editTask` endpoint does not automatically update the board's `taskOrderByGroups` field when task group changes.

**Impact:**
- Users see tasks in wrong columns in UI
- Task appears in one group in settings but another group on board
- Breaks visual workflow - users lose track of task positions
- SDK tests pass but UI shows incorrect state

**Task:**
- [ ] **Backend Fix (Primary):** Update `editTask` endpoint to automatically:
  - Remove task ID from old group in `taskOrderByGroups`
  - Add task ID to new group in `taskOrderByGroups`
  - Or provide separate API endpoint to update task order
- [ ] Document this limitation in SDK until backend is fixed
- [ ] Add warning in SDK documentation about group movement
- [ ] Consider adding workaround helper in SDK if backend fix is not feasible

**Workaround:**
Currently no SDK-level workaround exists as there's no API endpoint to manually update `taskOrderByGroups`. Users must manually move tasks in UI after API edit, or wait for backend fix.

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

**Critical Priority:**
- Task Group Movement taskOrderByGroups issue (breaks UI-API consistency, high user impact)

**High Priority:**
- GetTasksRequest filtering options (impacts usability significantly)
- CreateTaskRequest project requirement (causes confusion)
- File models type correctness (may cause runtime errors)
- Enum naming inconsistency (affects developer experience and code consistency)

**Medium Priority:**
- GetHistoryRequest filtering options
- Milestone filtering capabilities
- Icon enumeration alignment

**Low Priority:**
- Comment reaction metadata simplification (works but suboptimal)

---

*Last Updated: 2025-10-24*

