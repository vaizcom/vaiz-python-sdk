"""
Tests for Document Structure helper functions.
"""

import pytest
from tests.test_config import get_test_client
from vaiz.models import CreateTaskRequest, TaskPriority
from vaiz.helpers.document_structure import (
    text, paragraph, heading, bullet_list, ordered_list,
    list_item, link_text, separator, table, table_row, 
    table_cell
)


def test_document_structure_text_builder():
    """Test text node builder."""
    # Plain text
    node = text("Hello")
    assert node == {"type": "text", "text": "Hello"}
    
    # Bold text
    node = text("Bold", bold=True)
    assert node["marks"] == [{"type": "bold"}]
    
    # Italic text
    node = text("Italic", italic=True)
    assert node["marks"] == [{"type": "italic"}]
    
    # Code text
    node = text("code", code=True)
    assert node["marks"] == [{"type": "code"}]
    
    # Combined formatting
    node = text("Bold Italic", bold=True, italic=True)
    assert len(node["marks"]) == 2
    
    # Link
    node = text("Click here", link="https://vaiz.app")
    assert node["marks"][0]["type"] == "link"
    assert node["marks"][0]["attrs"]["href"] == "https://vaiz.app"


def test_document_structure_paragraph_builder():
    """Test paragraph node builder."""
    # Simple paragraph
    node = paragraph("Hello")
    assert node["type"] == "paragraph"
    assert node["content"][0]["text"] == "Hello"
    
    # Paragraph with mixed content
    node = paragraph(
        "Hello ",
        text("World", bold=True)
    )
    assert len(node["content"]) == 2
    assert node["content"][1]["marks"][0]["type"] == "bold"


def test_document_structure_heading_builder():
    """Test heading node builder."""
    # H1
    node = heading(1, "Title")
    assert node["type"] == "heading"
    assert node["attrs"]["level"] == 1
    assert node["content"][0]["text"] == "Title"
    
    # H2 with formatting
    node = heading(2, text("Subtitle", bold=True))
    assert node["attrs"]["level"] == 2


def test_document_structure_bullet_list_builder():
    """Test bullet list builder."""
    # Simple list
    node = bullet_list("First", "Second", "Third")
    assert node["type"] == "bulletList"
    assert len(node["content"]) == 3
    assert node["content"][0]["type"] == "listItem"
    
    # List with complex items
    node = bullet_list(
        list_item(paragraph(text("Bold item", bold=True))),
        "Simple item"
    )
    assert len(node["content"]) == 2


def test_document_structure_ordered_list_builder():
    """Test ordered list builder."""
    # Simple numbered list
    node = ordered_list("First", "Second", "Third")
    assert node["type"] == "orderedList"
    assert len(node["content"]) == 3
    
    # List starting from 5
    node = ordered_list("Item A", "Item B", start=5)
    assert node["attrs"]["start"] == 5


def test_document_structure_nested_lists():
    """Test nested list structures."""
    node = bullet_list(
        "Top level item",
        list_item(
            paragraph("Parent item"),
            bullet_list(
                "Nested item 1",
                "Nested item 2"
            )
        )
    )
    
    assert node["type"] == "bulletList"
    # Check nested structure exists
    assert node["content"][1]["content"][1]["type"] == "bulletList"


def test_document_structure_link_text_builder():
    """Test link text builder."""
    node = link_text("Visit Vaiz", "https://vaiz.app")
    assert node["type"] == "text"
    assert node["text"] == "Visit Vaiz"
    assert node["marks"][0]["type"] == "link"
    assert node["marks"][0]["attrs"]["href"] == "https://vaiz.app"
    
    # Bold link
    node = link_text("Bold Link", "https://example.com", bold=True)
    assert len(node["marks"]) == 2  # link + bold


def test_document_structure_separator_builder():
    """Test separator builder."""
    node = separator()
    assert node["type"] == "paragraph"
    assert "━" in node["content"][0]["text"]
    
    # Custom separator
    node = separator("—", 10)
    assert node["content"][0]["text"] == "—" * 10


def test_document_structure_table_builders():
    """Test table-related builders."""
    # Table cell
    cell = table_cell("Content")
    assert cell["type"] == "tableCell"
    assert cell["attrs"]["colspan"] == 1
    assert cell["attrs"]["rowspan"] == 1
    assert cell["content"][0]["type"] == "paragraph"
    
    # Table cell with colspan/rowspan
    cell_span = table_cell("Merged", colspan=2, rowspan=2)
    assert cell_span["attrs"]["colspan"] == 2
    assert cell_span["attrs"]["rowspan"] == 2
    
    # Table row with strings
    row = table_row("Cell 1", "Cell 2", "Cell 3")
    assert row["type"] == "tableRow"
    assert row["attrs"]["showRowNumbers"] == False
    assert len(row["content"]) == 3
    assert row["content"][0]["type"] == "tableCell"
    
    # Complete table
    tbl = table(
        table_row("Name", "Status"),  # Header row (first row)
        table_row("Task 1", "Done"),
        table_row("Task 2", "In Progress")
    )
    assert tbl["type"] == "extension-table"
    assert "uid" in tbl["attrs"]
    assert tbl["attrs"]["showRowNumbers"] == False
    assert len(tbl["content"]) == 3


