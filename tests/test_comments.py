"""
Test cases for comment functionality in the Vaiz SDK.
Tests real API interactions for posting comments.
"""

import pytest
from vaiz.models import PostCommentRequest, PostCommentResponse, Comment, CreateTaskRequest, TaskPriority
from vaiz.api.base import VaizSDKError, VaizNotFoundError
from tests.test_config import get_test_client, TEST_BOARD_ID, TEST_GROUP_ID, TEST_PROJECT_ID, TEST_ASSIGNEE_ID


@pytest.fixture(scope="module")
def client():
    """Fixture that provides a test client."""
    return get_test_client()


@pytest.fixture(scope="module")
def test_document_id(client):
    """
    Fixture that creates a test task and returns its document ID for comment testing.
    This ensures we have a valid document to comment on.
    """
    task = CreateTaskRequest(
        name="Test Task for Comments",
        group=TEST_GROUP_ID,
        board=TEST_BOARD_ID,
        project=TEST_PROJECT_ID,
        priority=TaskPriority.High,
        completed=False,
        types=[],
        assignees=[TEST_ASSIGNEE_ID] if TEST_ASSIGNEE_ID else [],
        subtasks=[],
        milestones=[],
        rightConnectors=[],
        leftConnectors=[]
    )
    response = client.create_task(task)
    assert response.type == "CreateTask"
    
    # Extract document ID from the created task
    task_data = response.task
    document_id = task_data.document
    print(f"Created test task with document ID: {document_id}")
    return document_id


def test_post_comment_request_model():
    """Test PostCommentRequest model creation and serialization."""
    request = PostCommentRequest(
        document_id="test_doc_id",
        content="<p>Test content</p>",
        file_ids=["file1", "file2"]
    )
    
    assert request.document_id == "test_doc_id"
    assert request.content == "<p>Test content</p>"
    assert request.file_ids == ["file1", "file2"]
    
    # Test model dump with aliases
    data = request.model_dump()
    assert data["documentId"] == "test_doc_id"
    assert data["content"] == "<p>Test content</p>"
    assert data["fileIds"] == ["file1", "file2"]


def test_post_comment_request_empty_files():
    """Test PostCommentRequest with empty file list."""
    request = PostCommentRequest(
        document_id="test_doc_id",
        content="Simple text content"
    )
    
    assert request.file_ids == []
    assert request.reply_to is None
    
    data = request.model_dump()
    assert data["fileIds"] == []
    # reply_to should not be in the data when None due to model_dump filtering
    assert "replyTo" not in data


def test_post_comment_request_with_reply():
    """Test PostCommentRequest with reply_to field."""
    request = PostCommentRequest(
        document_id="test_doc_id",
        content="<p>Reply content</p>",
        file_ids=["file1"],
        reply_to="original_comment_id"
    )
    
    assert request.document_id == "test_doc_id"
    assert request.content == "<p>Reply content</p>"
    assert request.file_ids == ["file1"]
    assert request.reply_to == "original_comment_id"
    
    # Test model dump with aliases
    data = request.model_dump()
    assert data["documentId"] == "test_doc_id"
    assert data["content"] == "<p>Reply content</p>"
    assert data["fileIds"] == ["file1"]
    assert data["replyTo"] == "original_comment_id"


def test_post_comment_with_html(client, test_document_id):
    """Test posting a comment with HTML content."""
    response = client.post_comment(
        document_id=test_document_id,
        content="<p>Test <em>italic</em> comment from SDK test</p>",
        file_ids=[]
    )
    
    # Validate response structure
    assert isinstance(response, PostCommentResponse)
    assert response.type == "PostComment"
    assert "comment" in response.payload
    
    # Validate comment data
    comment = response.comment
    assert isinstance(comment, Comment)
    assert comment.id is not None
    assert comment.author_id is not None
    assert comment.document_id == test_document_id
    assert comment.content == "<p>Test <em>italic</em> comment from SDK test</p>"
    assert comment.created_at is not None
    assert comment.updated_at is not None
    assert isinstance(comment.files, list)
    assert isinstance(comment.reactions, list)
    assert isinstance(comment.has_removed_files, bool)
    
    print(f"Posted comment ID: {comment.id}")


def test_post_simple_text_comment(client, test_document_id):
    """Test posting a simple text comment."""
    response = client.post_comment(
        document_id=test_document_id,
        content="Simple text comment from SDK test"
    )
    
    # Validate response
    assert isinstance(response, PostCommentResponse)
    assert response.type == "PostComment"
    
    comment = response.comment
    assert comment.content == "Simple text comment from SDK test"
    assert comment.document_id == test_document_id
    assert comment.files == []
    
    print(f"Posted simple comment ID: {comment.id}")


