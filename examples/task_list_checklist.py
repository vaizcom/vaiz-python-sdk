#!/usr/bin/env python3
"""
Example: Creating and using task lists (checklists) in documents

Task lists allow you to create interactive checklists with:
- Checkbox items that can be checked/unchecked
- Nested task lists (multi-level checklists)
- Mixed content (paragraphs + task lists)
"""

import os
from vaiz import VaizClient, heading, paragraph, task_list, task_item


def main():
    # Initialize client
    api_key = os.getenv("VAIZ_API_KEY")
    space_id = os.getenv("VAIZ_SPACE_ID")
    
    if not api_key or not space_id:
        print("Error: Set VAIZ_API_KEY and VAIZ_SPACE_ID environment variables")
        return
    
    client = VaizClient(api_key=api_key, space_id=space_id)
    
    print("=== Task List (Checklist) Examples ===\n")
    
    # Example 1: Simple checklist
    print("1. Creating simple checklist")
    simple_checklist = [
        heading(1, "Daily Tasks"),
        paragraph("Here's what needs to be done today:"),
        
        task_list(
            task_item("Review pull requests", checked=True),
            task_item("Update documentation", checked=False),
            task_item("Deploy to production", checked=False),
        )
    ]
    
    # Example 2: Nested checklist (multi-level)
    print("2. Creating nested checklist")
    nested_checklist = [
        heading(1, "Project Milestones"),
        
        task_list(
            # Main task with subtasks
            task_item(
                paragraph("Phase 1: Planning"),
                task_list(
                    task_item("Define requirements", checked=True),
                    task_item("Create wireframes", checked=True),
                    task_item("Review with stakeholders", checked=False)
                ),
                checked=True
            ),
            
            # Another main task with subtasks
            task_item(
                paragraph("Phase 2: Development"),
                task_list(
                    task_item("Setup project structure", checked=True),
                    task_item("Implement features", checked=False),
                    task_item(
                        paragraph("Testing"),
                        task_list(
                            task_item("Unit tests", checked=False),
                            task_item("Integration tests", checked=False),
                            task_item("E2E tests", checked=False)
                        ),
                        checked=False
                    )
                ),
                checked=False
            ),
            
            # Third main task
            task_item(
                paragraph("Phase 3: Deployment"),
                task_list(
                    task_item("Prepare production environment", checked=False),
                    task_item("Deploy application", checked=False),
                    task_item("Monitor metrics", checked=False)
                ),
                checked=False
            )
        )
    ]
    
    # Example 3: Shopping list (simple strings)
    print("3. Creating shopping list")
    shopping_list = [
        heading(1, "Shopping List"),
        paragraph("Items to buy this week:"),
        
        task_list(
            "Milk",
            "Bread",
            "Eggs",
            "Coffee",
            "Vegetables"
        )
    ]
    
    # Example 4: Mixed content with checklists
    print("4. Creating document with mixed content")
    mixed_content = [
        heading(1, "Sprint Planning"),
        
        paragraph("This sprint we will focus on user authentication."),
        
        heading(2, "Backend Tasks"),
        task_list(
            task_item("Design database schema", checked=True),
            task_item("Implement authentication API", checked=False),
            task_item("Add JWT tokens", checked=False),
            task_item("Write tests", checked=False)
        ),
        
        heading(2, "Frontend Tasks"),
        task_list(
            task_item("Create login page", checked=True),
            task_item("Create registration page", checked=False),
            task_item("Add form validation", checked=False),
            task_item("Connect to API", checked=False)
        ),
        
        paragraph("Review meeting scheduled for Friday."),
    ]
    
    # Example 5: Complex nested structure
    print("5. Creating complex nested structure")
    complex_checklist = [
        heading(1, "Product Launch Checklist"),
        
        task_list(
            task_item(
                paragraph("Pre-Launch Preparation"),
                task_list(
                    task_item(
                        paragraph("Technical Setup"),
                        task_list(
                            task_item("Configure servers", checked=True),
                            task_item("Setup monitoring", checked=True),
                            task_item("Configure CDN", checked=False)
                        ),
                        checked=True
                    ),
                    task_item(
                        paragraph("Content Preparation"),
                        task_list(
                            task_item("Write blog post", checked=True),
                            task_item("Create video demo", checked=False),
                            task_item("Update website", checked=False)
                        ),
                        checked=False
                    )
                ),
                checked=False
            ),
            
            task_item(
                paragraph("Launch Day"),
                task_list(
                    task_item("Deploy to production", checked=False),
                    task_item("Send email announcement", checked=False),
                    task_item("Post on social media", checked=False),
                    task_item("Monitor analytics", checked=False)
                ),
                checked=False
            ),
            
            task_item(
                paragraph("Post-Launch"),
                task_list(
                    task_item("Collect user feedback", checked=False),
                    task_item("Fix critical bugs", checked=False),
                    task_item("Write retrospective", checked=False)
                ),
                checked=False
            )
        )
    ]
    
    # You can now use any of these examples to replace document content:
    # 
    # # For task descriptions:
    # task_response = client.get_task("PRJ-123")
    # client.replace_json_document(task_response.task.document, simple_checklist)
    # 
    # # For standalone documents:
    # from vaiz import GetDocumentsRequest, Kind
    # docs = client.get_documents(GetDocumentsRequest(kind=Kind.Space, kind_id=space_id))
    # if docs.payload.documents:
    #     doc_id = docs.payload.documents[0].id
    #     client.replace_json_document(doc_id, nested_checklist)
    
    print("\n✅ All checklist examples created!")
    print("\nTo use these checklists:")
    print("1. Get a document ID (from task or standalone document)")
    print("2. Call client.replace_json_document(document_id, content)")
    print("\nExample:")
    print("  task = client.get_task('PRJ-123')")
    print("  client.replace_json_document(task.task.document, simple_checklist)")


if __name__ == "__main__":
    main()

