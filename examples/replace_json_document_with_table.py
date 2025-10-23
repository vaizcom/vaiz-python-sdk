"""
Example: Creating documents with tables using Document Structure helpers.

This example demonstrates how to create structured tables in documents
using the table helper functions.
"""

from examples.config import get_client
from vaiz.models import CreateTaskRequest, TaskPriority
from vaiz import (
    heading, paragraph, text, table, table_row,
    table_cell, horizontal_rule
)


def main():
    client = get_client()
    client.verbose = True

    # Create a task
    task = CreateTaskRequest(
        name="Project Status Report with Table",
        group=client.space_id,
        board="your_board_id",
        priority=TaskPriority.General,
        description="Initial description"
    )
    
    try:
        task_response = client.create_task(task)
        document_id = task_response.task.document
        print(f"Created task: {task_response.task.hrid}\n")
        
        # Build content with table
        content = [
            heading(1, "📊 Project Status Report"),
            
            paragraph(
                text("Report Date: ", bold=True),
                "2025-10-22"
            ),
            
            horizontal_rule(),
            
            heading(2, "Task Progress"),
            
            # Simple table (first row is treated as header in UI)
            table(
                table_row("Task", "Assignee", "Status", "Priority"),  # Header row
                table_row("Design UI mockups", "John Doe", "✅ Done", "High"),
                table_row("Implement API", "Jane Smith", "⏳ In Progress", "High"),
                table_row("Write documentation", "Mike Johnson", "📋 Todo", "Medium"),
                table_row("Testing", "Sarah Wilson", "📋 Todo", "Low")
            ),
            
            heading(2, "Milestones"),
            
            # Table with formatting
            table(
                table_row(
                    table_cell(paragraph(text("Milestone", bold=True))),
                    table_cell(paragraph(text("Due Date", bold=True))),
                    table_cell(paragraph(text("Completion", bold=True)))
                ),
                table_row(
                    table_cell(paragraph(text("Alpha Release", bold=True))),
                    "2025-11-01",
                    table_cell(paragraph(text("85%", italic=True)))
                ),
                table_row(
                    table_cell(paragraph(text("Beta Release", bold=True))),
                    "2025-11-15",
                    table_cell(paragraph(text("40%", italic=True)))
                ),
                table_row(
                    table_cell(paragraph(text("Production", bold=True))),
                    "2025-12-01",
                    table_cell(paragraph(text("10%", italic=True)))
                )
            ),
            
            heading(2, "Team Metrics"),
            
            table(
                table_row("Metric", "Value"),  # Header row
                table_row("Total Tasks", "47"),
                table_row("Completed", "28"),
                table_row("In Progress", "12"),
                table_row("Blocked", "3"),
                table_row("Overdue", "4")
            ),
            
            horizontal_rule(),
            
            paragraph(
                text("Generated with ", italic=True),
                text("table()", code=True),
                text(" helper function", italic=True)
            )
        ]
        
        # Replace document
        print("=== Creating document with tables ===")
        client.replace_json_document(
            document_id=document_id,
            content=content
        )
        print("✅ Document with tables created successfully!\n")
        
        print("📊 Content Summary:")
        print(f"   Total blocks: {len(content)}")
        print(f"   Tables: {sum(1 for c in content if c.get('type') == 'table')}")
        print(f"   Headings: {sum(1 for c in content if c.get('type') == 'heading')}")
        
        print(f"\n🎉 Check task {task_response.task.hrid} in Vaiz to see the tables!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

