---
sidebar_position: 3
sidebar_label: Comments
title: Comments API — Manage Comments, Replies & Reactions | Vaiz Python SDK
description: Learn how to use the Vaiz Python SDK to manage comments, replies, and reactions in your Vaiz projects. Includes examples, endpoints, and usage patterns.
---

# Comments

Complete reference for comment-related methods and models.

## Methods

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

## Models

### Comment

Main comment model representing a comment in the system.

```python
class Comment:
    id: str                             # Comment ID
    content: str                        # HTML content
    author_id: str                      # Author user ID
    document_id: str                    # Document ID
    created_at: datetime                # Creation timestamp
    updated_at: datetime                # Last update timestamp
    edited_at: Optional[datetime]       # Edit timestamp
    deleted_at: Optional[datetime]      # Deletion timestamp
    reply_to: Optional[str]             # Parent comment ID
    files: List[UploadedFile]           # Attached files
    reactions: List[CommentReaction]    # Reactions
    has_removed_files: bool             # Whether files were removed
```

---

### CommentReaction

```python
class CommentReaction:
    reaction_db_id: str                 # Reaction database ID
    emoji_id: str                       # Emoji ID
    native: Optional[str]               # Emoji character
    member_ids: List[str]               # Members who reacted
```

---

## Request Models

### PostCommentRequest

```python
class PostCommentRequest:
    document_id: str                    # Required - Document ID
    content: str                        # Required - Comment content (HTML)
    file_ids: List[str]                 # File IDs to attach
    reply_to: Optional[str]             # Parent comment ID for replies
```

---

### GetCommentsRequest

```python
class GetCommentsRequest:
    document_id: str                    # Required - Document ID
```

---

### EditCommentRequest

```python
class EditCommentRequest:
    comment_id: str                     # Required - Comment ID
    content: str                        # Required - New comment content (HTML)
    add_file_ids: List[str]             # File IDs to add
    order_file_ids: List[str]           # Order of file IDs
    remove_file_ids: List[str]          # File IDs to remove
```

---

### DeleteCommentRequest

```python
class DeleteCommentRequest:
    comment_id: str                     # Required - Comment ID to delete
```

---

### ReactToCommentRequest

```python
class ReactToCommentRequest:
    comment_id: str                     # Required - Comment ID
    id: str                             # Required - Emoji ID (e.g., "kissing_smiling_eyes")
    name: str                           # Required - Human readable name
    native: str                         # Required - Emoji character (e.g., "😙")
    unified: str                        # Required - Unicode codepoint (e.g., "1f619")
    keywords: List[str]                 # Keywords for the emoji
    shortcodes: str                     # Required - Shortcode (e.g., ":kissing_smiling_eyes:")
```

---

## Response Models

### PostCommentResponse

```python
class PostCommentResponse:
    type: str                           # Response type ("PostComment")
    payload: Dict[str, Comment]         # Response payload
    
    @property
    def comment(self) -> Comment:      # Convenience property
        ...
```

---

### GetCommentsResponse

```python
class GetCommentsResponse:
    type: str                           # Response type ("GetComments")
    payload: Dict[str, List[Comment]]   # Response payload
    
    @property
    def comments(self) -> List[Comment]:  # Convenience property
        ...
```

---

### EditCommentResponse

```python
class EditCommentResponse:
    type: str                           # Response type ("EditComment")
    payload: Dict[str, Comment]         # Response payload
    
    @property
    def comment(self) -> Comment:      # Convenience property
        ...
```

---

### DeleteCommentResponse

```python
class DeleteCommentResponse:
    type: str                           # Response type ("DeleteComment")
    payload: Dict[str, Comment]         # Response payload
    
    @property
    def comment(self) -> Comment:      # Convenience property
        ...
```

---

### ReactToCommentResponse

```python
class ReactToCommentResponse:
    type: str                           # Response type ("ReactToComment")
    payload: Dict[str, List[CommentReaction]]  # Response payload
    
    @property
    def reactions(self) -> List[CommentReaction]:  # Convenience property
        ...
```

---

## See Also

- [Comments Guide](../guides/comments) - Usage examples and patterns
- [Enums](./enums) - CommentReactionType and other enums
- [Files](./files) - File attachment methods

