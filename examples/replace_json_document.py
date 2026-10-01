"""
Example: Replace document content with rich JSON content using the replaceJSONDocument API.

This example demonstrates how to replace document content with structured JSON content
in the document editor format, allowing for rich formatting, links, and other features.
"""

import json
from examples.config import get_client, BOARD_ID, GROUP_ID
from vaiz.models import CreateTaskRequest, TaskPriority


def main():
    client = get_client()
    client.verbose = True

    # First, create a task with initial description to get a document ID
    task = CreateTaskRequest(
        name="Task for JSON Document Replacement Demo",
        board=BOARD_ID,
        group=GROUP_ID,
        priority=TaskPriority.General,
        description="Initial description that will be replaced with rich content"
    )
    
    try:
        task_response = client.create_task(task)
        document_id = task_response.task.document
        print(f"Created task with document ID: {document_id}")
        
        # Get initial document content
        initial_content = client.get_json_document(document_id)
        print(f"Initial content: {json.dumps(initial_content, indent=2)}")
        
        # Create rich JSON content in document structure format
        json_content = [
            {
                "type": "heading",
                "attrs": {"level": 1},
                "content": [
                    {"type": "text", "text": "🚀 Document with Rich Content"}
                ]
            },
            {
                "type": "paragraph",
                "content": [
                    {"type": "text", "text": "This document was created using "},
                    {
                        "type": "text",
                        "marks": [{"type": "bold"}],
                        "text": "structured JSON content"
                    },
                    {"type": "text", "text": " via the replaceJSONDocument API."}
                ]
            },
            {
                "type": "heading",
                "attrs": {"level": 2},
                "content": [
                    {"type": "text", "text": "✨ Features"}
                ]
            },
            {
                "type": "bulletList",
                "content": [
                    {
                        "type": "listItem",
                        "content": [
                            {
                                "type": "paragraph",
                                "content": [
                                    {
                                        "type": "text",
                                        "marks": [{"type": "bold"}],
                                        "text": "Rich text formatting"
                                    },
                                    {"type": "text", "text": " with bold, italic, and more"}
                                ]
                            }
                        ]
                    },
                    {
                        "type": "listItem",
                        "content": [
                            {
                                "type": "paragraph",
                                "content": [
                                    {"type": "text", "text": "Structured content with "},
                                    {
                                        "type": "text",
                                        "marks": [{"type": "italic"}],
                                        "text": "headings"
                                    },
                                    {"type": "text", "text": " and lists"}
                                ]
                            }
                        ]
                    },
                    {
                        "type": "listItem",
                        "content": [
                            {
                                "type": "paragraph",
                                "content": [
                                    {"type": "text", "text": "Direct control over document structure"}
                                ]
                            }
                        ]
                    }
                ]
            },
            {
                "type": "heading",
                "attrs": {"level": 2},
                "content": [
                    {"type": "text", "text": "🔗 Links"}
                ]
            },
            {
                "type": "paragraph",
                "content": [
                    {"type": "text", "text": "You can also add links: "},
                    {
                        "type": "text",
                        "marks": [
                            {
                                "type": "link",
                                "attrs": {
                                    "href": "https://vaiz.app",
                                    "target": "_blank"
                                }
                            }
                        ],
                        "text": "Visit Vaiz"
                    }
                ]
            },
            {
                "type": "paragraph",
                "content": [
                    {
                        "type": "text",
                        "marks": [{"type": "code"}],
                        "text": "code snippets"
                    },
                    {"type": "text", "text": " and more!"}
                ]
            }
        ]
        
        # Replace document content with JSON
        print("\n=== Replacing Document with JSON Content ===")
        replace_response = client.replace_json_document(
            document_id=document_id,
            content=json_content
        )
        print("✅ Document content replaced with rich JSON content successfully!")
        
        # Verify the change
        updated_content = client.get_json_document(document_id)
        print(f"\nUpdated content: {json.dumps(updated_content, indent=2)}")
        
        print(f"\n🎉 Document {document_id} now contains rich formatted content!")
        
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()

