"""
Example: Using Document Structure helper functions for type-safe document content creation.

This example demonstrates how to use the built-in document structure helper functions
to create rich document content in a type-safe, readable way.
"""

from examples.config import get_client
from vaiz.models import CreateTaskRequest, TaskPriority

# Import document structure builder functions
from vaiz import (
    text, paragraph, heading, bullet_list, ordered_list, 
    list_item, link_text, horizontal_rule, blockquote, details
)


def main():
    client = get_client()
    client.verbose = True

    # Create a task
    task = CreateTaskRequest(
        name="Type-Safe Document with Helpers Demo",
        group=client.space_id,
        board="your_board_id",
        priority=TaskPriority.General,
        description="Will be replaced"
    )
    
    try:
        task_response = client.create_task(task)
        document_id = task_response.task.document
        print(f"Created task: {task_response.task.hrid}\n")
        
        # Build content using helper functions - type-safe and readable!
        content = [
            # Title
            heading(1, "🚀 Project Documentation"),
            
            # Subtitle with formatting
            paragraph(
                text("Last updated: 2025-10-22 | ", italic=True),
                text("Status: Active", bold=True)
            ),
            
            # Separator
            horizontal_rule(),
            
            # Overview section
            heading(2, "📋 Overview"),
            paragraph(
                "This project uses ",
                text("structured document format", bold=True),
                " for rich text editing. Learn more at ",
                link_text("Vaiz Docs", "https://docs.vaiz.app"),
                "."
            ),
            
            # Features with bullet list
            heading(2, "✨ Key Features"),
            bullet_list(
                # Simple string items
                "Real-time collaboration",
                "Rich text editing",
                # Complex item with nested content
                list_item(
                    paragraph(
                        text("API Integration", bold=True),
                        " - Full Python SDK support"
                    ),
                    # Nested list!
                    bullet_list(
                        "Task management",
                        "Document operations", 
                        "Custom fields"
                    )
                )
            ),
            
            # Tech stack with ordered list
            heading(2, "🛠 Tech Stack"),
            ordered_list(
                list_item(paragraph(text("Backend: ", bold=True), "Node.js, MongoDB")),
                list_item(paragraph(text("Frontend: ", bold=True), "React, TypeScript")),
                list_item(paragraph(text("SDK: ", bold=True), "Python 3.8+"))
            ),
            
            # Code example
            heading(2, "💻 Quick Start"),
            paragraph("Install the SDK: ", text("pip install vaiz-sdk", code=True)),
            paragraph("Basic usage:"),
            paragraph(text("from vaiz import VaizClient", code=True)),
            paragraph(text("client = VaizClient(token='...')", code=True)),
            paragraph(text("task = client.get_task('PRJ-123')", code=True)),
            
            # Important note
            heading(2, "💡 Important"),
            paragraph(
                text("Security Notice: ", bold=True),
                "Always store your API token securely using environment variables."
            ),
            
            # Quote section
            heading(2, "📝 Philosophy"),
            blockquote(
                paragraph(
                    text("Good software is like a good joke: ", italic=True),
                    text("it needs no explanation.", bold=True, italic=True)
                ),
                paragraph(
                    "— The Pragmatic Programmer"
                )
            ),
            
            # Collapsible details section
            heading(2, "🔍 Advanced Usage"),
            details(
                "Click to expand: API Configuration",
                paragraph(
                    text("Endpoint: ", bold=True),
                    text("https://api.vaiz.app/v1", code=True)
                ),
                paragraph(
                    text("Authentication: ", bold=True),
                    "Bearer token required"
                ),
                paragraph(
                    text("Rate Limit: ", bold=True),
                    "1000 requests per hour"
                )
            ),
            
            # Links section
            heading(2, "🔗 Resources"),
            bullet_list(
                list_item(paragraph(link_text("Documentation", "https://docs.vaiz.app"))),
                list_item(paragraph(link_text("GitHub", "https://github.com/vaizcom/vaiz-python-sdk"))),
                list_item(paragraph(link_text("Community", "https://vaiz.app/community")))
            ),
            
            # Footer
            horizontal_rule(),
            paragraph(
                text("Generated with ", italic=True),
                text("replace_json_document", code=True),
                text(" helper functions", italic=True)
            )
        ]
        
        # Replace document content
        print("=== Replacing document with type-safe content ===")
        client.replace_json_document(
            document_id=document_id,
            content=content
        )
        print("✅ Document replaced successfully!\n")
        
        print("📊 Content Statistics:")
        print(f"   Total blocks: {len(content)}")
        print(f"   Headings: {sum(1 for c in content if c.get('type') == 'heading')}")
        print(f"   Paragraphs: {sum(1 for c in content if c.get('type') == 'paragraph')}")
        print(f"   Lists: {sum(1 for c in content if c.get('type') in ['bulletList', 'orderedList'])}")
        print(f"\n💡 Content built using document structure helpers!")
        
        print(f"\n🎉 Check task {task_response.task.hrid} in Vaiz!")
        
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()

