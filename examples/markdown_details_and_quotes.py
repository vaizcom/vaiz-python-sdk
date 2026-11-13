"""
Example: Collapsible sections, quotes, ordered lists and links in Markdown.

Collapsible blocks use the `:::details{summary="..." open}` container.
Without the `open` flag the block is imported collapsed.
"""

from examples.config import get_client, BOARD_ID, GROUP_ID
from vaiz.models import CreateTaskRequest, TaskPriority


MARKDOWN = """# 🚀 Project Documentation

*Last updated: 2025-10-22* | **Status: Active**

---

## 📋 Overview

This project uses a **structured document format** for rich text editing.
Learn more at [Vaiz Docs](https://vaiz.com).

## ✨ Features

- Rich text formatting
- Tables and checklists
- Collapsible sections

## 🛠 Setup

1. Install the SDK
2. Create a client
3. Write your first document

> **Tip:** write content with `replace_markdown_document()` and read it back
> with `get_markdown_document()`.

## ❓ FAQ

:::details{summary="How do I install the SDK?"}
Run `pip install vaiz-sdk` in your environment.
:::

:::details{summary="Is this block open by default?" open}
Yes - this one carries the `open` flag.
:::
"""


def main():
    client = get_client()
    client.verbose = True

    task = CreateTaskRequest(
        name="Markdown Details and Quotes Demo",
        board=BOARD_ID,
        group=GROUP_ID,
        priority=TaskPriority.General,
        description="Will be replaced",
    )

    try:
        task_response = client.create_task(task)
        document_id = task_response.task.document
        print(f"Created task: {task_response.task.hrid}\n")

        client.replace_markdown_document(document_id=document_id, markdown=MARKDOWN)
        print("✅ Document written")

        print("\n=== Document as Markdown ===\n")
        print(client.get_markdown_document(document_id))

    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
