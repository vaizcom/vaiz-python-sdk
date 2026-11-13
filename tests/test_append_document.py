"""
Tests for appendDocument and appendMarkdownDocument API endpoints.
"""

import pytest
from tests.test_config import get_test_client
from tests.lexical_utils import root_children
from vaiz.models import CreateTaskRequest, TaskPriority


def test_append_document():
    """Test appending plain text to existing document."""
    client = get_test_client()
    
    # Get first board
    boards = client.get_boards()
    if not boards or not boards.boards:
        pytest.skip("No boards available for testing")
    
    board = boards.boards[0]
    
    # Create task with initial content
    task_request = CreateTaskRequest(
        name="Test Append Plain Text",
        group=client.space_id,
        board=board.id,
        priority=TaskPriority.General,
        description="Initial content"
    )
    
    task_response = client.create_task(task_request)
    document_id = task_response.task.document
    
    # Verify initial content
    initial = client.get_json_document(document_id)
    initial_text = str(initial)
    assert "Initial content" in initial_text
    
    # Append additional content
    response = client.append_document(
        document_id=document_id,
        description="\n\nAppended content - this should be added to existing content"
    )
    
    assert response is not None
    
    # Verify both old and new content exist
    updated = client.get_json_document(document_id)
    updated_text = str(updated)
    
    assert "Initial content" in updated_text, "Original content should still exist"
    assert "Appended content" in updated_text, "New content should be added"
    
    print(f"✅ Successfully appended plain text to document")


def test_append_multiple_times():
    """Test appending content multiple times to same document."""
    client = get_test_client()
    
    # Get first board
    boards = client.get_boards()
    if not boards or not boards.boards:
        pytest.skip("No boards available for testing")
    
    board = boards.boards[0]
    
    # Create task
    task_request = CreateTaskRequest(
        name="Test Multiple Appends",
        group=client.space_id,
        board=board.id,
        priority=TaskPriority.General,
        description="Base content"
    )
    
    task_response = client.create_task(task_request)
    document_id = task_response.task.document
    
    # Append first time
    client.append_markdown_document(document_id, "First append")
    
    # Append second time
    client.append_markdown_document(document_id, "Second append")
    
    # Append third time
    client.append_markdown_document(document_id, "Third append")
    
    # Verify all appends, in order
    final_text = client.get_markdown_document(document_id)
    
    assert "Base content" in final_text
    assert "First append" in final_text
    assert "Second append" in final_text
    assert "Third append" in final_text
    assert (
        final_text.index("Base content")
        < final_text.index("First append")
        < final_text.index("Second append")
        < final_text.index("Third append")
    )
    
    print(f"✅ Successfully appended content 3 times")


def test_append_document_race_condition():
    """Test race condition handling for plain text append - verify order is preserved."""
    client = get_test_client()
    
    # Get first board
    boards = client.get_boards()
    if not boards or not boards.boards:
        pytest.skip("No boards available for testing")
    
    board = boards.boards[0]
    
    # Create task with marked initial content
    task_request = CreateTaskRequest(
        name="Test Plain Text Append Order",
        group=client.space_id,
        board=board.id,
        priority=TaskPriority.General,
        description="PLAIN_INITIAL_MARKER - Base content"
    )
    
    task_response = client.create_task(task_request)
    document_id = task_response.task.document
    
    # Verify initial content
    initial = client.get_json_document(document_id)
    initial_text = str(initial)
    assert "PLAIN_INITIAL_MARKER" in initial_text
    
    # Perform 3 rapid sequential plain text appends
    client.append_document(document_id, "\n\nPLAIN_APPEND_1_MARKER - First plain append")
    client.append_document(document_id, "\n\nPLAIN_APPEND_2_MARKER - Second plain append")
    client.append_document(document_id, "\n\nPLAIN_APPEND_3_MARKER - Third plain append")
    
    # Retrieve and verify
    final = client.get_json_document(document_id)
    final_text = str(final)
    
    # CRITICAL: All markers must be present
    assert "PLAIN_INITIAL_MARKER" in final_text, "Initial content missing!"
    assert "PLAIN_APPEND_1_MARKER" in final_text, "Plain append 1 missing!"
    assert "PLAIN_APPEND_2_MARKER" in final_text, "Plain append 2 missing!"
    assert "PLAIN_APPEND_3_MARKER" in final_text, "Plain append 3 missing!"
    
    # CRITICAL: Verify ORDER
    init_pos = final_text.find("PLAIN_INITIAL_MARKER")
    app1_pos = final_text.find("PLAIN_APPEND_1_MARKER")
    app2_pos = final_text.find("PLAIN_APPEND_2_MARKER")
    app3_pos = final_text.find("PLAIN_APPEND_3_MARKER")
    
    assert init_pos != -1 and app1_pos != -1 and app2_pos != -1 and app3_pos != -1
    
    # STRICT ORDER CHECK
    assert init_pos < app1_pos, f"INITIAL ({init_pos}) should come before APPEND_1 ({app1_pos})"
    assert app1_pos < app2_pos, f"APPEND_1 ({app1_pos}) should come before APPEND_2 ({app2_pos})"
    assert app2_pos < app3_pos, f"APPEND_2 ({app2_pos}) should come before APPEND_3 ({app3_pos})"
    
    print(f"✅ PLAIN TEXT RACE CONDITION TEST PASSED: All appends in correct order")
    print(f"   ✓ Correct order: INITIAL → APPEND_1 → APPEND_2 → APPEND_3")


def test_append_markdown_document_race_condition():
    """Test rapid sequential markdown appends - verify all are saved in order."""
    client = get_test_client()

    boards = client.get_boards()
    if not boards or not boards.boards:
        pytest.skip("No boards available for testing")

    board = boards.boards[0]

    task_request = CreateTaskRequest(
        name="Test Markdown Append Race Condition",
        group=client.space_id,
        board=board.id,
        priority=TaskPriority.General,
        description="INITIAL-MARKER - Base content"
    )

    task_response = client.create_task(task_request)
    document_id = task_response.task.document

    # Markers avoid underscores: Markdown export escapes them as backslash-underscore
    for number, label in enumerate(["First", "Second", "Third"], start=1):
        client.append_markdown_document(
            document_id, f"APPEND-{number}-MARKER - {label} append content"
        )

    final_text = client.get_markdown_document(document_id)
    positions = [
        final_text.find(marker)
        for marker in ("INITIAL-MARKER", "APPEND-1-MARKER", "APPEND-2-MARKER", "APPEND-3-MARKER")
    ]

    assert all(pos != -1 for pos in positions), f"A marker is missing - lost update! {final_text!r}"
    assert positions == sorted(positions), "Appends were saved out of order"

    # Each append is its own block
    final_blocks = root_children(client.get_json_document(document_id))
    assert len(final_blocks) >= 4, f"Expected at least 4 blocks, got {len(final_blocks)}"

    print("✅ MARKDOWN RACE CONDITION TEST PASSED: all appends saved in order")


if __name__ == "__main__":
    print("Running append document tests...")
    test_append_document()
    test_append_multiple_times()
    test_append_document_race_condition()
    test_append_markdown_document_race_condition()
    print("All tests passed! ✅")

