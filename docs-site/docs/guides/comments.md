---
sidebar_position: 3
sidebar_label: Comments
title: Working with Comments — Post, Reply & React | Vaiz Python SDK
description: Learn how to create comments, replies, and manage reactions in your Vaiz projects using the Python SDK. Includes Markdown formatting and file attachments.
---

# Comments

Working with comments, replies, and reactions.

Markdown is the recommended way to write comment content — it is converted to rich comment blocks on the server. HTML `content` remains supported as the legacy format. `markdown` and `content` are mutually exclusive: provide exactly one of them.

## Creating Comments

### Markdown Comment (Recommended)

```python
response = client.post_comment(
    document_id="document_id",
    markdown="My comment with **bold** text"
)

comment = response.comment
print(f"Created: {comment.id}")
```

Markdown supports rich formatting:

```python
markdown = """
Comment with **bold** and *italic*

- Item 1
- Item 2

`inline code` and [links](https://vaiz.app)
"""

response = client.post_comment(
    document_id="document_id",
    markdown=markdown
)
```

### HTML Comment (Legacy)

```python
response = client.post_comment(
    document_id="document_id",
    content="<p>Comment with <strong>bold</strong></p>"
)
```

### Comment with Files

```python
from vaiz.models.enums import UploadFileType

# Upload files
img = client.upload_file("screenshot.png", UploadFileType.Image)
doc = client.upload_file("report.pdf", UploadFileType.Pdf)

# Post comment
response = client.post_comment(
    document_id="document_id",
    markdown="Files attached",
    file_ids=[img.file.id, doc.file.id]
)
```

## Replies

```python
# Original comment
original = client.post_comment(
    document_id="document_id",
    markdown="Original"
)

# Reply
reply = client.post_comment(
    document_id="document_id",
    markdown="Reply",
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

See [`CommentReactionType`](../api-reference/enums#commentreactiontype) for all available reactions.

## Editing Comments

```python
response = client.edit_comment(
    comment_id="comment_id",
    markdown="Updated content with a [link](https://vaiz.app)"
)
```

### Managing Files

```python
# Add files (must include markdown or content)
response = client.edit_comment(
    comment_id="comment_id",
    markdown="Updated content",
    add_file_ids=["new_file_id"]
)

# Remove files (must include markdown or content)
response = client.edit_comment(
    comment_id="comment_id",
    markdown="Updated content",
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
document_id = task_response.task.document

# When creating task
task = CreateTaskRequest(name="Task", board="...", group="...")
response = client.create_task(task)
document_id = response.task.document
```

## See Also

- [Tasks API](./tasks)
- [Files API](./files)
- [Examples](../patterns/introduction)

