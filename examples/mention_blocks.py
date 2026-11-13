"""
Example: Using mentions in documents with Markdown.

Mentions use the syntax `@[Label](kind:id)` where kind is one of
`user`, `task`, `document`, `milestone`, `project` or `board`.
The label is cosmetic: only the kind and the ID are stored, and the editor
renders the live entity name.
"""

from examples.config import get_client, SPACE_ID
from vaiz.models import CreateDocumentRequest, GetDocumentsRequest, GetTasksRequest, Kind


def main():
    client = get_client()
    client.verbose = True

    print("=== Creating Document with Mentions ===\n")

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

    print("\nCreating new document with mentions...")

    document_id = client.create_document(
        CreateDocumentRequest(
            kind=Kind.Space,
            kind_id=SPACE_ID,
            title="Example: Mentions",
            index=0,
        )
    ).payload.document.id
    print(f"✓ Created document: {document_id}")

    # Build the Markdown with real mentions
    lines = [
        "# Document with Mentions",
        "",
        "This document contains various mention types:",
        "",
        f"User mention: @[Me](user:{member_id}) - this mentions a user",
    ]
    if reference_doc_id:
        lines += ["", f"Document mention: @[Document](document:{reference_doc_id}) - this mentions another document"]
    if task_id:
        lines += ["", f"Task mention: @[Task](task:{task_id}) - this mentions a task"]
    if milestone_id:
        lines += ["", f"Milestone mention: @[Milestone](milestone:{milestone_id}) - this mentions a milestone"]

    lines += ["", "## Multiple Mentions in One Paragraph", ""]
    paragraph = f"You can mention multiple items: @[Me](user:{member_id})"
    if task_id:
        paragraph += f" assigned to task @[Task](task:{task_id})"
    if milestone_id:
        paragraph += f" in milestone @[Milestone](milestone:{milestone_id})"
    lines.append(paragraph)

    try:
        client.replace_markdown_document(document_id, "\n".join(lines) + "\n")
        print("\n✅ Document updated successfully with mentions!")
        print(f"\n🔗 View document: https://vaiz.app/document/{document_id}")

        # Verify mentions were created: they survive the Markdown round trip
        print("\nVerifying mentions...")
        saved = client.get_markdown_document(document_id)
        mention_count = saved.count("](user:") + sum(
            saved.count(f"]({kind}:") for kind in ("task", "document", "milestone")
        )
        print(f"✓ Found {mention_count} mention(s) in document")

    except Exception as e:
        print(f"❌ Error: {e}")

    print("\n=== Example completed ===")


if __name__ == "__main__":
    main()
