"""
Example: Using Mention Blocks in Documents

This example demonstrates how to create documents with mention blocks
that reference users, documents, tasks, and milestones.
"""

from examples.config import get_client
from vaiz.helpers import (
    paragraph,
    text,
    heading,
    mention_user,
    mention_document,
    mention_task,
    mention_milestone,
)


def main():
    client = get_client()
    client.verbose = True
    
    print("=== Creating Document with Mention Blocks ===\n")
    
    # Get real IDs from API
    print("Getting real IDs from API...")
    
    # Get current user ID
    profile = client.get_profile()
    user_id = profile.profile.member_id
    print(f"✓ User ID: {user_id}")
    
    # Get a document ID
    from vaiz.models import GetDocumentsRequest, Kind, CreateDocumentRequest
    from examples.config import SPACE_ID
    
    docs_response = client.get_documents(
        GetDocumentsRequest(kind=Kind.Space, kind_id=SPACE_ID)
    )
    reference_doc_id = None
    if docs_response.payload.documents:
        reference_doc_id = docs_response.payload.documents[0].id
        print(f"✓ Reference Document ID: {reference_doc_id}")
    
    # Get a task ID
    from vaiz.models import GetTasksRequest
    tasks_response = client.get_tasks(GetTasksRequest())
    task_id = None
    if tasks_response.payload.tasks:
        task_id = tasks_response.payload.tasks[0].id
        print(f"✓ Task ID: {task_id}")
    
    # Get a milestone ID
    milestones_response = client.get_milestones()
    milestone_id = None
    if milestones_response.milestones:
        milestone_id = milestones_response.milestones[0].id
        print(f"✓ Milestone ID: {milestone_id}")
    
    print("\nCreating new document with mentions...")
    
    # Create a new document in Space
    create_request = CreateDocumentRequest(
        kind=Kind.Space,
        kind_id=SPACE_ID,
        title="Example: Mention Blocks",
        index=0
    )
    doc_response = client.create_document(create_request)
    document_id = doc_response.payload.document.id
    
    print(f"✓ Created document: {document_id}")
    
    # Build content with real mentions
    content = [
        heading(1, "Document with Mentions"),
        
        paragraph(
            text("This document contains various mention types:")
        ),
        
        # Mention a user
        paragraph(
            text("User mention: "),
            mention_user(user_id),
            text(" - this mentions a user")
        ),
    ]
    
    # Add document mention if available
    if reference_doc_id:
        content.append(paragraph(
            text("Document mention: "),
            mention_document(reference_doc_id),
            text(" - this mentions another document")
        ))
    
    # Add task mention if available
    if task_id:
        content.append(paragraph(
            text("Task mention: "),
            mention_task(task_id),
            text(" - this mentions a task")
        ))
    
    # Add milestone mention if available
    if milestone_id:
        content.append(paragraph(
            text("Milestone mention: "),
            mention_milestone(milestone_id),
            text(" - this mentions a milestone")
        ))
    
    # Add section with multiple mentions
    content.append(heading(2, "Multiple Mentions in One Paragraph"))
    
    multiple_mentions_para = [
        text("You can mention multiple items: "),
        mention_user(user_id),
    ]
    
    if task_id:
        multiple_mentions_para.extend([
            text(" assigned to task "),
            mention_task(task_id),
        ])
    
    if milestone_id:
        multiple_mentions_para.extend([
            text(" in milestone "),
            mention_milestone(milestone_id)
        ])
    
    content.append(paragraph(*multiple_mentions_para))
    
    try:
        client.replace_json_document(document_id, content)
        print("\n✅ Document updated successfully with mention blocks!")
        print(f"\n🔗 View document: https://vaiz.app/document/{document_id}")
        
        # Verify mentions were created
        print("\nVerifying mentions...")
        doc_content = client.get_json_document(document_id)
        
        mention_count = 0
        for node in doc_content.get("default", {}).get("content", []):
            if node.get("type") == "paragraph" and "content" in node:
                for child in node["content"]:
                    if child.get("type") == "custom-mention":
                        mention_count += 1
        
        print(f"✓ Found {mention_count} mention block(s) in document")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n=== Example completed ===")


if __name__ == "__main__":
    main()

