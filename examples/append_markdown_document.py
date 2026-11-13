"""
Example: Append Markdown to an existing document with append_markdown_document().

Appending adds content to the end of the document without removing existing
content - useful for incremental updates, logs and notes.
"""

from examples.config import get_client, BOARD_ID, GROUP_ID
from vaiz.models import CreateTaskRequest, TaskPriority


def main():
    client = get_client()
    client.verbose = True

    task = CreateTaskRequest(
        name="Incremental Document Updates Demo",
        board=BOARD_ID,
        group=GROUP_ID,
        priority=TaskPriority.General,
        description="Initial task description - this will remain",
    )

    try:
        task_response = client.create_task(task)
        document_id = task_response.task.document
        print(f"Created task: {task_response.task.hrid}\n")

        print("Initial content:")
        print(client.get_markdown_document(document_id))

        print("\n=== Appending Update #1 ===")
        client.append_markdown_document(
            document_id,
            "---\n\n"
            "## Update #1 - Design Phase\n\n"
            "**Status:** Design mockups completed\n\n"
            "- Homepage design approved\n"
            "- Component library created\n"
            "- Style guide finalized\n",
        )
        print("✅ Update #1 appended")

        print("\n=== Appending Update #2 ===")
        client.append_markdown_document(
            document_id,
            "---\n\n"
            "## Update #2 - Development Progress\n\n"
            "**Status:** API implementation in progress\n\n"
            "- [x] User authentication\n"
            "- [ ] Task management endpoints\n"
            "- [ ] Document API\n",
        )
        print("✅ Update #2 appended")

        print("\n=== Appending Update #3 ===")
        client.append_markdown_document(
            document_id,
            "---\n\n"
            "## Update #3 - Final Notes\n\n"
            "**Conclusion:** All updates have been *successfully appended* "
            "to the original content.\n\n"
            "> **Key Insight:** Incremental updates keep content organized.\n",
        )
        print("✅ Update #3 appended")

        final = client.get_markdown_document(document_id)
        print("\n📊 Final document:\n")
        print(final)

        print("\nOriginal content preserved:", "Initial task description" in final)
        for number in (1, 2, 3):
            print(f"Update #{number} added:", f"Update #{number}" in final)

    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
