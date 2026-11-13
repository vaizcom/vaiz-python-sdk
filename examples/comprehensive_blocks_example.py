"""
Example: Comprehensive Document Combining Many Markdown Elements

This example combines mentions, an image, tables, checklists, quotes and
containers in one rich document written entirely in Markdown.
"""

import os

from examples.config import get_client, SPACE_ID
from vaiz.models import CreateDocumentRequest, GetDocumentsRequest, GetTasksRequest, Kind
from vaiz.models.enums import UploadFileType


def main():
    client = get_client()
    client.verbose = True

    print("=== Creating Comprehensive Markdown Document ===\n")

    # Step 1: Get entity IDs for mentions
    print("Step 1: Getting entity IDs...")

    member_id = client.get_profile().profile.member_id
    print(f"✓ Member ID: {member_id}")

    docs_response = client.get_documents(GetDocumentsRequest(kind=Kind.Space, kind_id=SPACE_ID))
    ref_doc_id = docs_response.payload.documents[0].id if docs_response.payload.documents else None
    if ref_doc_id:
        print(f"✓ Reference Document ID: {ref_doc_id}")

    tasks_response = client.get_tasks(GetTasksRequest())
    task_id = tasks_response.payload.tasks[0].id if tasks_response.payload.tasks else None
    if task_id:
        print(f"✓ Task ID: {task_id}")

    # Step 2: Upload an image (it is referenced by URL in the Markdown)
    print("\nStep 2: Uploading image...")

    image_path = "assets/example.png"
    image_url = None
    if os.path.exists(image_path):
        uploaded = client.upload_file(image_path, file_type=UploadFileType.Image)
        image_url = uploaded.file.url
        print(f"✓ Uploaded image: {uploaded.file.name}")
    else:
        print(f"⚠️  {image_path} not found, skipping the image section")

    # Step 3: Create document
    print("\nStep 3: Creating document...")

    document_id = client.create_document(
        CreateDocumentRequest(
            kind=Kind.Space,
            kind_id=SPACE_ID,
            title="Comprehensive Example: Markdown Elements",
            index=0,
        )
    ).payload.document.id
    print(f"✓ Created document: {document_id}")

    # Step 4: Build the Markdown
    print("\nStep 4: Building comprehensive content...")

    user = f"@[Me](user:{member_id})"
    task = f"@[Task](task:{task_id})" if task_id else "TBD"

    parts = [
        "# 📋 Project Status Report",
        "",
        f"**Report Date: 2025-10-23** | Prepared by: {user}",
        "",
        "---",
        "",
        "## 👥 Team Assignments",
        "",
        f"Current assignee: {user}",
        "",
        "| Assignee | Task | Status |",
        "| --- | --- | --- |",
        f"| {user} | {task} | In Progress |",
        "",
        "---",
        "",
    ]

    if image_url:
        parts += [
            "## 📸 Visual Assets",
            "",
            "Project screenshot:",
            "",
            f"![Project Screenshot]({image_url})",
            "",
            "---",
            "",
        ]

    parts += [
        "## ✅ Next Steps",
        "",
        "- [x] Collect requirements",
        "- [ ] Ship the first version",
        "",
        "## 🔗 Related Resources",
        "",
    ]
    if ref_doc_id:
        parts.append(f"- Reference document: @[Document](document:{ref_doc_id})")
    parts.append(f"- Task link: {task}")
    parts += [
        "",
        ":::callout{icon=\"Light\" color=\"blue\"}",
        "Everything here is plain Markdown.",
        ":::",
        "",
        "## 📊 Summary",
        "",
        "> **This document demonstrates the supported elements:**",
        ">",
        "> - Headings and formatted text",
        "> - User mentions and task references",
        "> - Images, tables and checklists",
        "> - Callouts and quotes",
        "",
        f"Last updated by {user} on *2025-10-23*",
        "",
    ]

    # Step 5: Write the document
    try:
        client.replace_markdown_document(document_id, "\n".join(parts))
        print("\n✅ Comprehensive document created successfully!")
        print(f"\n🔗 View document: https://vaiz.app/document/{document_id}")

        print("\nVerifying content...")
        saved = client.get_markdown_document(document_id)

        mention_count = saved.count("](user:") + saved.count("](task:") + saved.count("](document:")
        table_rows = sum(1 for line in saved.splitlines() if line.startswith("|"))
        images = saved.count("![")
        checklist_items = saved.count("- [x]") + saved.count("- [ ]")

        print(f"✓ Found {mention_count} mention(s)")
        print(f"✓ Found {images} image(s)")
        print(f"✓ Found {table_rows} table row(s)")
        print(f"✓ Found {checklist_items} checklist item(s)")

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

    print("\n=== Example completed ===")


if __name__ == "__main__":
    main()
