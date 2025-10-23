"""
Example: Advanced Mention Usage in Task Descriptions

This example demonstrates how to create task descriptions with mentions,
combining them with other document elements for rich content.
"""

from examples.config import get_client, PROJECT_ID, BOARD_ID
from vaiz import (
    CreateTaskRequest,
    TaskPriority,
    # Document structure builders
    heading,
    paragraph,
    text,
    bullet_list,
    list_item,
    horizontal_rule,
    table,
    table_row,
    table_header,
    table_cell,
    # Mention helpers
    mention_user,
    mention_task,
    mention_milestone,
    mention_document,
)


def main():
    client = get_client()
    client.verbose = True
    
    print("=== Advanced Mention Usage Example ===\n")
    
    # Get real IDs from API
    print("Getting real IDs from API...")
    
    # Get user profile for current member ID
    profile = client.get_profile()
    current_member_id = profile.profile.member_id
    print(f"✓ Member ID: {current_member_id}")
    
    # Get real IDs
    from vaiz.models import GetDocumentsRequest, Kind
    from examples.config import SPACE_ID
    
    # Get document ID
    docs_response = client.get_documents(
        GetDocumentsRequest(kind=Kind.Space, kind_id=SPACE_ID)
    )
    reference_doc_id = None
    if docs_response.payload.documents:
        reference_doc_id = docs_response.payload.documents[0].id
        print(f"✓ Reference Document ID: {reference_doc_id}")
    
    # Get task ID
    from vaiz.models import GetTasksRequest
    tasks_response = client.get_tasks(GetTasksRequest())
    task_id = None
    if tasks_response.payload.tasks:
        task_id = tasks_response.payload.tasks[0].id
        print(f"✓ Task ID: {task_id}")
    
    # Get milestone ID
    milestones_response = client.get_milestones()
    milestone_id = None
    if milestones_response.milestones:
        milestone_id = milestones_response.milestones[0].id
        print(f"✓ Milestone ID: {milestone_id}")
    
    print()
    
    # Example 1: Create task with mentions in description
    print("1. Creating task with rich description including mentions...")
    
    # Build rich task description with mentions
    task_description = [
        heading(1, "📋 Project Status Update"),
        
        paragraph(
            text("This task is assigned to "),
            mention_user(current_member_id),
            text(" and requires coordination with the team.")
        ),
        
        horizontal_rule(),
        
        heading(2, "🎯 Objectives"),
        bullet_list(
            "Review current progress",
            "Update documentation",
            list_item(
                paragraph(
                    text("Coordinate with "),
                    mention_user(current_member_id)
                )
            )
        ),
        
        heading(2, "📎 Related Items"),
    ]
    
    # Add related items if available
    related_items = [text("References: ")]
    if milestone_id:
        related_items.extend([
            text("Milestone "),
            mention_milestone(milestone_id),
        ])
    if reference_doc_id:
        if milestone_id:
            related_items.append(text(" | "))
        related_items.extend([
            text("Document "),
            mention_document(reference_doc_id),
        ])
    
    task_description.append(paragraph(*related_items))
    
    task_description.extend([
        
        horizontal_rule(),
        
        heading(2, "👥 Team Members"),
        table(
            table_row(
                table_header("Role"),
                table_header("Member")
            ),
            table_row(
                table_cell("Lead"),
                table_cell(
                    paragraph(mention_user(current_member_id))
                )
            ),
            table_row(
                table_cell("Reviewer"),
                table_cell(
                    paragraph(mention_user(current_member_id))
                )
            )
        ),
    ])
    
    try:
        # Note: You need to provide valid PROJECT_ID and BOARD_ID in .env
        if not PROJECT_ID or not BOARD_ID:
            print("⚠️  Please set VAIZ_PROJECT_ID and VAIZ_BOARD_ID in your .env file")
            print("Skipping task creation example...")
        else:
            task_request = CreateTaskRequest(
                name="Project Status Update with Mentions",
                group=PROJECT_ID,
                board=BOARD_ID,
                priority=TaskPriority.General,
            )
            
            task_response = client.create_task(task_request)
            task_id = task_response.task.id
            document_id = task_response.task.document
            
            print(f"✅ Task created: {task_response.task.hrid}")
            print(f"Task ID: {task_id}")
            print(f"Document ID: {document_id}")
            
            # Update task description with rich content
            client.replace_json_document(document_id, task_description)
            print("✅ Task description updated with mentions!")
            
    except Exception as e:
        print(f"❌ Error creating task: {e}")
    
    print("\n" + "="*50)
    
    # Example 2: Create document with complex mention structure
    print("\n2. Creating document with complex mention structure...")
    
    # Create new document for testing
    from vaiz.models import CreateDocumentRequest
    create_request = CreateDocumentRequest(
        kind=Kind.Space,
        kind_id=SPACE_ID,
        title="Advanced Example: Meeting Notes with Mentions",
        index=0
    )
    doc_response = client.create_document(create_request)
    document_id = doc_response.payload.document.id
    print(f"✓ Created document: {document_id}")
    
    update_content = [
        heading(1, "📝 Meeting Notes"),
        
        paragraph(
            text("Date: 2025-10-23", bold=True)
        ),
        
        heading(2, "Attendees"),
        bullet_list(
            list_item(paragraph(mention_user(current_member_id))),
            list_item(paragraph(mention_user(current_member_id))),
        ),
        
        horizontal_rule(),
        
        heading(2, "Action Items"),
    ]
    
    # Add action items table if task available
    if task_id:
        update_content.append(table(
            table_row(
                table_header("Task"),
                table_header("Assignee"),
                table_header("Status")
            ),
            table_row(
                table_cell(
                    paragraph(mention_task(task_id))
                ),
                table_cell(
                    paragraph(mention_user(current_member_id))
                ),
                table_cell("In Progress")
            ),
            table_row(
                table_cell("Update documentation"),
                table_cell(
                    paragraph(mention_user(current_member_id))
                ),
                table_cell("Pending")
            )
        ))
    
    update_content.append(horizontal_rule())
    
    # Add references section
    update_content.append(heading(2, "References"))
    
    references = []
    if milestone_id:
        references.append(list_item(
            paragraph(
                text("Milestone: "),
                mention_milestone(milestone_id)
            )
        ))
    if reference_doc_id:
        references.append(list_item(
            paragraph(
                text("Related doc: "),
                mention_document(reference_doc_id)
            )
        ))
    
    if references:
        update_content.append(bullet_list(*references))
    
    update_content.extend([
        
        paragraph(
            text("Last updated by "),
            mention_user(current_member_id),
            text(" on 2025-10-23", italic=True)
        )
    ])
    
    try:
        client.replace_json_document(document_id, update_content)
        print("✅ Document updated successfully!")
        print(f"\n🔗 View at: https://vaiz.app/document/{document_id}")
        
        # Verify mentions were created
        print("\nVerifying mentions...")
        doc_content = client.get_json_document(document_id)
        
        mention_count = 0
        for node in doc_content.get("default", {}).get("content", []):
            if node.get("type") == "paragraph" and "content" in node:
                for child in node["content"]:
                    if child.get("type") == "custom-mention":
                        mention_count += 1
            elif node.get("type") == "extension-table" and "content" in node:
                # Check mentions in tables
                for row in node["content"]:
                    if "content" in row:
                        for cell in row["content"]:
                            if "content" in cell:
                                for cell_node in cell["content"]:
                                    if cell_node.get("type") == "paragraph" and "content" in cell_node:
                                        for child in cell_node["content"]:
                                            if child.get("type") == "custom-mention":
                                                mention_count += 1
            elif node.get("type") == "bulletList" and "content" in node:
                # Check mentions in lists
                for item in node["content"]:
                    if "content" in item:
                        for item_node in item["content"]:
                            if item_node.get("type") == "paragraph" and "content" in item_node:
                                for child in item_node["content"]:
                                    if child.get("type") == "custom-mention":
                                        mention_count += 1
        
        print(f"✓ Found {mention_count} mention block(s) in document")
        
    except Exception as e:
        print(f"❌ Error updating document: {e}")
    
    print("\n=== Example completed ===")


if __name__ == "__main__":
    main()
