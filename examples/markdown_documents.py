"""
Example: Working with document content using Markdown.

Markdown is the only supported way to read and write rich document content
in the SDK. Markdown is converted to native editor blocks on the server
(headings, lists, tables, code blocks, checklists, links, etc.) and can be
read back as Markdown.
"""

from examples.config import get_client
from examples.test_helpers import get_or_create_document_id


def replace_markdown():
    """Replace document content with Markdown."""
    client = get_client()
    document_id = get_or_create_document_id()

    markdown = """# Project Overview

Some **bold** and *italic* text with `inline code` and a [link](https://vaiz.app).

## Checklist

- [x] Design approved
- [ ] Implementation
- [ ] Code review

## Team

| Name | Role |
| --- | --- |
| Alice | Engineer |
| Bob | Designer |

```python
print("Code blocks work too")
```
"""

    client.replace_markdown_document(document_id, markdown)
    print(f"✅ Replaced content of document {document_id}")
    return document_id


def append_markdown(document_id: str):
    """Append Markdown content to an existing document."""
    client = get_client()

    client.append_markdown_document(
        document_id,
        "\n## Update\n\nAppended without removing existing content."
    )
    print("✅ Appended markdown content")


def read_markdown(document_id: str):
    """Read document content back as Markdown."""
    client = get_client()

    markdown = client.get_markdown_document(document_id)
    print("=== Document Markdown ===")
    print(markdown)


def task_description_workflow():
    """Create a task and set a rich Markdown description."""
    from vaiz.models import CreateTaskRequest, TaskPriority
    from examples.config import BOARD_ID, GROUP_ID

    client = get_client()

    # 1. Create the task (plain-text description only)
    task_response = client.create_task(
        CreateTaskRequest(
            name="Markdown Description Example",
            board=BOARD_ID,
            group=GROUP_ID,
            priority=TaskPriority.General,
        )
    )
    task = task_response.task

    # 2. Set a rich Markdown description via the task's document
    client.replace_markdown_document(
        task.document,
        "# Goal\n\nShip the feature.\n\n- [ ] Implement\n- [ ] Test\n- [ ] Release"
    )
    print(f"✅ Task {task.hrid} created with markdown description")

    # 3. Read it back
    print(task.get_task_description(client))


def main():
    document_id = replace_markdown()
    append_markdown(document_id)
    read_markdown(document_id)
    task_description_workflow()


if __name__ == "__main__":
    main()
