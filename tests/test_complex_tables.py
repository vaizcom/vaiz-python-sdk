"""
Tests for complex table structures with colspan, rowspan, and multiple columns.
"""

import pytest
from tests.test_config import get_test_client
from vaiz.models import CreateTaskRequest, TaskPriority
from vaiz import heading, paragraph, text, table, table_row, table_cell, table_header, horizontal_rule


def test_create_complex_table_with_colspan():
    """Test creating table with merged cells (colspan)."""
    client = get_test_client()
    
    # Get first board
    boards = client.get_boards()
    if not boards or not boards.boards:
        pytest.skip("No boards available for testing")
    
    board = boards.boards[0]
    
    # Create task
    task_request = CreateTaskRequest(
        name="Test Complex Table with Colspan",
        group=client.space_id,
        board=board.id,
        priority=TaskPriority.General,
        description=""
    )
    
    task_response = client.create_task(task_request)
    document_id = task_response.task.document
    
    # Build complex table with colspan
    content = [
        heading(1, "Project Quarterly Report"),
        
        paragraph("Quarterly performance metrics:"),
        
        table(
            # Header row with merged cell using table_header
            table_row(
                table_header(paragraph(text("Metric", bold=True))),
                table_header(paragraph(text("Q1-Q4 Performance", bold=True)), colspan=4)  # Spans 4 columns
            ),
            # Subheader row
            table_row(
                table_header(paragraph(text("Category", bold=True))),
                table_header("Q1"),
                table_header("Q2"),
                table_header("Q3"),
                table_header("Q4")
            ),
            # Data rows
            table_row("Revenue", "$100K", "$120K", "$150K", "$180K"),
            table_row("Users", "1,000", "1,500", "2,200", "3,000"),
            table_row("Growth %", "20%", "25%", "30%", "35%"),
            # Summary row with merged cell
            table_row(
                table_cell(paragraph(text("Total Revenue", bold=True))),
                table_cell(paragraph(text("$550K", bold=True)), colspan=4)
            )
        )
    ]
    
    response = client.replace_json_document(document_id, content)
    assert response is not None
    
    # Verify table saved
    saved = client.get_json_document(document_id)
    saved_text = str(saved)
    
    assert "extension-table" in saved_text
    assert "Q1-Q4 Performance" in saved_text
    assert "colspan" in saved_text
    
    print(f"✅ Complex table with colspan created successfully")


def test_create_complex_table_with_rowspan():
    """Test creating table with cells spanning multiple rows."""
    client = get_test_client()
    
    # Get first board
    boards = client.get_boards()
    if not boards or not boards.boards:
        pytest.skip("No boards available for testing")
    
    board = boards.boards[0]
    
    # Create task
    task_request = CreateTaskRequest(
        name="Test Complex Table with Rowspan",
        group=client.space_id,
        board=board.id,
        priority=TaskPriority.General,
        description=""
    )
    
    task_response = client.create_task(task_request)
    document_id = task_response.task.document
    
    # Build table with rowspan
    content = [
        heading(1, "Team Structure"),
        
        table(
            # Header row using table_header
            table_row(
                table_header("Department"),
                table_header("Role"),
                table_header("Name"),
                table_header("Status")
            ),
            # Engineering department (3 rows)
            table_row(
                table_cell(paragraph(text("Engineering", bold=True)), rowspan=3),  # Spans 3 rows
                "Backend Developer",
                "John Doe",
                "✅ Active"
            ),
            table_row(
                "Frontend Developer",
                "Jane Smith",
                "✅ Active"
            ),
            table_row(
                "DevOps Engineer",
                "Bob Wilson",
                "✅ Active"
            ),
            # Design department (2 rows)
            table_row(
                table_cell(paragraph(text("Design", bold=True)), rowspan=2),  # Spans 2 rows
                "UI Designer",
                "Alice Brown",
                "✅ Active"
            ),
            table_row(
                "UX Researcher",
                "Charlie Davis",
                "⏳ Onboarding"
            )
        )
    ]
    
    response = client.replace_json_document(document_id, content)
    assert response is not None
    
    # Verify
    saved = client.get_json_document(document_id)
    saved_text = str(saved)
    
    assert "rowspan" in saved_text
    assert "Engineering" in saved_text
    assert "Design" in saved_text
    
    print(f"✅ Complex table with rowspan created successfully")


