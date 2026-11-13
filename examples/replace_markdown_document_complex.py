"""
Example: A complex document written entirely in Markdown.

Demonstrates the full Markdown dialect supported by the server:
- Headings, text formatting (bold, italic, strikethrough, highlight, code)
- Nested bullet and ordered lists
- Checklists
- Tables
- Fenced code blocks and Mermaid diagrams
- Blockquotes and horizontal rules
- Inline and block equations
- Containers: callout, details, columns
"""

from examples.config import get_client, BOARD_ID, GROUP_ID
from vaiz.models import CreateTaskRequest, TaskPriority


MARKDOWN = """# 📚 Comprehensive Project Documentation

**Version:** 2.0 | *Status:* ==Active== | ~~Draft~~

---

## Overview

This guide covers `replace_markdown_document()` with every supported block.
Read more at [Vaiz](https://vaiz.com).

:::callout{icon="Light" color="blue"}
Callout text is plain text. Pick the icon and color in the start line.
:::

## Lists

- Level 1
    - Level 2
        - Level 3
- Another top-level item

1. First step
2. Second step
    1. Nested step
3. Third step

## Checklist

- [x] Write the content
- [ ] Review it
- [ ] Publish

## Data

| Feature | Status | Notes |
| --- | --- | --- |
| **Tables** | `done` | Cells support inline formatting |
| Lists | ~~todo~~ | *italic* |

## Code

```python
def greet(name: str) -> str:
    return f"Hello, {name}!"
```

```mermaid
graph LR
    A[Write markdown] --> B[Server converts]
    B --> C[Native blocks]
```

## Math

Inline math $E=mc^2$ and a block equation:

$$\\int_0^1 x\\,dx = \\frac{1}{2}$$

> **Note:** quotes can hold *formatted* text.

## Collapsible and columns

:::details{summary="Click to expand" open}
Hidden **details** content with a list:

- one
- two
:::

:::columns
::col
### Left
Left column text.
::col
### Right
Right column text.
:::
"""


def main():
    client = get_client()
    client.verbose = True

    task = CreateTaskRequest(
        name="Complex Markdown Document Demo",
        board=BOARD_ID,
        group=GROUP_ID,
        priority=TaskPriority.General,
        description="Initial description",
    )

    try:
        task_response = client.create_task(task)
        document_id = task_response.task.document
        print(f"Created task with document ID: {document_id}\n")

        client.replace_markdown_document(document_id=document_id, markdown=MARKDOWN)
        print("✅ Complex document written")

        saved = client.get_markdown_document(document_id)
        print("\n=== Document as Markdown ===\n")
        print(saved)

        print(f"\n🎉 Check task {task_response.task.hrid} in Vaiz to see the result!")

    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
