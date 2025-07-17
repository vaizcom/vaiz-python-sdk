"""
Test cases for comment functionality in the Vaiz SDK.
Tests real API interactions for posting comments.
"""

import pytest
from vaiz.models import PostCommentRequest, PostCommentResponse, Comment, CreateTaskRequest, TaskPriority, ReactToCommentRequest, ReactToCommentResponse, CommentReaction, CommentReactionType, COMMENT_REACTION_METADATA, GetCommentsRequest, GetCommentsResponse
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


def test_react_to_comment_request_model():
    """Test ReactToCommentRequest model creation and serialization."""
    request = ReactToCommentRequest(
        comment_id="comment123",
        id="kissing_smiling_eyes",
        name="Kissing Face with Smiling Eyes",
        native="😙",
        unified="1f619",
        keywords=["affection", "valentines", "infatuation", "kiss"],
        shortcodes=":kissing_smiling_eyes:"
    )
    
    assert request.comment_id == "comment123"
    assert request.id == "kissing_smiling_eyes"
    assert request.name == "Kissing Face with Smiling Eyes"
    assert request.native == "😙"
    assert request.unified == "1f619"
    assert request.keywords == ["affection", "valentines", "infatuation", "kiss"]
    assert request.shortcodes == ":kissing_smiling_eyes:"
    
    # Test model dump with aliases
    data = request.model_dump()
    assert data["commentId"] == "comment123"
    assert data["id"] == "kissing_smiling_eyes"
    assert data["name"] == "Kissing Face with Smiling Eyes"
    assert data["native"] == "😙"
    assert data["unified"] == "1f619"
    assert data["keywords"] == ["affection", "valentines", "infatuation", "kiss"]
    assert data["shortcodes"] == ":kissing_smiling_eyes:"


def test_comment_reaction_model():
    """Test CommentReaction model with field aliases."""
    reaction_data = {
        "_id": "reaction123",
        "native": "😙",
        "id": "kissing_smiling_eyes",
        "memberIds": ["member1", "member2"]
    }
    
    reaction = CommentReaction(**reaction_data)
    
    assert reaction.reaction_db_id == "reaction123"
    assert reaction.native == "😙"
    assert reaction.emoji_id == "kissing_smiling_eyes"
    assert reaction.member_ids == ["member1", "member2"]


def test_react_to_comment_response_model():
    """Test ReactToCommentResponse model."""
    response_data = {
        "payload": {
            "reactions": [
                {
                    "_id": "reaction123",
                    "native": "😙",
                    "id": "kissing_smiling_eyes",
                    "memberIds": ["member1"]
                }
            ]
        },
        "type": "ReactToComment"
    }
    
    response = ReactToCommentResponse(**response_data)
    
    assert response.type == "ReactToComment"
    assert len(response.reactions) == 1
    
    reaction = response.reactions[0]
    assert reaction.reaction_db_id == "reaction123"
    assert reaction.native == "😙"
    assert reaction.emoji_id == "kissing_smiling_eyes"
    assert reaction.member_ids == ["member1"]


def test_react_to_comment(client, test_document_id):
    """Test reacting to a comment."""
    # First, create a comment to react to
    comment_response = client.post_comment(
        document_id=test_document_id,
        content="<p>Comment that will receive a reaction</p>"
    )
    
    comment = comment_response.comment
    assert comment.id is not None
    print(f"Created comment for reaction test: {comment.id}")
    
    # Now react to the comment
    reaction_response = client.react_to_comment(
        comment_id=comment.id,
        emoji_id="kissing_smiling_eyes",
        emoji_name="Kissing Face with Smiling Eyes",
        emoji_native="😙",
        emoji_unified="1f619",
        emoji_keywords=["affection", "valentines", "infatuation", "kiss"],
        emoji_shortcodes=":kissing_smiling_eyes:"
    )
    
    # Validate reaction response
    assert isinstance(reaction_response, ReactToCommentResponse)
    assert reaction_response.type == "ReactToComment"
    assert len(reaction_response.reactions) >= 1
    
    # Find our reaction in the response
    our_reaction = None
    for reaction in reaction_response.reactions:
        if reaction.emoji_id == "kissing_smiling_eyes":
            our_reaction = reaction
            break
    
    assert our_reaction is not None
    assert our_reaction.native == "😙"
    assert our_reaction.emoji_id == "kissing_smiling_eyes"
    assert len(our_reaction.member_ids) >= 1
    
    print(f"Created reaction ID: {our_reaction.reaction_db_id}")
    print(f"Reaction emoji: {our_reaction.native}")
    print(f"Reaction members: {our_reaction.member_ids}")


