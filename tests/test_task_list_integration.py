"""
Integration tests for task lists (checklists) in real documents and tasks.
"""

import pytest
import sys
import os

# Add tests directory to path for test_config import
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from test_config import get_test_client, TEST_BOARD_ID, TEST_GROUP_ID
from vaiz import (
    CreateTaskRequest,
    heading,
    paragraph,
    task_list,
    task_item,
)


def get_client():
    """Get test client."""
    return get_test_client()


def get_board_id():
    """Get test board ID."""
    if not TEST_BOARD_ID:
        pytest.skip("TEST_BOARD_ID not set in environment")
    return TEST_BOARD_ID


def get_group_id():
    """Get test group ID."""
    if not TEST_GROUP_ID:
        pytest.skip("TEST_GROUP_ID not set in environment")
    return TEST_GROUP_ID


@pytest.mark.integration
def test_create_task_with_simple_checklist():
    """Test creating a real task with a simple checklist in description."""
    client = get_client()
    board_id = get_board_id()
    group_id = get_group_id()
    
    # Create task first
    request = CreateTaskRequest(
        name="Test Task with Checklist",
        board=board_id,
        group=group_id,
    )
    
    response = client.create_task(request)
    task_id = response.task.id
    document_id = response.task.document
    
    # Verify task was created
    assert task_id is not None
    assert response.task.name == "Test Task with Checklist"
    
    # Now add checklist content to the task description
    content = [
        heading(1, "Sprint Tasks"),
        paragraph("Here's what needs to be done:"),
        task_list(
            task_item("Review pull requests", checked=True),
            task_item("Update documentation", checked=False),
            task_item("Deploy to production", checked=False),
        )
    ]
    
    client.replace_json_document(document_id, content)
    
    # Fetch task and verify content
    task = client.get_task(task_id)
    doc_content = client.get_json_document(task.task.document)
    
    # Verify structure
    assert "default" in doc_content
    content_blocks = doc_content["default"]["content"]
    
    # Find task list block
    task_list_block = None
    for block in content_blocks:
        if block.get("type") == "taskList":
            task_list_block = block
            break
    
    assert task_list_block is not None, "Task list block not found in document"
    assert len(task_list_block["content"]) == 3
    
    # Verify task items
    items = task_list_block["content"]
    assert items[0]["attrs"]["checked"] == True
    assert items[1]["attrs"]["checked"] == False
    assert items[2]["attrs"]["checked"] == False
    
    print(f"✅ Created task with checklist: {task_id}")
    return task_id


@pytest.mark.integration
def test_create_task_with_nested_checklist():
    """Test creating a task with nested multi-level checklist."""
    client = get_client()
    board_id = get_board_id()
    group_id = get_group_id()
    
    # Create task first
    request = CreateTaskRequest(
        name="Project with Nested Checklist",
        board=board_id,
        group=group_id,
    )
    
    response = client.create_task(request)
    task_id = response.task.id
    document_id = response.task.document
    
    # Verify task was created
    assert task_id is not None
    
    # Create nested checklist content
    content = [
        heading(1, "Project Milestones"),
        task_list(
            task_item(
                paragraph("Phase 1: Planning"),
                task_list(
                    task_item("Define requirements", checked=True),
                    task_item("Create wireframes", checked=True),
                    task_item("Review with stakeholders", checked=False)
                ),
                checked=True
            ),
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
                        ),
                        checked=False
                    )
                ),
                checked=False
            ),
        )
    ]
    
    # Update task description with nested checklist
    client.replace_json_document(document_id, content)
    
    # Fetch and verify structure
    task = client.get_task(task_id)
    doc_content = client.get_json_document(task.task.document)
    
    # Verify nested structure exists
    assert "default" in doc_content
    content_blocks = doc_content["default"]["content"]
    
    # Find main task list
    main_task_list = None
    for block in content_blocks:
        if block.get("type") == "taskList":
            main_task_list = block
            break
    
    assert main_task_list is not None
    assert len(main_task_list["content"]) == 2
    
    # Verify first item has nested list
    first_item = main_task_list["content"][0]
    assert first_item["attrs"]["checked"] == True
    
    # Find nested task list in first item
    nested_list = None
    for item in first_item["content"]:
        if isinstance(item, dict) and item.get("type") == "taskList":
            nested_list = item
            break
    
    assert nested_list is not None
    assert len(nested_list["content"]) == 3
    
    print(f"✅ Created task with nested checklist: {task_id}")
    return task_id


