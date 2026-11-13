"""
Example: Replace document content with rich Markdown using replace_markdown_document().

Markdown is the way to write document content. It is converted to native
document blocks on the server (headings, lists, links, code, quotes, ...).
See the "Markdown syntax" page in the docs for the full dialect.
"""

from examples.config import get_client, BOARD_ID, GROUP_ID
from vaiz.models import CreateTaskRequest, TaskPriority


MARKDOWN = """# 🚀 Document with Rich Content

This document was written with **Markdown** via `replace_markdown_document()`.

## ✨ Features

- **Rich text formatting** with bold, *italic*, ~~strikethrough~~ and `inline code`
- Structured content with *headings* and lists
- Direct control over the document through a plain string

## 🔗 Links

You can also add links: [Visit Vaiz](https://vaiz.com)

> Markdown is the only way to write document content.
"""


def main():
    client = get_client()
    client.verbose = True

    # Create a task with an initial description to get a document ID
    task = CreateTaskRequest(
        name="Task for Markdown Document Replacement Demo",
        board=BOARD_ID,
        group=GROUP_ID,
        priority=TaskPriority.General,
        description="Initial description that will be replaced with rich content",
    )

    try:
        task_response = client.create_task(task)
        document_id = task_response.task.document
        print(f"Created task with document ID: {document_id}")

        print("\n=== Initial content ===")
        print(client.get_markdown_document(document_id))

        print("\n=== Replacing document with Markdown ===")
        client.replace_markdown_document(document_id=document_id, markdown=MARKDOWN)
        print("✅ Document content replaced")

        print("\n=== Updated content ===")
        print(client.get_markdown_document(document_id))

        print(f"\n🎉 Document {document_id} now contains rich formatted content!")

    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
