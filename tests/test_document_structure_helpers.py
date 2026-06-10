"""
Tests for Document Structure helper functions.
"""

import pytest
from tests.test_config import get_test_client
from vaiz.models import CreateTaskRequest, TaskPriority
from vaiz.helpers.document_structure import (
    text, paragraph, heading, bullet_list, ordered_list,
    list_item, link_text, horizontal_rule, blockquote, details, 
    details_summary, details_content, table, table_row, table_cell
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


def test_document_structure_horizontal_rule_builder():
    """Test horizontal rule builder."""
    node = horizontal_rule()
    assert node["type"] == "horizontalRule"
    assert node == {"type": "horizontalRule"}


def test_document_structure_blockquote_builder():
    """Test blockquote builder."""
    # Simple blockquote
    node = blockquote("This is a quote")
    assert node["type"] == "blockquote"
    assert node["content"][0]["type"] == "paragraph"
    assert node["content"][0]["content"][0]["text"] == "This is a quote"
    
    # Blockquote with multiple paragraphs
    node = blockquote(
        paragraph("First line"),
        paragraph("Second line")
    )
    assert node["type"] == "blockquote"
    assert len(node["content"]) == 2
    
    # Blockquote with formatted text
    node = blockquote(
        paragraph(
            text("Important: ", bold=True),
            "This is a critical note"
        )
    )
    assert node["type"] == "blockquote"
    assert node["content"][0]["content"][0]["marks"][0]["type"] == "bold"


def test_document_structure_details_builder():
    """Test details (collapsible section) builder."""
    # Simple details with string summary
    node = details("Click to expand", paragraph("Hidden content"))
    assert node["type"] == "details"
    assert len(node["content"]) == 2
    assert node["content"][0]["type"] == "detailsSummary"
    assert node["content"][0]["content"][0]["text"] == "Click to expand"
    assert node["content"][1]["type"] == "detailsContent"
    
    # Details with formatted summary
    node = details(
        details_summary(text("Additional Info", bold=True)),
        details_content(paragraph("More information here"))
    )
    assert node["type"] == "details"
    assert node["content"][0]["type"] == "detailsSummary"
    assert node["content"][0]["content"][0]["marks"][0]["type"] == "bold"
    assert node["content"][1]["type"] == "detailsContent"
    
    # Details with multiple paragraphs in content
    node = details(
        "Summary",
        details_content(
            paragraph("First paragraph"),
            paragraph("Second paragraph")
        )
    )
    assert node["type"] == "details"
    assert node["content"][1]["type"] == "detailsContent"
    assert len(node["content"][1]["content"]) == 2
    
    # Details with simple string content (auto-wrapped)
    node = details("Summary", paragraph("Content"))
    assert node["type"] == "details"
    assert node["content"][1]["type"] == "detailsContent"


def test_document_structure_details_summary_builder():
    """Test details summary builder."""
    node = details_summary("Click to expand")
    assert node["type"] == "detailsSummary"
    assert node["content"][0]["text"] == "Click to expand"
    
    # With formatted text
    node = details_summary(text("Important", bold=True), " info")
    assert node["type"] == "detailsSummary"
    assert len(node["content"]) == 2
    assert node["content"][0]["marks"][0]["type"] == "bold"


def test_document_structure_details_content_builder():
    """Test details content builder."""
    node = details_content(paragraph("Hidden content"))
    assert node["type"] == "detailsContent"
    assert node["content"][0]["type"] == "paragraph"
    
    # With multiple paragraphs
    node = details_content(
        paragraph("First"),
        paragraph("Second")
    )
    assert node["type"] == "detailsContent"
    assert len(node["content"]) == 2


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


def test_document_structure_table_header():
    """Test table_header builder."""
    from vaiz import table_header
    
    # Simple table header
    header = table_header("Column Name")
    assert header["type"] == "tableHeader"
    assert header["attrs"]["colspan"] == 1
    assert header["attrs"]["rowspan"] == 1
    assert header["content"][0]["type"] == "paragraph"
    assert header["content"][0]["content"][0]["text"] == "Column Name"
    
    # Table header with colspan/rowspan
    header_span = table_header("Merged Header", colspan=3, rowspan=2)
    assert header_span["attrs"]["colspan"] == 3
    assert header_span["attrs"]["rowspan"] == 2
    
    # Table header with formatted text
    header_bold = table_header(paragraph(text("Name", bold=True)))
    assert header_bold["type"] == "tableHeader"
    assert header_bold["content"][0]["content"][0]["marks"][0]["type"] == "bold"
    
    # Complete table with table_header
    tbl = table(
        table_row(
            table_header("Name"),
            table_header("Status"),
            table_header("Priority")
        ),
        table_row("Task 1", "Done", "High"),
        table_row("Task 2", "In Progress", "Medium")
    )
    
    assert tbl["type"] == "extension-table"
    assert len(tbl["content"]) == 3
    
    # First row should have tableHeader cells
    first_row = tbl["content"][0]
    assert first_row["content"][0]["type"] == "tableHeader"
    assert first_row["content"][1]["type"] == "tableHeader"
    assert first_row["content"][2]["type"] == "tableHeader"
    
    # Second row should have tableCell cells
    second_row = tbl["content"][1]
    assert second_row["content"][0]["type"] == "tableCell"
    assert second_row["content"][1]["type"] == "tableCell"
    assert second_row["content"][2]["type"] == "tableCell"


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
        
        horizontal_rule(),
        
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


def test_create_comprehensive_document_with_all_features():
    """Test creating a large comprehensive document with all available features."""
    from vaiz import (
        heading, paragraph, text, 
        bullet_list, ordered_list, list_item,
        table, table_row, table_cell, table_header,
        horizontal_rule, blockquote, details, link_text
    )
    
    client = get_test_client()
    
    # Get first board
    boards = client.get_boards()
    if not boards or not boards.boards:
        pytest.skip("No boards available for testing")
    
    board = boards.boards[0]
    
    # Create a test task
    task_request = CreateTaskRequest(
        name="📚 Comprehensive Document - All Features Test",
        group=client.space_id,
        board=board.id,
        priority=TaskPriority.High,
        description="Testing all document structure features"
    )
    
    task_response = client.create_task(task_request)
    document_id = task_response.task.document
    
    # Build a comprehensive document with all features
    content = [
        # Header section
        heading(1, "📚 Comprehensive Documentation Example"),
        
        paragraph(
            "This document demonstrates ",
            text("all available features", bold=True),
            " of the Vaiz Python SDK document structure helpers. ",
            "Created on: ",
            text("2025-10-23", italic=True)
        ),
        
        horizontal_rule(),
        
        # Text formatting section
        heading(2, "✨ Text Formatting"),
        
        paragraph(
            "The SDK supports various text formatting options: ",
            text("bold text", bold=True),
            ", ",
            text("italic text", italic=True),
            ", ",
            text("inline code", code=True),
            ", and ",
            text("bold + italic", bold=True, italic=True),
            "."
        ),
        
        paragraph(
            "You can also create ",
            link_text("hyperlinks", "https://vaiz.app"),
            " with custom targets."
        ),
        
        horizontal_rule(),
        
        # Lists section
        heading(2, "📝 Lists"),
        
        heading(3, "Bullet Lists"),
        
        paragraph("Simple unordered list:"),
        
        bullet_list(
            "First item",
            "Second item with some detail",
            "Third item"
        ),
        
        paragraph("Nested bullet list with formatting:"),
        
        bullet_list(
            list_item(
                paragraph(text("Parent item 1", bold=True)),
                bullet_list(
                    "Nested item 1.1",
                    "Nested item 1.2"
                )
            ),
            list_item(
                paragraph(text("Parent item 2", bold=True)),
                bullet_list(
                    "Nested item 2.1",
                    list_item(
                        paragraph("Nested item 2.2 with sub-items:"),
                        bullet_list(
                            "Deep nested 2.2.1",
                            "Deep nested 2.2.2"
                        )
                    )
                )
            ),
            "Parent item 3 (no nesting)"
        ),
        
        heading(3, "Ordered Lists"),
        
        paragraph("Numbered steps:"),
        
        ordered_list(
            "Initialize the client",
            "Create a document request",
            "Build content using helpers",
            "Send the request to API",
            "Verify the response"
        ),
        
        paragraph("Custom start number:"),
        
        ordered_list(
            "Step 10",
            "Step 11", 
            "Step 12",
            start=10
        ),
        
        horizontal_rule(),
        
        # Tables section
        heading(2, "📊 Tables"),
        
        heading(3, "Simple Table with Headers"),
        
        paragraph("Basic table using ", text("table_header()", code=True), ":"),
        
        table(
            table_row(
                table_header("Feature"),
                table_header("Status"),
                table_header("Version"),
                table_header("Priority")
            ),
            table_row(
                "Document helpers",
                text("✅ Complete", bold=True),
                "0.8.0",
                "High"
            ),
            table_row(
                "Table headers",
                text("✅ Complete", bold=True),
                "0.9.0",
                "High"
            ),
            table_row(
                "Custom fields",
                text("✅ Complete", bold=True),
                "0.7.0",
                "Medium"
            ),
            table_row(
                "File uploads",
                text("✅ Complete", bold=True),
                "0.6.0",
                "Medium"
            )
        ),
        
        heading(3, "Complex Table with Merged Cells"),
        
        paragraph("Table with colspan and rowspan:"),
        
        table(
            # Main header
            table_row(
                table_header(paragraph(text("Q1-Q4 2025 Roadmap", bold=True)), colspan=6)
            ),
            # Subheaders
            table_row(
                table_header("Quarter"),
                table_header("Month"),
                table_header("Feature"),
                table_header("Team"),
                table_header("Status"),
                table_header("Progress")
            ),
            # Q1 data
            table_row(
                table_cell(paragraph(text("Q1", bold=True)), rowspan=3),
                "January",
                "API v2 Migration",
                "Backend",
                "✅ Done",
                "100%"
            ),
            table_row(
                "February",
                "UI Redesign",
                "Frontend",
                "✅ Done",
                "100%"
            ),
            table_row(
                "March",
                "Mobile App",
                "Mobile",
                "✅ Done",
                "100%"
            ),
            # Q2 data
            table_row(
                table_cell(paragraph(text("Q2", bold=True)), rowspan=2),
                "April",
                "Performance Optimization",
                "DevOps",
                "⏳ In Progress",
                "75%"
            ),
            table_row(
                "May",
                "Analytics Dashboard",
                "Data",
                "📋 Planned",
                "0%"
            ),
            # Summary
            table_row(
                table_cell(paragraph(text("Summary", bold=True)), colspan=4),
                table_cell(paragraph(text("5 features", bold=True))),
                table_cell(paragraph(text("75% complete", bold=True)))
            )
        ),
        
        heading(3, "Wide Table (Many Columns)"),
        
        paragraph("Table with 8 columns:"),
        
        table(
            table_row(
                table_header("#"),
                table_header("Name"),
                table_header("Role"),
                table_header("Team"),
                table_header("Location"),
                table_header("Status"),
                table_header("Start Date"),
                table_header("Projects")
            ),
            table_row("1", "John Doe", "Backend Dev", "API", "🇺🇸 USA", "Active", "2023-01", "5"),
            table_row("2", "Jane Smith", "Frontend Dev", "UI", "🇬🇧 UK", "Active", "2023-03", "8"),
            table_row("3", "Mike Johnson", "DevOps", "Infra", "🇩🇪 DE", "Active", "2023-06", "3"),
            table_row("4", "Sarah Williams", "Designer", "UX", "🇫🇷 FR", "Active", "2024-01", "12"),
            table_row("5", "Tom Brown", "QA Engineer", "Test", "🇯🇵 JP", "Active", "2024-03", "6"),
            table_row(
                table_cell(paragraph(text("Total", bold=True)), colspan=7),
                table_cell(paragraph(text("34 projects", bold=True)))
            )
        ),
        
        horizontal_rule(),
        
        # Details (collapsible) section
        heading(2, "📂 Collapsible Sections (Details)"),
        
        paragraph("Simple collapsible section:"),
        
        details(
            "Click to expand",
            paragraph("This content is hidden by default and can be expanded.")
        ),
        
        paragraph("Details with formatted content:"),
        
        details(
            "Technical Details",
            paragraph(
                text("API Endpoint: ", bold=True),
                text("/api/v1/documents", code=True)
            ),
            paragraph(
                text("Method: ", bold=True),
                "POST"
            ),
            paragraph(
                text("Authentication: ", bold=True),
                "Bearer token required"
            )
        ),
        
        horizontal_rule(),
        
        # Blockquote section
        heading(2, "💬 Blockquotes"),
        
        paragraph("Simple blockquote:"),
        
        blockquote(
            paragraph(
                text("Note: ", bold=True),
                "This is an important callout or quote that stands out from regular content."
            )
        ),
        
        paragraph("Blockquote with multiple paragraphs:"),
        
        blockquote(
            paragraph(
                text("First principle: ", bold=True),
                "Always write clean, maintainable code."
            ),
            paragraph(
                text("Second principle: ", bold=True),
                "Documentation is as important as the code itself."
            ),
            paragraph(
                "— The Clean Code Philosophy"
            )
        ),
        
        horizontal_rule(),
        
        # Mixed content section
        heading(2, "🎨 Mixed Content"),
        
        paragraph(
            text("Complex paragraph", bold=True),
            " with ",
            text("multiple", italic=True),
            " ",
            text("formatting", code=True),
            " options and a ",
            link_text("link to documentation", "https://docs.vaiz.app", bold=True),
            "."
        ),
        
        bullet_list(
            list_item(
                paragraph("List item with inline ", text("bold", bold=True), " and ", text("code", code=True)),
            ),
            list_item(
                paragraph("List item with ", link_text("a link", "https://vaiz.app")),
            ),
            list_item(
                paragraph(
                    "Complex item: ",
                    text("bold", bold=True),
                    " + ",
                    text("italic", italic=True),
                    " + ",
                    text("code", code=True)
                )
            )
        ),
        
        horizontal_rule(),
        
        # Summary section
        heading(2, "📋 Summary"),
        
        paragraph(text("This document demonstrates:", bold=True)),
        
        ordered_list(
            "6 heading levels (H1-H6)",
            "Text formatting: bold, italic, code, links",
            "Bullet lists (simple and nested)",
            "Ordered lists (with custom start numbers)",
            "Blockquotes (simple and multi-paragraph)",
            "Details (collapsible sections)",
            "Tables with header cells (table_header)",
            "Complex tables with colspan and rowspan",
            "Wide tables with many columns",
            "Horizontal rules (dividers)",
            "Mixed content with multiple formatting"
        ),
        
        horizontal_rule(),
        
        # Footer
        paragraph(
            text("Created with: ", italic=True),
            text("Vaiz Python SDK v0.9.0+", code=True)
        ),
        
        paragraph(
            text("GitHub: ", bold=True),
            link_text("vaiz-python-sdk", "https://github.com/vaiz/vaiz-python-sdk")
        ),
    ]
    
    # Replace document content
    response = client.replace_json_document(document_id, content)
    assert response is not None
    
    # Verify the document was created successfully via markdown round-trip
    saved = client.get_json_document(document_id)
    assert "root" in saved

    markdown = client.get_markdown_document(document_id)
    lines = markdown.splitlines()

    # Count different element types from rendered markdown
    headings = sum(1 for l in lines if l.lstrip().startswith("#"))
    paragraphs = sum(
        1 for l in lines
        if l.strip() and not l.lstrip().startswith(("#", ">", "-", "|", "1.", "2.", "3."))
    )
    table_separators = sum(
        1 for l in lines
        if l.strip().startswith("|") and "---" in l
    )
    bullet_items = sum(1 for l in lines if l.lstrip().startswith("- "))
    ordered_items = sum(1 for l in lines if l.lstrip()[:3] in ("1. ", "2. ", "3. "))
    blockquote_lines = sum(1 for l in lines if l.lstrip().startswith(">"))

    # Verify we have a good variety of content
    assert headings >= 8, f"Expected at least 8 headings, got {headings}"
    assert paragraphs >= 10, f"Expected at least 10 paragraphs, got {paragraphs}"
    assert table_separators >= 3, f"Expected at least 3 tables, got {table_separators}"
    assert bullet_items >= 5, f"Expected at least 5 bullet items, got {bullet_items}"
    assert ordered_items >= 4, f"Expected at least 4 ordered items, got {ordered_items}"
    assert blockquote_lines >= 2, f"Expected at least 2 blockquote lines, got {blockquote_lines}"

    # Details blocks content survives the round-trip as plain text
    assert "First principle:" in markdown
    assert "Second principle:" in markdown

    print("✅ Comprehensive document created successfully")
    print(f"   Headings: {headings}")
    print(f"   Paragraphs: {paragraphs}")
    print(f"   Tables: {table_separators}")
    print(f"   Bullet items: {bullet_items}")
    print(f"   Ordered items: {ordered_items}")
    print(f"   Blockquote lines: {blockquote_lines}")
    print(f"   Document ID: {document_id}")


if __name__ == "__main__":
    print("Running Document Structure helpers tests...")
    test_document_structure_text_builder()
    test_document_structure_paragraph_builder()
    test_document_structure_heading_builder()
    test_document_structure_bullet_list_builder()
    test_document_structure_ordered_list_builder()
    test_document_structure_nested_lists()
    test_document_structure_link_text_builder()
    test_document_structure_horizontal_rule_builder()
    test_document_structure_blockquote_builder()
    test_document_structure_details_builder()
    test_document_structure_details_summary_builder()
    test_document_structure_details_content_builder()
    test_document_structure_table_builders()
    test_document_structure_table_with_formatting()
    test_replace_json_document_with_helpers()
    test_replace_json_document_with_table()
    print("All tests passed! ✅")

