---
sidebar_position: 2
---

# Methods & Enums

Complete reference of all SDK methods and enums.

## Tasks

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
- `task` - Task configuration (name, board, group, project required)
- `description` - Optional task description
- `file` - Optional file to upload and attach

**Returns:** `TaskResponse` with created task

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

## Comments

### `post_comment`

```python
post_comment(
    document_id: str,
    content: str,
    file_ids: List[str] = None,
    reply_to: str = None
) -> PostCommentResponse
```

Post a comment to a document.

**Parameters:**
- `document_id` - Document ID to comment on
- `content` - Comment content (HTML supported)
- `file_ids` - Optional list of file IDs to attach
- `reply_to` - Optional parent comment ID for replies

**Returns:** `PostCommentResponse` with created comment

---

### `get_comments`

```python
get_comments(document_id: str) -> GetCommentsResponse
```

Get all comments for a document.

**Parameters:**
- `document_id` - Document ID

**Returns:** `GetCommentsResponse` with list of comments

---

### `edit_comment`

```python
edit_comment(
    comment_id: str,
    content: str,
    add_file_ids: List[str] = None,
    order_file_ids: List[str] = None,
    remove_file_ids: List[str] = None
) -> EditCommentResponse
```

Edit comment content and manage files.

**Parameters:**
- `comment_id` - Comment ID to edit
- `content` - New content
- `add_file_ids` - Files to add
- `order_file_ids` - New file order
- `remove_file_ids` - Files to remove

**Returns:** `EditCommentResponse` with updated comment

---

### `delete_comment`

```python
delete_comment(comment_id: str) -> DeleteCommentResponse
```

Soft delete a comment.

**Parameters:**
- `comment_id` - Comment ID to delete

**Returns:** `DeleteCommentResponse` with deleted comment

---

### `add_reaction`

```python
add_reaction(
    comment_id: str,
    reaction: CommentReactionType
) -> ReactToCommentResponse
```

Add a popular emoji reaction.

**Parameters:**
- `comment_id` - Comment ID
- `reaction` - Reaction type (THUMBS_UP, HEART, etc.)

**Returns:** `ReactToCommentResponse` with reactions

---

### `react_to_comment`

```python
react_to_comment(
    comment_id: str,
    emoji_id: str,
    emoji_name: str,
    emoji_native: str,
    emoji_unified: str,
    emoji_keywords: List[str] = None,
    emoji_shortcodes: str = None
) -> ReactToCommentResponse
```

Add custom emoji reaction.

**Parameters:**
- `comment_id` - Comment ID
- `emoji_id` - Emoji identifier
- `emoji_name` - Human-readable name
- `emoji_native` - Emoji character (e.g., "😙")
- `emoji_unified` - Unicode code (e.g., "1f619")
- `emoji_keywords` - Search keywords
- `emoji_shortcodes` - Shortcode (e.g., ":smile:")

**Returns:** `ReactToCommentResponse` with reactions

---

## Files

### `upload_file`

```python
upload_file(
    file_path: str,
    file_type: EUploadFileType
) -> UploadFileResponse
```

Upload a file from local disk.

**Parameters:**
- `file_path` - Path to file
- `file_type` - File type (Image, Video, Pdf, File)

**Returns:** `UploadFileResponse` with uploaded file info

---

### `upload_file_from_url`

```python
upload_file_from_url(
    file_url: str,
    file_type: EUploadFileType = None,
    filename: str = None
) -> UploadFileResponse
```

Upload a file from URL.

**Parameters:**
- `file_url` - URL of file to download
- `file_type` - Optional file type (auto-detected if not provided)
- `filename` - Optional custom filename

**Returns:** `UploadFileResponse` with uploaded file info

---

## Milestones

### `get_milestones`

```python
get_milestones() -> MilestonesResponse
```

Get all milestones in current space.

**Returns:** `MilestonesResponse` with list of milestones

---

### `get_milestone`

```python
get_milestone(milestone_id: str) -> GetMilestoneResponse
```