def test_document_structure_table_with_formatting():
    """Test table with formatted content."""
    tbl = table(
        table_row(
            table_cell(paragraph(text("Name", bold=True))),
            table_cell(paragraph(text("Status", bold=True)))
        ),
        table_row(
            table_cell(paragraph(text("Task 1", bold=True))),
            table_cell("✅ Done")
        ),
        table_row(
            "Task 2",
            table_cell(paragraph(text("In Progress", italic=True)))
        )
    )
    
    assert tbl["type"] == "extension-table"
    assert len(tbl["content"]) == 3


def test_replace_json_document_with_helpers():
    """Test replace_json_document using helper functions."""
    client = get_test_client()
    
    # Get first board
    boards = client.get_boards()
    if not boards or not boards.boards:
        pytest.skip("No boards available for testing")
    
    board = boards.boards[0]
    
    # Create a test task
    task_request = CreateTaskRequest(
        name="Test Task with Helper Functions",
        group=client.space_id,
        board=board.id,
        priority=TaskPriority.General,
        description="Will be replaced"
    )
    
    task_response = client.create_task(task_request)
    document_id = task_response.task.document
    
    # Build content using helper functions
    content = [
        heading(1, "🎉 Created with Helpers"),
        
        paragraph(
            "This document was created using ",
            text("type-safe helper functions", bold=True),
            " from the Vaiz Python SDK!"
        ),
        
        heading(2, "✨ Features"),
        bullet_list(
            "Type-safe builders",
            "Readable code",
            list_item(
                paragraph("Nested lists with ", text("formatting", italic=True)),
                bullet_list(
                    "Subitem 1",
                    "Subitem 2"
                )
            )
        ),
        
        heading(2, "🔗 Links"),
        paragraph(
            "Visit ",
            link_text("Vaiz", "https://vaiz.app", bold=True)
        ),
        
        separator(),
        
    paragraph(
        text("Built with ", italic=True),
        text("document structure helpers", code=True)
    )
    ]
    
    # Replace document
    response = client.replace_json_document(
        document_id=document_id,
        content=content
    )
    
    assert response is not None
    
    # Verify
    updated_content = client.get_json_document(document_id)
    assert updated_content is not None
    
    print(f"✅ Successfully created document with helper functions")
    print(f"   Content blocks: {len(content)}")


def test_replace_json_document_with_table():
    """Test replace_json_document with table content."""
    client = get_test_client()
    
    # Get first board
    boards = client.get_boards()
    if not boards or not boards.boards:
        pytest.skip("No boards available for testing")
    
    board = boards.boards[0]
    
    # Create a test task
    task_request = CreateTaskRequest(
        name="Test Task with Table",
        group=client.space_id,
        board=board.id,
        priority=TaskPriority.General,
        description="Will be replaced with table"
    )
    
    task_response = client.create_task(task_request)
    document_id = task_response.task.document
    
    # Build content with table
    content = [
        heading(1, "Project Status"),
        paragraph("Current task status:"),
        table(
            table_row("Task", "Assignee", "Status"),  # Header row
            table_row("Design mockups", "John", "✅ Done"),
            table_row("API development", "Jane", "⏳ In Progress"),
            table_row("Documentation", "Mike", "📋 Todo")
        )
    ]
    
    # Replace document
    response = client.replace_json_document(
        document_id=document_id,
        content=content
    )
    
    assert response is not None
    
    # Verify
    updated_content = client.get_json_document(document_id)
    assert updated_content is not None
    
    print(f"✅ Successfully created document with table")


if __name__ == "__main__":
    print("Running Document Structure helpers tests...")
    test_document_structure_text_builder()
    test_document_structure_paragraph_builder()
    test_document_structure_heading_builder()
    test_document_structure_bullet_list_builder()
    test_document_structure_ordered_list_builder()
    test_document_structure_nested_lists()
    test_document_structure_link_text_builder()
    test_document_structure_separator_builder()
    test_document_structure_table_builders()
    test_document_structure_table_with_formatting()
    test_replace_json_document_with_helpers()
    test_replace_json_document_with_table()
    print("All tests passed! ✅")