def test_create_large_table_many_columns():
    """Test creating table with many columns (10+)."""
    client = get_test_client()
    
    # Get first board
    boards = client.get_boards()
    if not boards or not boards.boards:
        pytest.skip("No boards available for testing")
    
    board = boards.boards[0]
    
    # Create task
    task_request = CreateTaskRequest(
        name="Test Large Table (Many Columns)",
        group=client.space_id,
        board=board.id,
        priority=TaskPriority.General,
        description=""
    )
    
    task_response = client.create_task(task_request)
    document_id = task_response.task.document
    
    # Build wide table with 12 columns (monthly data)
    content = [
        heading(1, "Annual Performance Dashboard"),
        
        paragraph("Monthly metrics for 2025:"),
        
        table(
            # Header row - 12 months using table_header
            table_row(
                table_header(paragraph(text("Metric", bold=True))),
                table_header("Jan"), table_header("Feb"), table_header("Mar"),
                table_header("Apr"), table_header("May"), table_header("Jun"),
                table_header("Jul"), table_header("Aug"), table_header("Sep"),
                table_header("Oct"), table_header("Nov"), table_header("Dec")
            ),
            # Revenue row
            table_row(
                table_cell(paragraph(text("Revenue ($K)", bold=True))),
                "45", "48", "52", "55", "60", "65",
                "70", "75", "82", "88", "95", "100"
            ),
            # Users row
            table_row(
                table_cell(paragraph(text("Active Users", bold=True))),
                "1.2K", "1.3K", "1.5K", "1.7K", "2.0K", "2.3K",
                "2.6K", "3.0K", "3.5K", "4.0K", "4.5K", "5.0K"
            ),
            # Growth row
            table_row(
                table_cell(paragraph(text("Growth %", bold=True))),
                "5", "6", "8", "6", "9", "8",
                "8", "7", "17", "14", "13", "11"
            )
        ),
        
        paragraph(
            text("Total Revenue: ", bold=True),
            text("$835K", italic=True)
        )
    ]
    
    response = client.replace_json_document(document_id, content)
    assert response is not None
    
    # Verify
    saved = client.get_json_document(document_id)
    saved_blocks = saved.get("default", {}).get("content", [])
    
    # Find table
    tables = [b for b in saved_blocks if b.get("type") == "extension-table"]
    assert len(tables) > 0, "Table not found"
    
    # Verify table has rows
    table_content = tables[0].get("content", [])
    assert len(table_content) == 4, f"Expected 4 rows (header + 3 data), got {len(table_content)}"
    
    # Verify first row has 13 cells (Metric + 12 months)
    first_row = table_content[0].get("content", [])
    assert len(first_row) == 13, f"Expected 13 columns, got {len(first_row)}"
    
    print(f"✅ Large table with 13 columns created successfully")


