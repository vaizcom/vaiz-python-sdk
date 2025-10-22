"""
Tests for appendDocument and appendJSONDocument API endpoints.
"""

import pytest
from tests.test_config import get_test_client
from vaiz.models import CreateTaskRequest, TaskPriority
from vaiz import heading, paragraph, text, bullet_list


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


def test_append_json_document():
    """Test appending JSON content to existing document."""
    client = get_test_client()
    
    # Get first board
    boards = client.get_boards()
    if not boards or not boards.boards:
        pytest.skip("No boards available for testing")
    
    board = boards.boards[0]
    
    # Create task with initial content
    task_request = CreateTaskRequest(
        name="Test Append JSON",
        group=client.space_id,
        board=board.id,
        priority=TaskPriority.General,
        description="Initial paragraph"
    )
    
    task_response = client.create_task(task_request)
    document_id = task_response.task.document
    
    # Verify initial content
    initial = client.get_json_document(document_id)
    initial_text = str(initial)
    assert "Initial paragraph" in initial_text
    
    # Append JSON content
    appended_content = [
        {
            "type": "heading",
            "attrs": {"level": 2},
            "content": [
                {"type": "text", "text": "Appended Section"}
            ]
        },
        {
            "type": "paragraph",
            "content": [
                {"type": "text", "text": "This content was "},
                {"type": "text", "marks": [{"type": "bold"}], "text": "appended"},
                {"type": "text", "text": " to the document."}
            ]
        }
    ]
    
    response = client.append_json_document(
        document_id=document_id,
        content=appended_content
    )
    
    assert response is not None
    
    # Verify both old and new content exist
    updated = client.get_json_document(document_id)
    updated_text = str(updated)
    
    assert "Initial paragraph" in updated_text, "Original content should still exist"
    assert "Appended Section" in updated_text, "New heading should be added"
    assert "appended" in updated_text, "New content should be added"
    
    print(f"✅ Successfully appended JSON content to document")


def test_append_json_document_with_helpers():
    """Test appending JSON content using helper functions."""
    client = get_test_client()
    
    # Get first board
    boards = client.get_boards()
    if not boards or not boards.boards:
        pytest.skip("No boards available for testing")
    
    board = boards.boards[0]
    
    # Create task with initial content
    task_request = CreateTaskRequest(
        name="Test Append with Helpers",
        group=client.space_id,
        board=board.id,
        priority=TaskPriority.General,
        description="Original task description"
    )
    
    task_response = client.create_task(task_request)
    document_id = task_response.task.document
    
    # Append using helpers
    appended_content = [
        heading(2, "Updates"),
        paragraph(
            text("Update: ", bold=True),
            "Added new requirements"
        ),
        bullet_list(
            "Requirement 1",
            "Requirement 2",
            "Requirement 3"
        )
    ]
    
    response = client.append_json_document(
        document_id=document_id,
        content=appended_content
    )
    
    assert response is not None
    
    # Verify both contents
    updated = client.get_json_document(document_id)
    updated_text = str(updated)
    
    assert "Original task description" in updated_text
    assert "Updates" in updated_text
    assert "Requirement" in updated_text
    
    print(f"✅ Successfully appended content using helpers")


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
    client.append_json_document(
        document_id,
        [paragraph("First append")]
    )
    
    # Append second time
    client.append_json_document(
        document_id,
        [paragraph("Second append")]
    )
    
    # Append third time
    client.append_json_document(
        document_id,
        [paragraph("Third append")]
    )
    
    # Verify all appends
    final = client.get_json_document(document_id)
    final_text = str(final)
    
    assert "Base content" in final_text
    assert "First append" in final_text
    assert "Second append" in final_text
    assert "Third append" in final_text
    
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