Get a single milestone by ID.

**Parameters:**
- `milestone_id` - Milestone ID

**Returns:** `GetMilestoneResponse` with milestone data

---

### `create_milestone`

```python
create_milestone(request: CreateMilestoneRequest) -> CreateMilestoneResponse
```

Create a new milestone.

**Parameters:**
- `request` - Milestone configuration (name, board, project required)

**Returns:** `CreateMilestoneResponse` with created milestone

---

### `edit_milestone`

```python
edit_milestone(request: EditMilestoneRequest) -> EditMilestoneResponse
```

Edit an existing milestone.

**Parameters:**
- `request` - Edit request with milestone_id and fields to update

**Returns:** `EditMilestoneResponse` with updated milestone

---

### `toggle_milestone`

```python
toggle_milestone(request: ToggleMilestoneRequest) -> ToggleMilestoneResponse
```

Attach/detach milestones to/from a task.

**Parameters:**
- `request` - Task ID and milestone IDs to toggle

**Returns:** `ToggleMilestoneResponse` with updated task

---

## Boards

### `get_boards`

```python
get_boards() -> BoardsResponse
```

Get all boards in current space.

**Returns:** `BoardsResponse` with list of boards

---

### `get_board`

```python
get_board(board_id: str) -> BoardResponse
```

Get a single board by ID.

**Parameters:**
- `board_id` - Board ID

**Returns:** `BoardResponse` with board data

---

### `create_board_type`

```python
create_board_type(request: CreateBoardTypeRequest) -> CreateBoardTypeResponse
```

Create a new board type (e.g., Bug, Feature).

**Parameters:**
- `request` - Type configuration (board_id, label, icon, color)

**Returns:** `CreateBoardTypeResponse` with created type

---

### `edit_board_type`

```python
edit_board_type(request: EditBoardTypeRequest) -> EditBoardTypeResponse
```

Edit an existing board type.

**Parameters:**
- `request` - Edit request with board_type_id and fields to update

**Returns:** `EditBoardTypeResponse` with updated type

---

### `create_board_group`

```python
create_board_group(request: CreateBoardGroupRequest) -> CreateBoardGroupResponse
```

Create a new board group (column).

**Parameters:**
- `request` - Group configuration (name, board_id)

**Returns:** `CreateBoardGroupResponse` with all board groups

---

### `edit_board_group`

```python
edit_board_group(request: EditBoardGroupRequest) -> EditBoardGroupResponse
```

Edit an existing board group.

**Parameters:**
- `request` - Edit request with board_group_id and fields to update

**Returns:** `EditBoardGroupResponse` with all board groups

---

### `create_board_custom_field`

```python
create_board_custom_field(request: CreateBoardCustomFieldRequest) -> CreateBoardCustomFieldResponse
```

Create a custom field on a board.

**Parameters:**
- `request` - Field configuration (use helper functions like `make_text_field`)

**Returns:** `CreateBoardCustomFieldResponse` with created field

---

### `edit_board_custom_field`

```python
edit_board_custom_field(request: EditBoardCustomFieldRequest) -> EditBoardCustomFieldResponse
```

Edit an existing custom field.

**Parameters:**
- `request` - Edit request (use helper functions like `edit_custom_field_name`)

**Returns:** `EditBoardCustomFieldResponse` with updated field

---

## Projects

### `get_projects`

```python
get_projects() -> ProjectsResponse
```

Get all projects in current space.

**Returns:** `ProjectsResponse` with list of projects

---

### `get_project`

```python
get_project(project_id: str) -> ProjectResponse
```

Get a single project by ID.

**Parameters:**
- `project_id` - Project ID

**Returns:** `ProjectResponse` with project data

---

## Profile

### `get_profile`

```python
get_profile() -> ProfileResponse
```

Get current user's profile information.

**Returns:** `ProfileResponse` with user data

---

## Documents

### `get_document_body`

```python
get_document_body(document_id: str) -> Dict[str, Any]
```

Get document content as JSON.

**Parameters:**
- `document_id` - Document ID

