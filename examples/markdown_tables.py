"""
Example: Tables in Markdown documents.

Tables use standard GFM syntax. The first row is the header row, and cells
support inline formatting (bold, italic, code, links, strikethrough).
"""

from examples.config import get_client, BOARD_ID, GROUP_ID
from vaiz.models import CreateTaskRequest, TaskPriority


MARKDOWN = """# 📊 Project Status Report

**Report Date:** 2025-10-22

---

## Task Progress

| Task | Assignee | Status | Priority |
| --- | --- | --- | --- |
| Design UI mockups | John Doe | ✅ Done | High |
| Implement API | Jane Smith | ⏳ In Progress | High |
| Write documentation | Mike Johnson | 📋 Todo | Medium |
| Testing | Sarah Wilson | 📋 Todo | Low |

## Milestones

| **Milestone** | **Due Date** | **Completion** |
| --- | --- | --- |
| **Alpha Release** | 2025-11-01 | *85%* |
| **Beta Release** | 2025-11-15 | *40%* |
| **Production** | 2025-12-01 | *10%* |

## Team Metrics

| Metric | Value |
| --- | --- |
| Total Tasks | 47 |
| Completed | 28 |
| In Progress | 12 |
| Blocked | 3 |
| Overdue | 4 |

---

*Generated with Markdown tables*
"""


def main():
    client = get_client()
    client.verbose = True

    task = CreateTaskRequest(
        name="Project Status Report with Tables",
        board=BOARD_ID,
        group=GROUP_ID,
        priority=TaskPriority.General,
        description="Initial description",
    )

    try:
        task_response = client.create_task(task)
        document_id = task_response.task.document
        print(f"Created task: {task_response.task.hrid}\n")

        client.replace_markdown_document(document_id=document_id, markdown=MARKDOWN)
        print("✅ Document with tables created")

        saved = client.get_markdown_document(document_id)
        table_rows = [line for line in saved.splitlines() if line.startswith("|")]
        print(f"📊 Table rows in the saved document: {len(table_rows)}")

        print(f"\n🎉 Check task {task_response.task.hrid} in Vaiz to see the tables!")

    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
