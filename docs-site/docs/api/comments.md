---
sidebar_position: 3
---

# Comments

Working with comments, replies, and reactions.

## Creating Comments

### Simple Comment

```python
response = client.post_comment(
    document_id="document_id",
    content="<p>My comment</p>"
)

comment = response.comment
print(f"Created: {comment.id}")
```

### Comment with HTML

```python
html = """
<p>Comment with <strong>bold</strong> and <em>italic</em></p>
<ul>
  <li>Item 1</li>
  <li>Item 2</li>
</ul>
"""

response = client.post_comment(
    document_id="document_id",
    content=html
)
```

### Comment with Files

```python
from vaiz.models.enums import UploadFileType

# Upload files
img = client.upload_file("screenshot.png", EUploadFileType.Image)
doc = client.upload_file("report.pdf", EUploadFileType.Pdf)

# Post comment
response = client.post_comment(
    document_id="document_id",
    content="<p>Files attached</p>",
    file_ids=[img.file.id, doc.file.id]
)
```

## Replies

```python
# Original comment
original = client.post_comment(
    document_id="document_id",
    content="<p>Original</p>"
)

# Reply
reply = client.post_comment(
    document_id="document_id",
    content="<p>Reply</p>",
    reply_to=original.comment.id
)
```

## Reactions

### Quick Reactions

```python
from vaiz.models import CommentReactionType

client.add_reaction(
    comment_id="comment_id",
    reaction=CommentReactionType.THUMBS_UP
)
```

### Available Reactions

- `CommentReactionType.THUMBS_UP` - 👍
- `CommentReactionType.HEART` - ❤️
- `CommentReactionType.LAUGHING` - 😂
- `CommentReactionType.WOW` - 😮
- `CommentReactionType.CRYING` - 😢
- `CommentReactionType.ANGRY` - 😡
- `CommentReactionType.PARTY` - 🎉

## Editing Comments

```python
response = client.edit_comment(
    comment_id="comment_id",
    content="<p>Updated content</p>"
)
```

### Managing Files

```python
# Add files
client.edit_comment(
    comment_id="comment_id",
    add_file_ids=["new_file_id"]
)

# Remove files
client.edit_comment(
    comment_id="comment_id",
    remove_file_ids=["file_id"]
)
```

## Deleting Comments

```python
response = client.delete_comment(comment_id="comment_id")
print(f"Deleted: {response.comment.deleted_at}")
```

## Getting Comments

```python
response = client.get_comments(document_id="document_id")

for comment in response.comments:
    print(f"Author: {comment.author_id}")
    print(f"Content: {comment.content}")
    if comment.reply_to:
        print(f"  Reply to: {comment.reply_to}")
```

## Getting document_id

```python
# From task
task_response = client.get_task("PRJ-123")
document_id = task_response.payload["task"]["document"]

# When creating task
task = CreateTaskRequest(name="Task", board="...", group="...")
response = client.create_task(task)
document_id = response.task.document
```

## See Also

- [Tasks API](./tasks)
- [Files API](./files)
- [Examples](../examples)