def test_comment_reaction_type_enum():
    """Test CommentReactionType enum and metadata."""
    # Test that all enum values have metadata
    for reaction_type in CommentReactionType:
        assert reaction_type in COMMENT_REACTION_METADATA
        metadata = COMMENT_REACTION_METADATA[reaction_type]
        
        # Verify required fields exist
        assert "id" in metadata
        assert "name" in metadata
        assert "native" in metadata
        assert "unified" in metadata
        assert "keywords" in metadata
        assert "shortcodes" in metadata
        
        # Verify data types
        assert isinstance(metadata["id"], str)
        assert isinstance(metadata["name"], str)
        assert isinstance(metadata["native"], str)
        assert isinstance(metadata["unified"], str)
        assert isinstance(metadata["keywords"], list)
        assert isinstance(metadata["shortcodes"], str)
        
        print(f"✅ {reaction_type.value}: {metadata['native']} - {metadata['name']}")


def test_add_reaction_simple_api(client, test_document_id):
    """Test the simplified add_reaction API with enum."""
    # First, create a comment to react to
    comment_response = client.post_comment(
        document_id=test_document_id,
        content="<p>Comment for simplified reaction test</p>"
    )
    
    comment = comment_response.comment
    assert comment.id is not None
    print(f"Created comment for simple reaction test: {comment.id}")
    
    # Test with THUMBS_UP reaction
    reaction_response = client.add_reaction(
        comment_id=comment.id,
        reaction=CommentReactionType.THUMBS_UP
    )
    
    # Validate reaction response
    assert isinstance(reaction_response, ReactToCommentResponse)
    assert reaction_response.type == "ReactToComment"
    assert len(reaction_response.reactions) >= 1
    
    # Find our reaction in the response
    thumbs_up_reaction = None
    for reaction in reaction_response.reactions:
        if reaction.emoji_id == "1f44d":  # thumbs up unified code
            thumbs_up_reaction = reaction
            break
    
    assert thumbs_up_reaction is not None
    assert thumbs_up_reaction.native == "👍"
    assert len(thumbs_up_reaction.member_ids) >= 1
    
    print(f"Added THUMBS_UP reaction: {thumbs_up_reaction.native}")
    print(f"Reaction ID: {thumbs_up_reaction.reaction_db_id}")


def test_add_all_popular_reactions(client, test_document_id):
    """Test adding all 7 popular reactions to a single comment."""
    # First, create a comment to react to
    comment_response = client.post_comment(
        document_id=test_document_id,
        content="<p>This comment will receive ALL popular reactions! 🎯</p>"
    )
    
    comment = comment_response.comment
    assert comment.id is not None
    print(f"Created comment for all reactions test: {comment.id}")
    
    reactions_added = []
    
    # Add all popular reactions one by one
    for reaction_type in CommentReactionType:
        print(f"\nAdding reaction: {reaction_type.value}")
        
        reaction_response = client.add_reaction(
            comment_id=comment.id,
            reaction=reaction_type
        )
        
        # Validate response
        assert isinstance(reaction_response, ReactToCommentResponse)
        assert reaction_response.type == "ReactToComment"
        
        # Find the reaction we just added
        metadata = COMMENT_REACTION_METADATA[reaction_type]
        our_reaction = None
        for reaction in reaction_response.reactions:
            if reaction.emoji_id == metadata["id"]:
                our_reaction = reaction
                break
        
        assert our_reaction is not None
        assert our_reaction.native == metadata["native"]
        assert len(our_reaction.member_ids) >= 1
        
        reactions_added.append({
            "type": reaction_type,
            "emoji": our_reaction.native,
            "id": our_reaction.reaction_db_id,
            "members": len(our_reaction.member_ids)
        })
        
        print(f"✅ Added {reaction_type.value}: {our_reaction.native} (ID: {our_reaction.reaction_db_id})")
    
    print(f"\n🎉 Successfully added all {len(reactions_added)} popular reactions!")
    print("Reactions summary:")
    for i, reaction in enumerate(reactions_added, 1):
        print(f"{i}. {reaction['emoji']} {reaction['type'].value} - {reaction['members']} member(s)")
    
    # Final verification - should have all 7 reactions
    assert len(reactions_added) == 7
    
    # Verify we have all the expected emojis
    expected_emojis = {"👍", "❤️", "😂", "😮", "😢", "😡", "🎉"}
    actual_emojis = {r["emoji"] for r in reactions_added}
    assert actual_emojis == expected_emojis
    
    print(f"\n✅ All {len(expected_emojis)} popular reactions successfully added to comment {comment.id}!")


