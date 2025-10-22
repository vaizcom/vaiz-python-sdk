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


if __name__ == "__main__":
    print("Running append document tests...")
    test_append_document()
    test_append_json_document()
    test_append_json_document_with_helpers()
    test_append_multiple_times()
    print("All tests passed! ✅")

