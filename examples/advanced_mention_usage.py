"""
Example: Advanced Mention Usage in Task Descriptions and Documents

This example demonstrates how to combine mentions with other Markdown elements
(lists, tables, checklists) in task descriptions and standalone documents.
"""

from examples.config import get_client, PROJECT_ID, BOARD_ID, SPACE_ID
from vaiz import CreateTaskRequest, TaskPriority
from vaiz.models import CreateDocumentRequest, GetDocumentsRequest, GetTasksRequest, Kind


def main():
    client = get_client()
    client.verbose = True

    print("=== Advanced Mention Usage Example ===\n")

    # Get real IDs from API
    print("Getting real IDs from API...")

    member_id = client.get_profile().profile.member_id
    print(f"✓ Member ID: {member_id}")

    docs_response = client.get_documents(GetDocumentsRequest(kind=Kind.Space, kind_id=SPACE_ID))
    reference_doc_id = docs_response.payload.documents[0].id if docs_response.payload.documents else None
    if reference_doc_id:
        print(f"✓ Reference Document ID: {reference_doc_id}")

    tasks_response = client.get_tasks(GetTasksRequest())
    task_id = tasks_response.payload.tasks[0].id if tasks_response.payload.tasks else None
    if task_id:
        print(f"✓ Task ID: {task_id}")

    milestones_response = client.get_milestones()
    milestone_id = milestones_response.milestones[0].id if milestones_response.milestones else None
    if milestone_id:
        print(f"✓ Milestone ID: {milestone_id}")

    user = f"@[Me](user:{member_id})"

    print()

    # Example 1: Create a task with mentions in the description
    print("1. Creating task with rich description including mentions...")

    references = []
    if milestone_id:
        references.append(f"- Milestone: @[Milestone](milestone:{milestone_id})")
    if reference_doc_id:
        references.append(f"- Document: @[Document](document:{reference_doc_id})")

    task_description = "\n".join(
        [
            "# 📋 Project Status Update",
            "",
            f"This task is assigned to {user} and requires coordination with the team.",
            "",
            "---",
            "",
            "## 🎯 Objectives",
            "",
            "- [ ] Review current progress",
            "- [ ] Update documentation",
            f"- [ ] Coordinate with {user}",
            "",
            "## 📎 Related Items",
            "",
            *(references or ["- No related items found"]),
            "",
            "## 👥 Team Members",
            "",
            "| Role | Member |",
            "| --- | --- |",
            f"| Lead | {user} |",
            f"| Reviewer | {user} |",
            "",
        ]
    )

    try:
        if not PROJECT_ID or not BOARD_ID:
            print("⚠️  Please set VAIZ_PROJECT_ID and VAIZ_BOARD_ID in your .env file")
            print("Skipping task creation example...")
        else:
            task_response = client.create_task(
                CreateTaskRequest(
                    name="Project Status Update with Mentions",
                    group=PROJECT_ID,
                    board=BOARD_ID,
                    priority=TaskPriority.General,
                )
            )
            print(f"✅ Task created: {task_response.task.hrid}")

            client.replace_markdown_document(task_response.task.document, task_description)
            print("✅ Task description updated with mentions!")

    except Exception as e:
        print(f"❌ Error creating task: {e}")

    print("\n" + "=" * 50)

    # Example 2: Create a document with mentions in lists and tables
    print("\n2. Creating document with complex mention structure...")

    document_id = client.create_document(
        CreateDocumentRequest(
            kind=Kind.Space,
            kind_id=SPACE_ID,
            title="Advanced Example: Meeting Notes with Mentions",
            index=0,
        )
    ).payload.document.id
    print(f"✓ Created document: {document_id}")

    action_task = f"@[Task](task:{task_id})" if task_id else "Prepare the report"
    notes = [
        "# 📝 Meeting Notes",
        "",
        "**Date:** 2025-10-23",
        "",
        "## Attendees",
        "",
        f"- {user}",
        "",
        "---",
        "",
        "## Action Items",
        "",
        "| Task | Assignee | Status |",
        "| --- | --- | --- |",
        f"| {action_task} | {user} | In Progress |",
        f"| Update documentation | {user} | Pending |",
        "",
        "---",
        "",
        "## References",
        "",
        *(references or ["- No references"]),
        "",
        f"Last updated by {user} on *2025-10-23*",
        "",
    ]

    try:
        client.replace_markdown_document(document_id, "\n".join(notes))
        print("✅ Document updated successfully!")
        print(f"\n🔗 View at: https://vaiz.app/document/{document_id}")

        print("\nVerifying mentions...")
        saved = client.get_markdown_document(document_id)
        mention_count = saved.count("](user:") + saved.count("](task:")
        print(f"✓ Found {mention_count} user/task mention(s) in document (tables and lists included)")

    except Exception as e:
        print(f"❌ Error updating document: {e}")

    print("\n=== Example completed ===")


if __name__ == "__main__":
    main()