def test_get_comments_request_model():
    """Test GetCommentsRequest model creation and serialization."""
    request = GetCommentsRequest(document_id="test_doc_123")
    
    assert request.document_id == "test_doc_123"
    
    # Test model dump with aliases
    data = request.model_dump()
    assert data["documentId"] == "test_doc_123"


def test_get_comments_response_model():
    """Test GetCommentsResponse model."""
    response_data = {
        "payload": {
            "comments": [
                {
                    "_id": "comment1",
                    "authorId": "author1",
                    "documentId": "doc1",
                    "content": "<p>Test comment</p>",
                    "createdAt": "2025-01-01T00:00:00Z",
                    "updatedAt": "2025-01-01T00:00:00Z",
                    "files": [],
                    "reactions": [],
                    "hasRemovedFiles": False
                }
            ]
        },
        "type": "GetComments"
    }
    
    response = GetCommentsResponse(**response_data)
    
    assert response.type == "GetComments"
    assert len(response.comments) == 1
    
    comment = response.comments[0]
    assert comment.id == "comment1"
    assert comment.author_id == "author1"
    assert comment.document_id == "doc1"
    assert comment.content == "<p>Test comment</p>"


def test_get_comments(client, test_document_id):
    """Test getting comments for a document."""
    # First, create a few comments to retrieve
    comment1_response = client.post_comment(
        document_id=test_document_id,
        content="<p>First comment for get test</p>"
    )
    
    comment2_response = client.post_comment(
        document_id=test_document_id,
        content="<p>Second comment for get test</p>",
        reply_to=comment1_response.comment.id
    )
    
    # Add a reaction to the first comment
    client.add_reaction(
        comment_id=comment1_response.comment.id,
        reaction=CommentReactionType.THUMBS_UP
    )
    
    print(f"Created comments: {comment1_response.comment.id}, {comment2_response.comment.id}")
    
    # Now get all comments for the document
    comments_response = client.get_comments(document_id=test_document_id)
    
    # Validate response structure
    assert isinstance(comments_response, GetCommentsResponse)
    assert comments_response.type == "GetComments"
    assert len(comments_response.comments) >= 2  # Should have at least our 2 comments
    
    # Find our comments in the response
    our_comment1 = None
    our_comment2 = None
    
    for comment in comments_response.comments:
        if comment.id == comment1_response.comment.id:
            our_comment1 = comment
        elif comment.id == comment2_response.comment.id:
            our_comment2 = comment
    
    # Validate first comment
    assert our_comment1 is not None
    assert our_comment1.content == "<p>First comment for get test</p>"
    assert our_comment1.document_id == test_document_id
    assert len(our_comment1.reactions) >= 1  # Should have our thumbs up reaction
    assert our_comment1.reply_to is None  # Not a reply
    
    # Find thumbs up reaction
    thumbs_up_reaction = None
    for reaction in our_comment1.reactions:
        if reaction.emoji_id == "1f44d":  # thumbs up unified code
            thumbs_up_reaction = reaction
            break
    
    assert thumbs_up_reaction is not None
    assert thumbs_up_reaction.native == "👍"
    
    # Validate second comment (reply)
    assert our_comment2 is not None
    assert our_comment2.content == "<p>Second comment for get test</p>"
    assert our_comment2.document_id == test_document_id
    assert our_comment2.reply_to == comment1_response.comment.id  # Is a reply to first comment
    
    print(f"✅ Retrieved {len(comments_response.comments)} comments")
    print(f"✅ Found our first comment: {our_comment1.content}")
    print(f"✅ Found our reply comment: {our_comment2.content}")
    print(f"✅ First comment has {len(our_comment1.reactions)} reaction(s)")
    print(f"✅ Reply points to: {our_comment2.reply_to}")


if __name__ == "__main__":
    # Run specific tests for development
    test_post_comment_request_model()
    test_post_comment_request_empty_files()
    test_post_comment_request_with_reply()
    test_comment_model_aliases()
    test_comment_model_with_reply()
    test_react_to_comment_request_model()
    test_comment_reaction_model()
    test_react_to_comment_response_model()
    test_comment_reaction_type_enum()
    test_get_comments_request_model()
    test_get_comments_response_model()
    print("All model tests passed!")
    
    # Note: API tests now require fixtures, run with pytest instead:
    # pytest tests/test_comments.py -v 