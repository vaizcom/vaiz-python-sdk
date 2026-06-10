"""
Tests for mention block helper functions.
"""

import json

import pytest
from vaiz.helpers import (
    mention,
    mention_user,
    mention_document,
    mention_task,
    mention_milestone,
    paragraph,
    text,
    heading,
)
from vaiz.models import CreateDocumentRequest, Kind, GetDocumentsRequest, GetTasksRequest
from tests.test_config import get_test_client, TEST_SPACE_ID


def test_mention_user():
    """Test creating a user mention with member_id."""
    member_id = "68fa5e14cdb30e1c96755975"
    result = mention_user(member_id)
    
    assert result["type"] == "custom-mention"
    assert result["attrs"]["custom"] == 1
    assert result["attrs"]["inline"] is True
    assert result["attrs"]["data"]["item"]["id"] == member_id
    assert result["attrs"]["data"]["item"]["kind"] == "User"
    assert "uid" in result["attrs"]
    assert len(result["content"]) == 1
    assert result["content"][0]["type"] == "text"


def test_mention_document():
    """Test creating a document mention."""
    document_id = "68fa6c7b62f676bcd1bcecae"
    result = mention_document(document_id)
    
    assert result["type"] == "custom-mention"
    assert result["attrs"]["data"]["item"]["id"] == document_id
    assert result["attrs"]["data"]["item"]["kind"] == "Document"


def test_mention_task():
    """Test creating a task mention."""
    task_id = "68fa67d262f676bcd1bc162f"
    result = mention_task(task_id)
    
    assert result["type"] == "custom-mention"
    assert result["attrs"]["data"]["item"]["id"] == task_id
    assert result["attrs"]["data"]["item"]["kind"] == "Task"


def test_mention_milestone():
    """Test creating a milestone mention."""
    milestone_id = "68fa650bcdb30e1c9677562e"
    result = mention_milestone(milestone_id)
    
    assert result["type"] == "custom-mention"
    assert result["attrs"]["data"]["item"]["id"] == milestone_id
    assert result["attrs"]["data"]["item"]["kind"] == "Milestone"


def test_mention_generic():
    """Test creating a generic mention with explicit kind."""
    item_id = "test123"
    result = mention(item_id, "User")
    
    assert result["type"] == "custom-mention"
    assert result["attrs"]["data"]["item"]["id"] == item_id
    assert result["attrs"]["data"]["item"]["kind"] == "User"


def test_mention_in_paragraph():
    """Test using mentions in a paragraph."""
    member_id = "68fa5e14cdb30e1c96755975"
    task_id = "68fa67d262f676bcd1bc162f"
    
    para = paragraph(
        text("User "),
        mention_user(member_id),
        text(" is assigned to "),
        mention_task(task_id)
    )
    
    assert para["type"] == "paragraph"
    assert len(para["content"]) == 4
    assert para["content"][1]["type"] == "custom-mention"
    assert para["content"][3]["type"] == "custom-mention"


def test_mention_unique_uids():
    """Test that each mention gets a unique UID."""
    member_id = "68fa5e14cdb30e1c96755975"
    mention1 = mention_user(member_id)
    mention2 = mention_user(member_id)
    
    assert mention1["attrs"]["uid"] != mention2["attrs"]["uid"]


def test_mention_structure_complete():
    """Test that mention structure has all required fields."""
    result = mention_user("test123")
    
    # Check all required attributes exist
    assert "type" in result
    assert "attrs" in result
    assert "content" in result
    
    attrs = result["attrs"]
    assert "uid" in attrs
    assert "custom" in attrs
    assert "inline" in attrs
    assert "data" in attrs
    
    data = attrs["data"]
    assert "item" in data
    
    item = data["item"]
    assert "id" in item
    assert "kind" in item


def test_all_mention_kinds():
    """Test all supported mention kinds."""
    kinds = ["User", "Document", "Task", "Milestone"]
    
    for kind in kinds:
        result = mention("test_id", kind)
        assert result["attrs"]["data"]["item"]["kind"] == kind


def test_create_document_with_real_mentions():
    """Integration test: Create document with real mentions and verify they exist."""
    client = get_test_client()
    
    # Get real IDs from API
    profile = client.get_profile()
    member_id = profile.profile.member_id
    
    # Get real document ID
    docs_response = client.get_documents(
        GetDocumentsRequest(kind=Kind.Space, kind_id=TEST_SPACE_ID)
    )
    document_id = None
    if docs_response.payload.documents:
        document_id = docs_response.payload.documents[0].id
    
    # Get real task ID
    tasks_response = client.get_tasks(GetTasksRequest())
    task_id = None
    if tasks_response.payload.tasks:
        task_id = tasks_response.payload.tasks[0].id
    
    # Get real milestone ID
    milestones_response = client.get_milestones()
    milestone_id = None
    if milestones_response.milestones:
        milestone_id = milestones_response.milestones[0].id
    
    # Create document in Space with mentions
    create_request = CreateDocumentRequest(
        kind=Kind.Space,
        kind_id=TEST_SPACE_ID,
        title="Test: Mention Blocks",
        index=0
    )
    
    doc_response = client.create_document(create_request)
    test_doc_id = doc_response.payload.document.id
    
    try:
        # Build content with real mentions
        content = [
            heading(1, "Test Mention Blocks"),
            paragraph(
                text("User mention: "),
                mention_user(member_id)
            )
        ]
        
        # Add document mention if available
        if document_id:
            content.append(paragraph(
                text("Document mention: "),
                mention_document(document_id)
            ))
        
        # Add task mention if available
        if task_id:
            content.append(paragraph(
                text("Task mention: "),
                mention_task(task_id)
            ))
        
        # Add milestone mention if available
        if milestone_id:
            content.append(paragraph(
                text("Milestone mention: "),
                mention_milestone(milestone_id)
            ))
        
        # Replace document content with mentions
        client.replace_json_document(test_doc_id, content)
        
        # Verify mentions were created by reading document
        doc_content = client.get_json_document(test_doc_id)

        assert doc_content is not None
        assert "root" in doc_content
        assert "content" in doc_content["root"]

        # Lexical format: mentions persist as serialized markers
        # with __userId / __entityId and __entityKind fields
        doc_str = json.dumps(doc_content)
        mention_count = doc_str.count("-mention")

        # Verify at least user mention was created
        assert mention_count > 0, "No mention blocks found in document"

        assert member_id in doc_str, "User mention not found in document"
        assert "user-mention" in doc_str, "User mention marker not found"

        if document_id:
            assert document_id in doc_str, "Document mention not found"
            assert 'Document' in doc_str, "Document kind not found"
        if task_id:
            assert task_id in doc_str, "Task mention not found"
            assert 'Task' in doc_str, "Task kind not found"
        if milestone_id:
            assert milestone_id in doc_str, "Milestone mention not found"
            assert 'Milestone' in doc_str, "Milestone kind not found"

        print(f"\n✅ Successfully created and verified document with {mention_count} mention block(s)")
        print(f"   Document ID: {test_doc_id}")
        print(f"   View at: https://vaiz.app/document/{test_doc_id}")
        
    finally:
        # Cleanup: delete test document
        # Note: If there's a delete_document method, use it here
        pass