def test_create_complex_table_with_formatting():
    """Test table with mixed colspan, rowspan, and rich formatting."""
    client = get_test_client()
    
    # Get first board
    boards = client.get_boards()
    if not boards or not boards.boards:
        pytest.skip("No boards available for testing")
    
    board = boards.boards[0]
    
    # Create task
    task_request = CreateTaskRequest(
        name="Test Ultra Complex Table",
        group=client.space_id,
        board=board.id,
        priority=TaskPriority.General,
        description=""
    )
    
    task_response = client.create_task(task_request)
    document_id = task_response.task.document
    
    # Build ultra complex table
    content = [
        heading(1, "Project Status Matrix"),
        
        table(
            # Header with merged cell using table_header
            table_row(
                table_header(paragraph(text("Project Dashboard", bold=True)), colspan=5)
            ),
            # Subheader using table_header
            table_row(
                table_header(paragraph(text("Phase", bold=True))),
                table_header(paragraph(text("Tasks", bold=True))),
                table_header(paragraph(text("Status", bold=True))),
                table_header(paragraph(text("Owner", bold=True))),
                table_header(paragraph(text("Due", bold=True)))
            ),
            # Phase 1 - 3 tasks (rowspan for phase)
            table_row(
                table_cell(paragraph(text("Phase 1: Design", bold=True)), rowspan=3),
                "UI Mockups",
                table_cell(paragraph(text("Done", italic=True))),
                "John",
                "Oct 15"
            ),
            table_row(
                "Wireframes",
                table_cell(paragraph(text("Done", italic=True))),
                "Jane",
                "Oct 18"
            ),
            table_row(
                "Style Guide",
                table_cell(paragraph(text("In Progress", italic=True))),
                "Mike",
                "Oct 25"
            ),
            # Phase 2 - 2 tasks
            table_row(
                table_cell(paragraph(text("Phase 2: Development", bold=True)), rowspan=2),
                "API Implementation",
                table_cell(paragraph(text("In Progress", italic=True))),
                "Sarah",
                "Nov 5"
            ),
            table_row(
                "Frontend Integration",
                table_cell(paragraph(text("Todo", italic=True))),
                "Tom",
                "Nov 10"
            ),
            # Summary row with merged cells
            table_row(
                table_cell(paragraph(text("Total Progress", bold=True)), colspan=2),
                table_cell(paragraph(text("40% Complete", bold=True, italic=True)), colspan=3)
            )
        ),
        
        horizontal_rule(),
        
        paragraph(
            text("Legend: ", bold=True),
            text("Done", italic=True), " | ",
            text("In Progress", italic=True), " | ",
            text("Todo", italic=True)
        )
    ]
    
    response = client.replace_json_document(document_id, content)
    assert response is not None
    
    # Verify complex structure
    saved = client.get_json_document(document_id)
    saved_text = str(saved)
    
    assert "extension-table" in saved_text
    assert "colspan" in saved_text
    assert "rowspan" in saved_text
    assert "Project Dashboard" in saved_text
    assert "Phase 1: Design" in saved_text
    assert "Phase 2: Development" in saved_text
    
    # Verify table structure
    saved_blocks = saved.get("default", {}).get("content", [])
    tables = [b for b in saved_blocks if b.get("type") == "extension-table"]
    assert len(tables) > 0
    
    table_rows = tables[0].get("content", [])
    assert len(table_rows) >= 7, f"Expected at least 7 rows, got {len(table_rows)}"
    
    print(f"✅ Ultra complex table with colspan, rowspan, and formatting created")
    print(f"   Rows: {len(table_rows)}")
    print(f"   Features: colspan, rowspan, bold, italic")


def test_append_multiple_complex_tables():
    """Test appending multiple tables to same document."""
    client = get_test_client()
    
    # Get first board
    boards = client.get_boards()
    if not boards or not boards.boards:
        pytest.skip("No boards available for testing")
    
    board = boards.boards[0]
    
    # Create task
    task_request = CreateTaskRequest(
        name="Test Multiple Tables via Append",
        group=client.space_id,
        board=board.id,
        priority=TaskPriority.General,
        description="Initial description with base info"
    )
    
    task_response = client.create_task(task_request)
    document_id = task_response.task.document
    
    # Append first table - Sprint metrics
    table1 = [
        horizontal_rule(),
        heading(2, "📊 Sprint Metrics"),
        table(
            table_row("Sprint", "Velocity", "Completed", "Carry Over"),
            table_row("Sprint 1", "25", "23", "2"),
            table_row("Sprint 2", "28", "26", "2"),
            table_row("Sprint 3", "30", "30", "0")
        )
    ]
    client.append_json_document(document_id, table1)
    
    # Append second table - Team allocation
    table2 = [
        horizontal_rule(),
        heading(2, "👥 Team Allocation"),
        table(
            table_row(
                table_header("Team"),
                table_header("Frontend"),
                table_header("Backend"),
                table_header("QA"),
                table_header("Total")
            ),
            table_row("Team A", "3", "2", "1", "6"),
            table_row("Team B", "2", "3", "1", "6"),
            table_row(
                table_cell(paragraph(text("Total", bold=True))),
                table_cell("5"),
                table_cell("5"),
                table_cell("2"),
                table_cell(paragraph(text("12", bold=True)))
            )
        )
    ]
    client.append_json_document(document_id, table2)
    
    # Append third table - Budget breakdown with merged cells
    table3 = [
        horizontal_rule(),
        heading(2, "💰 Budget Breakdown"),
        table(
            table_row(
                table_header(paragraph(text("Category", bold=True))),
                table_header(paragraph(text("2025 Budget", bold=True)), colspan=2)
            ),
            table_row(
                table_header(""),
                table_header("Planned"),
                table_header("Actual")
            ),
            table_row("Development", "$200K", "$180K"),
            table_row("Marketing", "$100K", "$95K"),
            table_row("Operations", "$50K", "$48K"),
            table_row(
                table_cell(paragraph(text("Total", bold=True))),
                table_cell(paragraph(text("$350K", bold=True))),
                table_cell(paragraph(text("$323K", bold=True)))
            )
        )
    ]
    client.append_json_document(document_id, table3)
    
    # Verify all 3 tables present
    saved = client.get_json_document(document_id)
    saved_blocks = saved.get("default", {}).get("content", [])
    
    tables = [b for b in saved_blocks if b.get("type") == "extension-table"]
    assert len(tables) == 3, f"Expected 3 tables, found {len(tables)}"
    
    saved_text = str(saved)
    assert "Sprint Metrics" in saved_text
    assert "Team Allocation" in saved_text
    assert "Budget Breakdown" in saved_text
    
    print(f"✅ Successfully appended 3 complex tables")
    print(f"   Table 1: Sprint metrics (4 columns)")
    print(f"   Table 2: Team allocation (5 columns)")
    print(f"   Table 3: Budget breakdown (3 columns, with colspan)")