**Returns:** Dictionary with document JSON structure

---

### `replace_document`

```python
replace_document(
    document_id: str,
    description: str
) -> ReplaceDocumentResponse
```

Replace document content completely.

**Parameters:**
- `document_id` - Document ID
- `description` - New content (plain text)

**Returns:** `ReplaceDocumentResponse`

---

## History

### `get_history`

```python
get_history(request: GetHistoryRequest) -> GetHistoryResponse
```

Get change history for an entity.

**Parameters:**
- `request` - History request (kind, kindId, optional filters)

**Returns:** `GetHistoryResponse` with list of history events

---

### `clear_tasks_cache`

```python
clear_tasks_cache() -> None
```

Clear the get_tasks() cache manually.

---

## Enums

### TaskPriority

```python
TaskPriority.None_     # 0 - No priority
TaskPriority.General   # 1 - General (default)
TaskPriority.Medium    # 2 - Medium
TaskPriority.High      # 3 - High
```

### EUploadFileType

```python
EUploadFileType.Image    # Image files (shows preview)
EUploadFileType.Video    # Video files (shows player)
EUploadFileType.Pdf      # PDF files (shows viewer)
EUploadFileType.File     # Generic files (download link)
```

### CommentReactionType

```python
CommentReactionType.THUMBS_UP    # 👍
CommentReactionType.HEART        # ❤️
CommentReactionType.LAUGHING     # 😂
CommentReactionType.WOW          # 😮
CommentReactionType.CRYING       # 😢
CommentReactionType.ANGRY        # 😡
CommentReactionType.PARTY        # 🎉
```

### EIcon

All available icons (200+ options):

