"""
Integration tests for mention blocks with main vaiz module imports.
"""

import pytest


def test_mention_imports_from_vaiz():
    """Test that mention helpers can be imported from vaiz module."""
    from vaiz import (
        mention,
        mention_user,
        mention_document,
        mention_task,
        mention_milestone,
    )
    
    # Test that functions are callable
    assert callable(mention)
    assert callable(mention_user)
    assert callable(mention_document)
    assert callable(mention_task)
    assert callable(mention_milestone)


def test_mention_with_other_document_helpers():
    """Test using mentions with other document structure helpers."""
    from vaiz import (
        paragraph,
        text,
        heading,
        mention_user,
        mention_task,
        bullet_list,
        list_item,
    )
    
    member_id = "test_member_123"
    task_id = "test_task_456"
    
    # Create document with mentions mixed with other elements
    content = [
        heading(1, "Task Assignment"),
        paragraph(
            text("User "),
            mention_user(member_id),
            text(" is assigned to "),
            mention_task(task_id)
        ),
        bullet_list(
            list_item(paragraph(text("Priority: High"))),
            list_item(paragraph(
                text("Assignee: "),
                mention_user(member_id)
            ))
        )
    ]
    
    assert len(content) == 3
    assert content[0]["type"] == "heading"
    assert content[1]["type"] == "paragraph"
    assert content[2]["type"] == "bulletList"


def test_mention_helpers_create_valid_structure():
    """Test that all mention helper functions create valid structures."""
    from vaiz import (
        mention_user,
        mention_document,
        mention_task,
        mention_milestone,
    )
    
    helpers = [
        (mention_user, "User"),
        (mention_document, "Document"),
        (mention_task, "Task"),
        (mention_milestone, "Milestone"),
    ]
    
    for helper_func, expected_kind in helpers:
        result = helper_func("test_id_123")
        
        assert result["type"] == "custom-mention"
        assert result["attrs"]["custom"] == 1
        assert result["attrs"]["inline"] is True
        assert result["attrs"]["data"]["item"]["kind"] == expected_kind
        assert result["attrs"]["data"]["item"]["id"] == "test_id_123"