def test_create_nested_table_structure():
    """Test creating document with table nested within other content."""
    client = get_test_client()
    
    # Get first board
    boards = client.get_boards()
    if not boards or not boards.boards:
        pytest.skip("No boards available for testing")
    
    board = boards.boards[0]
    
    # Create task
    task_request = CreateTaskRequest(
        name="Test Nested Table Structure",
        group=client.space_id,
        board=board.id,
        priority=TaskPriority.General,
        description=""
    )
    
    task_response = client.create_task(task_request)
    document_id = task_response.task.document
    
    # Build complex nested structure
    from vaiz import bullet_list, ordered_list
    
    content = [
        heading(1, "Project Documentation"),
        
        paragraph("Overview of project status and metrics."),
        
        heading(2, "Key Milestones"),
        bullet_list(
            "Phase 1: Planning - Complete",
            "Phase 2: Development - In Progress",
            "Phase 3: Testing - Upcoming"
        ),
        
        heading(2, "Current Sprint Tasks"),
        
        table(
            table_row(
                table_header("ID"),
                table_header("Task"),
                table_header("Assignee"),
                table_header("Priority"),
                table_header("Status"),
                table_header("Hours")
            ),
            table_row("T-001", "API Integration", "John", "High", "✅ Done", "8"),
            table_row("T-002", "UI Polish", "Jane", "Medium", "⏳ Progress", "12"),
            table_row("T-003", "Documentation", "Mike", "Low", "📋 Todo", "6"),
            table_row(
                table_cell(paragraph(text("Total", bold=True)), colspan=5),
                table_cell(paragraph(text("26 hours", bold=True)))
            )
        ),
        
        heading(2, "Next Steps"),
        ordered_list(
            "Review completed tasks",
            "Update sprint board",
            "Plan next iteration"
        ),
        
        horizontal_rule(),
        
        paragraph(
            text("Document created with ", italic=True),
            text("replace_json_document()", code=True),
            text(" and document structure helpers", italic=True)
        )
    ]
    
    response = client.replace_json_document(document_id, content)
    assert response is not None
    
    # Verify structure
    saved = client.get_json_document(document_id)
    saved_blocks = saved.get("default", {}).get("content", [])
    
    # Count different element types
    headings = sum(1 for b in saved_blocks if b.get("type") == "heading")
    tables = sum(1 for b in saved_blocks if b.get("type") == "extension-table")
    bullet_lists = sum(1 for b in saved_blocks if b.get("type") == "bulletList")
    ordered_lists = sum(1 for b in saved_blocks if b.get("type") == "orderedList")
    
    assert headings >= 3, "Should have at least 3 headings"
    assert tables >= 1, "Should have at least 1 table"
    assert bullet_lists >= 1, "Should have bullet list"
    assert ordered_lists >= 1, "Should have ordered list"
    
    print(f"✅ Complex nested structure with table created")
    print(f"   Headings: {headings}")
    print(f"   Tables: {tables}")
    print(f"   Bullet lists: {bullet_lists}")
    print(f"   Ordered lists: {ordered_lists}")
    print(f"   Total blocks: {len(saved_blocks)}")


if __name__ == "__main__":
    print("Running complex table tests...")
    test_create_complex_table_with_colspan()
    test_create_complex_table_with_rowspan()
    test_create_large_table_many_columns()
    test_append_multiple_complex_tables()
    test_create_nested_table_structure()
    print("All tests passed! ✅")