@pytest.mark.integration
def test_update_task_with_checklist():
    """Test updating an existing task to add a checklist."""
    client = get_client()
    board_id = get_board_id()
    group_id = get_group_id()
    
    # Create simple task first
    request = CreateTaskRequest(
        name="Task to Update with Checklist",
        board=board_id,
        group=group_id
    )
    
    response = client.create_task(request)
    task_id = response.task.id
    document_id = response.task.document
    
    # Update with checklist
    new_content = [
        heading(1, "Updated with Checklist"),
        paragraph("Action items:"),
        task_list(
            task_item("First action", checked=False),
            task_item("Second action", checked=False),
            task_item("Third action", checked=False),
        )
    ]
    
    client.replace_json_document(document_id, new_content)
    
    # Verify update
    doc_content = client.get_json_document(document_id)
    content_blocks = doc_content["default"]["content"]
    
    # Find task list
    has_task_list = any(block.get("type") == "taskList" for block in content_blocks)
    assert has_task_list, "Task list not found after update"
    
    print(f"✅ Updated task with checklist: {task_id}")
    return task_id


@pytest.mark.integration
def test_task_list_with_mixed_content():
    """Test creating a task with mixed content including checklist."""
    client = get_client()
    board_id = get_board_id()
    group_id = get_group_id()
    
    # Create task first
    request = CreateTaskRequest(
        name="Sprint Planning with Checklists",
        board=board_id,
        group=group_id,
    )
    
    response = client.create_task(request)
    task_id = response.task.id
    document_id = response.task.document
    
    # Verify task was created
    assert task_id is not None
    
    # Create mixed content with checklists
    content = [
        heading(1, "Sprint Planning"),
        paragraph("This sprint focuses on user authentication."),
        
        heading(2, "Backend Tasks"),
        task_list(
            task_item("Design database schema", checked=True),
            task_item("Implement authentication API", checked=False),
            task_item("Add JWT tokens", checked=False),
        ),
        
        heading(2, "Frontend Tasks"),
        task_list(
            task_item("Create login page", checked=True),
            task_item("Create registration page", checked=False),
            task_item("Add form validation", checked=False),
        ),
        
        paragraph("Review meeting scheduled for Friday."),
    ]
    
    # Update task description with mixed content
    client.replace_json_document(document_id, content)
    
    # Verify content
    task = client.get_task(task_id)
    doc_content = client.get_json_document(task.task.document)
    content_blocks = doc_content["default"]["content"]
    
    # Count task lists
    task_lists = [block for block in content_blocks if block.get("type") == "taskList"]
    assert len(task_lists) == 2, "Should have 2 task lists"
    
    # Count headings
    headings = [block for block in content_blocks if block.get("type") == "heading"]
    assert len(headings) >= 2, "Should have at least 2 headings"
    
    print(f"✅ Created task with mixed content and checklists: {task_id}")
    return task_id


if __name__ == "__main__":
    print("Running task list integration tests...")
    print()
    
    try:
        task_id_1 = test_create_task_with_simple_checklist()
        print(f"Test 1 passed: Simple checklist - Task ID: {task_id_1}")
        print()
        
        task_id_2 = test_create_task_with_nested_checklist()
        print(f"Test 2 passed: Nested checklist - Task ID: {task_id_2}")
        print()
        
        task_id_3 = test_update_task_with_checklist()
        print(f"Test 3 passed: Update with checklist - Task ID: {task_id_3}")
        print()
        
        task_id_4 = test_task_list_with_mixed_content()
        print(f"Test 4 passed: Mixed content - Task ID: {task_id_4}")
        print()
        
        print("=" * 60)
        print("✅ All integration tests passed!")
        print()
        print("Created tasks with task lists:")
        print(f"  1. Simple checklist: {task_id_1}")
        print(f"  2. Nested checklist: {task_id_2}")
        print(f"  3. Updated checklist: {task_id_3}")
        print(f"  4. Mixed content: {task_id_4}")
        print()
        print("You can view these tasks in your Vaiz workspace to see the checklists!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