def test_append_json_document_race_condition():
    """Test race condition handling - verify all 3 appends are saved correctly."""
    client = get_test_client()
    
    # Get first board
    boards = client.get_boards()
    if not boards or not boards.boards:
        pytest.skip("No boards available for testing")
    
    board = boards.boards[0]
    
    # Create task with marked initial content
    task_request = CreateTaskRequest(
        name="Test Append Race Condition",
        group=client.space_id,
        board=board.id,
        priority=TaskPriority.General,
        description="INITIAL_MARKER - Base content"
    )
    
    task_response = client.create_task(task_request)
    document_id = task_response.task.document
    
    # Verify initial content
    initial = client.get_json_document(document_id)
    initial_text = str(initial)
    assert "INITIAL_MARKER" in initial_text
    
    # Perform 3 rapid sequential appends with unique markers
    # Each append has a unique marker to verify it was saved
    
    # Append 1
    append1 = [
        {
            "type": "paragraph",
            "content": [
                {"type": "text", "text": "APPEND_1_MARKER - First append content"}
            ]
        }
    ]
    client.append_json_document(document_id, append1)
    
    # Append 2
    append2 = [
        {
            "type": "paragraph",
            "content": [
                {"type": "text", "text": "APPEND_2_MARKER - Second append content"}
            ]
        }
    ]
    client.append_json_document(document_id, append2)
    
    # Append 3
    append3 = [
        {
            "type": "paragraph",
            "content": [
                {"type": "text", "text": "APPEND_3_MARKER - Third append content"}
            ]
        }
    ]
    client.append_json_document(document_id, append3)
    
    # Retrieve final content and STRICTLY verify all markers present
    final = client.get_json_document(document_id)
    final_text = str(final)
    
    # CRITICAL: All 4 markers must be present (initial + 3 appends)
    assert "INITIAL_MARKER" in final_text, "Initial content missing - was overwritten!"
    assert "APPEND_1_MARKER" in final_text, "Append 1 missing - race condition or lost update!"
    assert "APPEND_2_MARKER" in final_text, "Append 2 missing - race condition or lost update!"
    assert "APPEND_3_MARKER" in final_text, "Append 3 missing - race condition or lost update!"
    
    # Count actual markers in content blocks to ensure they're in document structure
    final_blocks = final.get("default", {}).get("content", [])
    
    # Verify we have at least 4 blocks (could be more with formatting)
    # Initial paragraph + 3 appended paragraphs
    assert len(final_blocks) >= 4, f"Expected at least 4 blocks, got {len(final_blocks)}"
    
    # Detailed verification
    markers_found = {
        "INITIAL_MARKER": False,
        "APPEND_1_MARKER": False,
        "APPEND_2_MARKER": False,
        "APPEND_3_MARKER": False
    }
    
    for block in final_blocks:
        block_text = str(block)
        for marker in markers_found:
            if marker in block_text:
                markers_found[marker] = True
    
    # Assert all markers were found in actual blocks
    for marker, found in markers_found.items():
        assert found, f"{marker} not found in document blocks!"
    
    # CRITICAL: Verify ORDER of markers - they must appear in correct sequence
    # Find positions of each marker in the full text
    initial_pos = final_text.find("INITIAL_MARKER")
    append1_pos = final_text.find("APPEND_1_MARKER")
    append2_pos = final_text.find("APPEND_2_MARKER")
    append3_pos = final_text.find("APPEND_3_MARKER")
    
    # All positions must be valid
    assert initial_pos != -1
    assert append1_pos != -1
    assert append2_pos != -1
    assert append3_pos != -1
    
    # STRICT ORDER CHECK: INITIAL must come first, then APPEND_1, then APPEND_2, then APPEND_3
    assert initial_pos < append1_pos, f"INITIAL ({initial_pos}) should come before APPEND_1 ({append1_pos})"
    assert append1_pos < append2_pos, f"APPEND_1 ({append1_pos}) should come before APPEND_2 ({append2_pos})"
    assert append2_pos < append3_pos, f"APPEND_2 ({append2_pos}) should come before APPEND_3 ({append3_pos})"
    
    print(f"✅ RACE CONDITION TEST PASSED: All 3 appends saved correctly IN ORDER")
    print(f"   ✓ Initial content preserved (INITIAL_MARKER found)")
    print(f"   ✓ Append 1 saved (APPEND_1_MARKER found)")
    print(f"   ✓ Append 2 saved (APPEND_2_MARKER found)")
    print(f"   ✓ Append 3 saved (APPEND_3_MARKER found)")
    print(f"   ✓ Correct order: INITIAL → APPEND_1 → APPEND_2 → APPEND_3")
    print(f"   Total blocks: {len(final_blocks)}")


if __name__ == "__main__":
    print("Running append document tests...")
    test_append_document()
    test_append_json_document()
    test_append_json_document_with_helpers()
    test_append_multiple_times()
    test_append_document_race_condition()
    test_append_json_document_race_condition()
    print("All tests passed! ✅")

