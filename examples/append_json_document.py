"""
Example: Appending content to existing documents using appendJSONDocument API.

This example demonstrates how to add new content to documents without
removing existing content - useful for incremental updates, logs, and notes.
"""

from examples.config import get_client
from vaiz.models import CreateTaskRequest, TaskPriority
from vaiz import heading, paragraph, text, bullet_list, horizontal_rule


def main():
    client = get_client()
    client.verbose = True

    # Create a task with initial content
    task = CreateTaskRequest(
        name="Incremental Document Updates Demo",
        group=client.space_id,
        board="your_board_id",
        priority=TaskPriority.General,
        description="Initial task description - this will remain"
    )
    
    try:
        task_response = client.create_task(task)
        document_id = task_response.task.document
        print(f"Created task: {task_response.task.hrid}\n")
        
        # Get initial content
        initial_content = client.get_json_document(document_id)
        print(f"Initial content present: {len(initial_content.get('default', {}).get('content', []))} blocks")
        
        # Append first update
        print("\n=== Appending Update #1 ===")
        update1 = [
            horizontal_rule(),
            heading(2, "Update #1 - Design Phase"),
            paragraph(
                text("Status: ", bold=True),
                "Design mockups completed"
            ),
            bullet_list(
                "Homepage design approved",
                "Component library created",
                "Style guide finalized"
            )
        ]
        
        client.append_json_document(document_id, update1)
        print("✅ Update #1 appended")
        
        # Append second update
        print("\n=== Appending Update #2 ===")
        update2 = [
            horizontal_rule(),
            heading(2, "Update #2 - Development Progress"),
            paragraph(
                text("Status: ", bold=True),
                "API implementation in progress"
            ),
            bullet_list(
                "User authentication - Done",
                "Task management endpoints - In Progress",
                "Document API - Planned"
            )
        ]
        
        client.append_json_document(document_id, update2)
        print("✅ Update #2 appended")
        
        # Append third update
        print("\n=== Appending Update #3 ===")
        update3 = [
            horizontal_rule(),
            heading(2, "Update #3 - Final Notes"),
            paragraph(
                text("Conclusion: ", bold=True),
                "All updates have been ",
                text("successfully appended", italic=True),
                " to the original content."
            )
        ]
        
        client.append_json_document(document_id, update3)
        print("✅ Update #3 appended")
        
        # Verify all content exists
        final_content = client.get_json_document(document_id)
        final_blocks = final_content.get('default', {}).get('content', [])
        
        print(f"\n📊 Final Document Summary:")
        print(f"   Total blocks: {len(final_blocks)}")
        print(f"   Original content: ✅ Preserved")
        print(f"   Update #1: ✅ Added")
        print(f"   Update #2: ✅ Added")
        print(f"   Update #3: ✅ Added")
        
        print(f"\n🎉 Check task {task_response.task.hrid} to see incremental updates!")
        print(f"   The document now contains the original description plus 3 appended updates")
        
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()