```python
from vaiz.models.enums import EIcon

# Shapes
EIcon.Cursor, EIcon.Square, EIcon.Hexagon, EIcon.Rhombus, EIcon.Triangle
EIcon.Checkbox, EIcon.Diamonds, EIcon.Circle

# UI & Interface
EIcon.Light, EIcon.Search, EIcon.Stop, EIcon.User, EIcon.People
EIcon.UserGroup2, EIcon.ConnectedPeople, EIcon.Col, EIcon.Code, EIcon.Todo
EIcon.Board, EIcon.Document, EIcon.Project

# Science & Tech
EIcon.Air, EIcon.Atom, EIcon.Molecule, EIcon.Battery, EIcon.BatteryCharging
EIcon.BatteryLevel, EIcon.BenzeneRing, EIcon.BGRemover

# Objects & Items
EIcon.Barcode, EIcon.QR, EIcon.Basilica, EIcon.Basketball, EIcon.Binoculars
EIcon.BlackHat, EIcon.Hat, EIcon.Bot, EIcon.Broom, EIcon.CampingChair
EIcon.Cable, EIcon.Terminal, EIcon.Rs232Female, EIcon.CD

# Music & Media
EIcon.Music, EIcon.Music2, EIcon.MusicPlaylist, EIcon.Video, EIcon.Play
EIcon.Camera, EIcon.Camera2, EIcon.Aperture, EIcon.Image

# Time & Actions
EIcon.Clock, EIcon.Watch, EIcon.Tenses, EIcon.Voicemail, EIcon.WatchesFrontView
EIcon.WeddingRings, EIcon.List, EIcon.Restart, EIcon.Swap, EIcon.Target

# Weather & Nature
EIcon.Moon, EIcon.Sun, EIcon.Cloud, EIcon.Snow, EIcon.Fire, EIcon.Drop

# Medical & Health
EIcon.DoctorsBag, EIcon.Hospital, EIcon.MedicalDoctor

# Work & Education
EIcon.ELearning, EIcon.Laptop, EIcon.FanSpeed, EIcon.MindMap, EIcon.Mirror
EIcon.Attach, EIcon.Table, EIcon.Chart, EIcon.Broadcast

# Achievement & Status
EIcon.Flag, EIcon.Finish, EIcon.Crown, EIcon.Money, EIcon.Coins
EIcon.Shield, EIcon.Trophy, EIcon.Star

# Characters & People
EIcon.WomanHead, EIcon.Knight

# Animals & Creatures
EIcon.Bug, EIcon.Bird, EIcon.PeacePigeon, EIcon.Penguin, EIcon.Fish
EIcon.Alien, EIcon.Panda, EIcon.Cat, EIcon.Dog, EIcon.Unicorn

# Sports & Activities
EIcon.Run, EIcon.Swimming, EIcon.Ball

# Location & Navigation
EIcon.Geography, EIcon.Planet, EIcon.Location, EIcon.Navigate

# Vehicles & Transportation
EIcon.Stormtrooper, EIcon.SpaceFighter, EIcon.Submarine, EIcon.Plane
EIcon.Ship, EIcon.ShipWheel, EIcon.Lifebuoy, EIcon.Launch, EIcon.Car
EIcon.BikePath, EIcon.Cycling, EIcon.MotorbikeHelmet, EIcon.Road

# Communication & Tech
EIcon.GpsSignal, EIcon.Radio, EIcon.InternetAntenna, EIcon.Satellites
EIcon.Satellite, EIcon.Speed, EIcon.Info, EIcon.Help, EIcon.Quote
EIcon.Attention, EIcon.Phone, EIcon.Email, EIcon.Mail, EIcon.Message
EIcon.Chat, EIcon.Sound

# Editing & Content
EIcon.Rename, EIcon.New, EIcon.Add, EIcon.Delete, EIcon.Type, EIcon.Asterisk
EIcon.Thumb, EIcon.Percent, EIcon.Percent25, EIcon.Percent50

# Food & Drink
EIcon.Coffee, EIcon.Beer, EIcon.Champagne, EIcon.WineGlass, EIcon.Cocktail
EIcon.Plate

# Misc & Fun
EIcon.Heart, EIcon.Link, EIcon.Happy, EIcon.Layers, EIcon.Apps, EIcon.Up
EIcon.Lab, EIcon.Cancel, EIcon.Poo, EIcon.Skull, EIcon.Bone, EIcon.Dice
EIcon.Puzzle, EIcon.Bang, EIcon.Explosion, EIcon.Gun, EIcon.Shower
EIcon.SpaFlower, EIcon.FoamBubbles, EIcon.Galaxy, EIcon.Bookmark, EIcon.Book
EIcon.Sent, EIcon.Home, EIcon.MarkerPen, EIcon.Illustrator, EIcon.Paint
EIcon.Paint2, EIcon.Gear, EIcon.BoxClose

# Greek Letters
EIcon.Alpha, EIcon.Beta, EIcon.Gamma, EIcon.Lambda, EIcon.Mu
EIcon.Omega, EIcon.Pi, EIcon.Sigma

# Field Type Icons
EIcon.TypeText, EIcon.TypeNumber, EIcon.TypeDate, EIcon.TypeCheck, EIcon.TypeUser
```

### EColor

All available colors:

```python
from vaiz.models.enums import EColor

# Available Colors
EColor.Red, EColor.Orange, EColor.Gold, EColor.Olive, EColor.Green
EColor.Cyan, EColor.Blue, EColor.Violet, EColor.Magenta, EColor.Rose
```

### EKind

Entity types for history:

```python
from vaiz.models.enums import EKind

# Entity types
EKind.Task, EKind.Project, EKind.Board, EKind.Document, EKind.Milestone
```

### CustomFieldType

All custom field types:

```python
from vaiz.models.enums import CustomFieldType

CustomFieldType.TEXT            # Text input field
CustomFieldType.NUMBER          # Number input field
CustomFieldType.CHECKBOX        # Checkbox field
CustomFieldType.DATE            # Date picker field
CustomFieldType.MEMBER          # User selector field
CustomFieldType.TASK_RELATIONS  # Task relations field
CustomFieldType.SELECT          # Dropdown select field
CustomFieldType.URL             # URL input field
CustomFieldType.ESTIMATION      # Time estimation field
```