def test_post_comment_with_empty_file_list(client, test_document_id):
    """Test posting a comment with explicitly empty file list."""
    response = client.post_comment(
        document_id=test_document_id,
        content="<p>Comment with <strong>bold</strong> text</p>",
        file_ids=[]
    )
    
    # Validate response
    assert isinstance(response, PostCommentResponse)
    comment = response.comment
    assert comment.files == []
    assert "<strong>bold</strong>" in comment.content
    
    print(f"Posted comment with empty files ID: {comment.id}")


def test_post_comment_reply(client, test_document_id):
    """Test posting a reply to a comment."""
    # First, create an original comment
    original_response = client.post_comment(
        document_id=test_document_id,
        content="<p>Original comment for reply test</p>"
    )
    
    original_comment = original_response.comment
    assert original_comment.id is not None
    assert original_comment.reply_to is None  # Original comment has no reply_to
    
    print(f"Created original comment ID: {original_comment.id}")
    
    # Now create a reply to the original comment
    reply_response = client.post_comment(
        document_id=test_document_id,
        content="<p>This is a <strong>reply</strong> to the original comment</p>",
        reply_to=original_comment.id
    )
    
    # Validate reply response
    assert isinstance(reply_response, PostCommentResponse)
    assert reply_response.type == "PostComment"
    
    reply_comment = reply_response.comment
    assert isinstance(reply_comment, Comment)
    assert reply_comment.id is not None
    assert reply_comment.author_id is not None
    assert reply_comment.document_id == test_document_id
    assert reply_comment.content == "<p>This is a <strong>reply</strong> to the original comment</p>"
    assert reply_comment.reply_to == original_comment.id  # This is the key assertion
    assert reply_comment.created_at is not None
    assert reply_comment.updated_at is not None
    
    print(f"Created reply comment ID: {reply_comment.id}")
    print(f"Reply points to original comment: {reply_comment.reply_to}")


def test_post_comment_invalid_document(client):
    """Test posting a comment to invalid document ID."""
    invalid_document_id = "invalid_document_id_123"
    
    with pytest.raises(VaizSDKError):
        client.post_comment(
            document_id=invalid_document_id,
            content="This should fail"
        )


def test_comment_model_aliases():
    """Test Comment model field aliases."""
    comment_data = {
        "_id": "comment123",
        "authorId": "author123",
        "documentId": "doc123",
        "content": "<p>Test</p>",
        "createdAt": "2025-01-01T00:00:00Z",
        "updatedAt": "2025-01-01T00:00:00Z",
        "files": [],
        "reactions": [],
        "hasRemovedFiles": False
    }
    
    comment = Comment(**comment_data)
    
    assert comment.id == "comment123"
    assert comment.author_id == "author123"
    assert comment.document_id == "doc123"
    assert comment.content == "<p>Test</p>"
    assert comment.created_at == "2025-01-01T00:00:00Z"
    assert comment.updated_at == "2025-01-01T00:00:00Z"
    assert comment.files == []
    assert comment.reactions == []
    assert comment.has_removed_files is False
    assert comment.reply_to is None  # No replyTo in original data


def test_comment_model_with_reply():
    """Test Comment model with reply_to field."""
    comment_data = {
        "_id": "reply123",
        "authorId": "author123",
        "documentId": "doc123",
        "content": "<p>Reply content</p>",
        "createdAt": "2025-01-01T00:00:00Z",
        "updatedAt": "2025-01-01T00:00:00Z",
        "files": [],
        "reactions": [],
        "hasRemovedFiles": False,
        "replyTo": "original_comment_id"
    }
    
    comment = Comment(**comment_data)
    
    assert comment.id == "reply123"
    assert comment.author_id == "author123"
    assert comment.document_id == "doc123"
    assert comment.content == "<p>Reply content</p>"
    assert comment.reply_to == "original_comment_id"


if __name__ == "__main__":
    # Run specific tests for development
    test_post_comment_request_model()
    test_post_comment_request_empty_files()
    test_post_comment_request_with_reply()
    test_comment_model_aliases()
    test_comment_model_with_reply()
    print("All model tests passed!")
    
    # Note: API tests now require fixtures, run with pytest instead:
    # pytest tests/test_comments.py -v 