"""
Example: Replace document content using the replaceDocument API.
"""

import json
from examples.config import get_client
from vaiz.models import CreateTaskRequest, TaskPriority


def main():
    client = get_client()
    client.verbose = True

    # First, create a task with initial description to get a document ID
    task = CreateTaskRequest(
        name="Task for Document Replacement Demo",
        group=client.space_id,  # Using space_id as fallback for demo
        board="your_board_id",
        priority=TaskPriority.General,
        description="Initial description that will be replaced"
    )
    
    try:
        task_response = client.create_task(task)
        document_id = task_response.task.document
        print(f"Created task with document ID: {document_id}")
        
        # Get initial document content
        initial_content = client.get_json_document(document_id)
        print(f"Initial content: {json.dumps(initial_content, indent=2)}")
        
        # Create new content as PLAIN TEXT (current API supports plain text only)
        new_description_text = (
            "🚀 Document Content Replaced!\n\n"
            "This is the new content that completely replaced the original task description.\n\n"
            "Features Demonstrated:\n"
            "- ✅ Complete content replacement via API\n"
            "- 📝 Plain text formatting\n"
            "- 🎯 Direct document manipulation\n"
            "- 🔄 Real-time content updates\n\n"
            "Next Steps:\n"
            "1. Verify content changed\n"
            "2. Test with different content types\n"
            "3. Explore file attachments\n\n"
            "Note: Content was replaced using the replace_document API method from the Vaiz Python SDK."
        )
        
        # Replace document content
        print("\n=== Replacing Document Content ===")
        replace_response = client.replace_document(
            document_id=document_id,
            description=new_description_text
        )
        print("✅ Document content replaced successfully!")
        
        # Verify the change
        updated_content = client.get_json_document(document_id)
        print(f"\nUpdated content: {json.dumps(updated_content, indent=2)}")
        
        print(f"\n🎉 Document {document_id} content successfully replaced!")
        
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
