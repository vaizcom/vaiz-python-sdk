"""
Test cases for comment functionality in the Vaiz SDK.
Tests real API interactions for posting comments.
"""

import pytest
from vaiz.models import PostCommentRequest, PostCommentResponse, Comment, CreateTaskRequest, TaskPriority, ReactToCommentRequest, ReactToCommentResponse, CommentReaction, CommentReactionType, COMMENT_REACTION_METADATA, GetCommentsRequest, GetCommentsResponse, EditCommentRequest, EditCommentResponse, DeleteCommentRequest, DeleteCommentResponse
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
    # Import here to avoid circular imports
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'examples'))
    from test_helpers import create_test_task_and_get_document_id
    
    return create_test_task_and_get_document_id("Test Task for Comments")


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
    # Now checking datetime objects instead of strings
    assert comment.created_at.year == 2025
    assert comment.created_at.month == 1
    assert comment.created_at.day == 1
    assert comment.updated_at.year == 2025
    assert comment.updated_at.month == 1
    assert comment.updated_at.day == 1
    assert comment.files == []
    assert comment.reactions == []
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
    # Test with native field present
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
    
    # Test without native field (as API doesn't always return it)
    reaction_data_no_native = {
        "_id": "reaction456",
        "id": "thumbs_up",
        "memberIds": ["member3"]
    }
    
    reaction2 = CommentReaction(**reaction_data_no_native)
    assert reaction2.reaction_db_id == "reaction456"
    assert reaction2.native is None  # Should be None when not provided
    assert reaction2.emoji_id == "thumbs_up"
    assert reaction2.member_ids == ["member3"]


def test_react_to_comment_response_model():
    """Test ReactToCommentResponse model."""
    # Test with native field present
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
    
    # Test without native field (as API doesn't always return it)
    response_data_no_native = {
        "payload": {
            "reactions": [
                {
                    "_id": "reaction456",
                    "id": "thumbs_up",
                    "memberIds": ["member2", "member3"]
                }
            ]
        },
        "type": "ReactToComment"
    }
    
    response2 = ReactToCommentResponse(**response_data_no_native)
    assert response2.type == "ReactToComment"
    assert len(response2.reactions) == 1
    assert response2.reactions[0].native is None
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
    # Note: API doesn't return native field anymore, so we don't check it
    assert our_reaction.emoji_id == "kissing_smiling_eyes"
    assert len(our_reaction.member_ids) >= 1
    
    print(f"Created reaction ID: {our_reaction.reaction_db_id}")
    print(f"Reaction emoji ID: {our_reaction.emoji_id}")
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
    # Note: API doesn't return native field anymore, so we don't check it
    assert len(thumbs_up_reaction.member_ids) >= 1
    
    print(f"Added THUMBS_UP reaction")
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
        # Note: API doesn't return native field anymore, so we don't check it
        assert len(our_reaction.member_ids) >= 1
        
        reactions_added.append({
            "type": reaction_type,
            "emoji": metadata["native"],  # Use metadata since API doesn't return native
            "id": our_reaction.reaction_db_id,
            "members": len(our_reaction.member_ids)
        })
        
        print(f"✅ Added {reaction_type.value}: {metadata['native']} (ID: {our_reaction.reaction_db_id})")
    
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
    # Note: API doesn't return native field anymore, so we don't check it
    
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


def test_edit_comment_request_model():
    """Test EditCommentRequest model creation and serialization."""
    request = EditCommentRequest(
        content="<p>Updated content</p>",
        comment_id="comment123",
        add_file_ids=["file1", "file2"],
        order_file_ids=["file1", "file2"],
        remove_file_ids=["file3"]
    )
    
    assert request.content == "<p>Updated content</p>"
    assert request.comment_id == "comment123"
    assert request.add_file_ids == ["file1", "file2"]
    assert request.order_file_ids == ["file1", "file2"]
    assert request.remove_file_ids == ["file3"]
    
    # Test model dump with aliases
    data = request.model_dump()
    assert data["content"] == "<p>Updated content</p>"
    assert data["commentId"] == "comment123"
    assert data["addFileIds"] == ["file1", "file2"]
    assert data["orderFileIds"] == ["file1", "file2"]
    assert data["removeFileIds"] == ["file3"]


def test_edit_comment_request_minimal():
    """Test EditCommentRequest model with minimal data."""
    request = EditCommentRequest(
        content="Simple text",
        comment_id="comment456"
    )
    
    assert request.content == "Simple text"
    assert request.comment_id == "comment456"
    assert request.add_file_ids == []
    assert request.order_file_ids == []
    assert request.remove_file_ids == []
    
    data = request.model_dump()
    assert data["addFileIds"] == []
    assert data["orderFileIds"] == []
    assert data["removeFileIds"] == []


def test_edit_comment_response_model():
    """Test EditCommentResponse model."""
    response_data = {
        "payload": {
            "comment": {
                "_id": "comment1",
                "authorId": "author1",
                "documentId": "doc1",
                "content": "<p>Updated comment</p>",
                "createdAt": "2025-01-01T00:00:00Z",
                "updatedAt": "2025-01-01T00:01:00Z",
                "editedAt": "2025-01-01T00:01:00Z",
                "files": [],
                "reactions": [],
                "hasRemovedFiles": False
            }
        },
        "type": "EditComment"
    }
    
    response = EditCommentResponse(**response_data)
    
    assert response.type == "EditComment"
    
    comment = response.comment
    assert comment.id == "comment1"
    assert comment.author_id == "author1"
    assert comment.document_id == "doc1"
    assert comment.content == "<p>Updated comment</p>"
    # Check edited_at as datetime object
    assert comment.edited_at.year == 2025
    assert comment.edited_at.month == 1
    assert comment.edited_at.day == 1
    assert comment.edited_at.hour == 0
    assert comment.edited_at.minute == 1


def test_comment_model_with_edited_at():
    """Test Comment model with editedAt field."""
    comment_data = {
        "_id": "comment1",
        "authorId": "author1", 
        "documentId": "doc1",
        "content": "<p>Test comment</p>",
        "createdAt": "2025-01-01T00:00:00Z",
        "updatedAt": "2025-01-01T00:01:00Z",
        "editedAt": "2025-01-01T00:01:00Z",
        "files": [],
        "reactions": [],
        "hasRemovedFiles": False
    }
    
    comment = Comment(**comment_data)
    
    # Check edited_at as datetime object  
    assert comment.edited_at.year == 2025
    assert comment.edited_at.month == 1
    assert comment.edited_at.day == 1
    assert comment.edited_at.hour == 0
    assert comment.edited_at.minute == 1


def test_edit_comment(client, test_document_id):
    """Test editing a comment."""
    # First, create a comment to edit
    original_response = client.post_comment(
        document_id=test_document_id,
        content="<p>Original content that will be edited</p>"
    )
    
    original_comment = original_response.comment
    print(f"Created comment ID: {original_comment.id}")
    print(f"Original content: {original_comment.content}")
    
    # Edit the comment
    new_content = "<p><strong>Updated</strong> content with <em>formatting</em>!</p>"
    edit_response = client.edit_comment(
        comment_id=original_comment.id,
        content=new_content
    )
    
    # Validate edit response
    assert isinstance(edit_response, EditCommentResponse)
    assert edit_response.type == "EditComment"
    
    edited_comment = edit_response.comment
    
    # Check that content was updated
    assert edited_comment.id == original_comment.id
    assert edited_comment.content == new_content
    assert edited_comment.document_id == test_document_id
    assert edited_comment.author_id == original_comment.author_id
    
    # Check timestamps
    assert edited_comment.created_at == original_comment.created_at  # Created time should remain the same
    assert edited_comment.updated_at != original_comment.updated_at  # Updated time should change
    assert edited_comment.edited_at is not None  # Should have edited timestamp
    
    print(f"✅ Comment successfully edited!")
    print(f"✅ New content: {edited_comment.content}")
    print(f"✅ Created at: {edited_comment.created_at}")
    print(f"✅ Updated at: {edited_comment.updated_at}")
    print(f"✅ Edited at: {edited_comment.edited_at}")


def test_edit_comment_with_files(client, test_document_id):
    """Test editing a comment with file operations (using empty arrays)."""
    # Create a comment
    original_response = client.post_comment(
        document_id=test_document_id,
        content="<p>Comment for file editing test</p>"
    )
    
    original_comment = original_response.comment
    print(f"Created comment for file test: {original_comment.id}")
    
    # Edit with empty file operations (testing API structure without validation errors)
    edit_response = client.edit_comment(
        comment_id=original_comment.id,
        content="<p>Updated content with file operations</p>",
        add_file_ids=[],     # Empty array - no validation error
        order_file_ids=[],   # Empty array - no validation error  
        remove_file_ids=[]   # Empty array - no validation error
    )
    
    edited_comment = edit_response.comment
    
    assert edited_comment.content == "<p>Updated content with file operations</p>"
    assert edited_comment.edited_at is not None
    
    print(f"✅ Comment with file operations edited successfully!")
    print(f"✅ Content: {edited_comment.content}")
    print(f"✅ File arrays handled correctly (empty arrays)")


def test_edit_nonexistent_comment(client):
    """Test editing a comment that doesn't exist."""
    with pytest.raises((VaizSDKError, VaizNotFoundError)):
        client.edit_comment(
            comment_id="nonexistent_comment_id",
            content="<p>This should fail</p>"
        )


def test_delete_comment_request_model():
    """Test DeleteCommentRequest model creation and serialization."""
    request = DeleteCommentRequest(comment_id="comment123")
    
    assert request.comment_id == "comment123"
    
    # Test model dump with aliases
    data = request.model_dump()
    assert data["commentId"] == "comment123"


def test_delete_comment_response_model():
    """Test DeleteCommentResponse model."""
    response_data = {
        "payload": {
            "comment": {
                "_id": "comment1",
                "authorId": "author1",
                "documentId": "doc1",
                "content": "",  # Deleted comment has empty content
                "createdAt": "2025-01-01T00:00:00Z",
                "updatedAt": "2025-01-01T00:02:00Z",
                "deletedAt": "2025-01-01T00:02:00Z",  # Has deleted timestamp
                "files": [],
                "reactions": [],
                "hasRemovedFiles": False
            }
        },
        "type": "DeleteComment"
    }
    
    response = DeleteCommentResponse(**response_data)
    
    assert response.type == "DeleteComment"
    
    comment = response.comment
    assert comment.id == "comment1"
    assert comment.author_id == "author1"
    assert comment.document_id == "doc1"
    assert comment.content == ""  # Deleted comment has empty content
    # Check deleted_at as datetime object
    assert comment.deleted_at.year == 2025
    assert comment.deleted_at.month == 1
    assert comment.deleted_at.day == 1
    assert comment.deleted_at.hour == 0
    assert comment.deleted_at.minute == 2


def test_comment_model_with_deleted_at():
    """Test Comment model with deletedAt field."""
    comment_data = {
        "_id": "comment1",
        "authorId": "author1", 
        "documentId": "doc1",
        "content": "",
        "createdAt": "2025-01-01T00:00:00Z",
        "updatedAt": "2025-01-01T00:02:00Z",
        "deletedAt": "2025-01-01T00:02:00Z",
        "files": [],
        "reactions": [],
        "hasRemovedFiles": False
    }
    
    comment = Comment(**comment_data)
    
    # Check deleted_at as datetime object
    assert comment.deleted_at.year == 2025
    assert comment.deleted_at.month == 1
    assert comment.deleted_at.day == 1
    assert comment.deleted_at.hour == 0
    assert comment.deleted_at.minute == 2


def test_delete_comment(client, test_document_id):
    """Test deleting a comment."""
    # First, create a comment to delete
    original_response = client.post_comment(
        document_id=test_document_id,
        content="<p>This comment will be deleted</p>"
    )
    
    original_comment = original_response.comment
    print(f"Created comment ID: {original_comment.id}")
    print(f"Original content: {original_comment.content}")
    
    # Delete the comment
    delete_response = client.delete_comment(comment_id=original_comment.id)
    
    # Validate delete response
    assert isinstance(delete_response, DeleteCommentResponse)
    assert delete_response.type == "DeleteComment"
    
    deleted_comment = delete_response.comment
    
    # Check that comment was soft deleted
    assert deleted_comment.id == original_comment.id
    assert deleted_comment.content == ""  # Content becomes empty
    assert deleted_comment.document_id == test_document_id
    assert deleted_comment.author_id == original_comment.author_id
    
    # Check timestamps
    assert deleted_comment.created_at == original_comment.created_at  # Created time should remain the same
    assert deleted_comment.updated_at != original_comment.updated_at  # Updated time should change
    assert deleted_comment.deleted_at is not None  # Should have deleted timestamp
    
    print(f"✅ Comment successfully deleted!")
    print(f"✅ Content cleared: '{deleted_comment.content}'")
    print(f"✅ Created at: {deleted_comment.created_at}")
    print(f"✅ Updated at: {deleted_comment.updated_at}")
    print(f"✅ Deleted at: {deleted_comment.deleted_at}")


def test_delete_comment_and_verify_in_list(client, test_document_id):
    """Test that deleted comment still appears in get_comments but is marked as deleted."""
    # Create a comment
    comment_response = client.post_comment(
        document_id=test_document_id,
        content="<p>Comment to delete and verify</p>"
    )
    
    comment_id = comment_response.comment.id
    print(f"Created comment for deletion: {comment_id}")
    
    # Delete the comment
    delete_response = client.delete_comment(comment_id=comment_id)
    assert delete_response.comment.deleted_at is not None
    print(f"Deleted comment at: {delete_response.comment.deleted_at}")
    
    # Get all comments and verify deleted comment is still there but marked as deleted
    comments_response = client.get_comments(document_id=test_document_id)
    
    # Find our deleted comment in the list
    deleted_comment_in_list = None
    for comment in comments_response.comments:
        if comment.id == comment_id:
            deleted_comment_in_list = comment
            break
    
    # Verify deleted comment properties
    assert deleted_comment_in_list is not None
    assert deleted_comment_in_list.content == ""  # Content should be empty
    assert deleted_comment_in_list.deleted_at is not None  # Should have deleted timestamp
    
    print(f"✅ Deleted comment found in list with empty content")
    print(f"✅ Deleted timestamp: {deleted_comment_in_list.deleted_at}")


def test_delete_nonexistent_comment(client):
    """Test deleting a comment that doesn't exist."""
    with pytest.raises((VaizSDKError, VaizNotFoundError)):
        client.delete_comment(comment_id="nonexistent_comment_id")


def test_post_comment_with_single_file(client, test_document_id):
    """Test posting a comment with a single uploaded file."""
    import os
    from vaiz.models.enums import UploadFileType
    
    # Upload a single file first
    file_path = os.path.join("assets", "example.png")
    if not os.path.exists(file_path):
        print(f"Skipping test - file not found: {file_path}")
        return
    
    print(f"Uploading file: {file_path}")
    upload_response = client.upload_file(file_path, UploadFileType.Image)
    file_id = upload_response.file.id
    print(f"Uploaded file ID: {file_id}")
    print(f"File type: {upload_response.file.type.value}")
    
    # Create comment with the uploaded file
    comment_response = client.post_comment(
        document_id=test_document_id,
        content="<p>Comment with a single <strong>image</strong> file</p>",
        file_ids=[file_id]
    )
    
    comment = comment_response.comment
    assert len(comment.files) == 1
    assert comment.files[0].id == file_id
    assert comment.files[0].type.value == "Image"
    
    print(f"✅ Created comment with single file: {comment.id}")
    print(f"✅ Comment files: {[f.id for f in comment.files]}")
    print(f"✅ File details: {comment.files[0].original_name} ({comment.files[0].size} bytes, {comment.files[0].type.value})")


def test_post_comment_with_multiple_files(client, test_document_id):
    """Test posting a comment with multiple uploaded files (image, video, document)."""
    import os
    from vaiz.models.enums import UploadFileType
    
    # Upload multiple different file types
    files_to_upload = [
        ("assets/example.png", "Image", UploadFileType.Image),
        ("assets/example.mp4", "Video", UploadFileType.Video), 
        ("assets/example.pdf", "Document", UploadFileType.Pdf)
    ]
    
    uploaded_file_ids = []
    
    for file_path, file_type_name, file_type_enum in files_to_upload:
        if os.path.exists(file_path):
            print(f"Uploading {file_type_name}: {file_path}")
            upload_response = client.upload_file(file_path, file_type_enum)
            file_id = upload_response.file.id
            uploaded_file_ids.append(file_id)
            print(f"Uploaded {file_type_name} ID: {file_id}")
            print(f"File type: {upload_response.file.type.value}")
            assert upload_response.file.type.value == file_type_enum.value
        else:
            print(f"Skipping {file_type_name} - file not found: {file_path}")
    
    if not uploaded_file_ids:
        print("No files uploaded, skipping test")
        return
    
    # Create comment with multiple files
    comment_response = client.post_comment(
        document_id=test_document_id,
        content="<p>Comment with <strong>multiple files</strong>: image, video, and document</p>",
        file_ids=uploaded_file_ids
    )
    
    comment = comment_response.comment
    assert len(comment.files) == len(uploaded_file_ids)
    
    comment_file_ids = [f.id for f in comment.files]
    for file_id in uploaded_file_ids:
        assert file_id in comment_file_ids
    
    print(f"✅ Created comment with {len(uploaded_file_ids)} files: {comment.id}")
    print(f"✅ Comment files: {comment_file_ids}")
    print(f"✅ File details: {[(f.original_name, f.size, f.type.value) for f in comment.files]}")
    
    # Return removed - pytest expects None from test functions


def test_edit_comment_add_files(client, test_document_id):
    """Test editing a comment to add files."""
    import os
    from vaiz.models.enums import UploadFileType
    
    # First create a comment without files
    original_response = client.post_comment(
        document_id=test_document_id,
        content="<p>Original comment without files</p>"
    )
    
    original_comment = original_response.comment
    assert len(original_comment.files) == 0
    print(f"Created comment without files: {original_comment.id}")
    
    # Upload a file to add
    file_path = os.path.join("assets", "example.pdf")
    if not os.path.exists(file_path):
        print(f"Skipping test - file not found: {file_path}")
        return
    
    upload_response = client.upload_file(file_path, UploadFileType.Pdf)
    file_id = upload_response.file.id
    print(f"Uploaded file to add: {file_id}")
    print(f"File type: {upload_response.file.type.value}")
    
    # Edit comment to add the file
    edit_response = client.edit_comment(
        comment_id=original_comment.id,
        content="<p><strong>EDITED:</strong> Comment now has a file attached!</p>",
        add_file_ids=[file_id],
        order_file_ids=[file_id]  # Set the order
    )
    
    edited_comment = edit_response.comment
    assert len(edited_comment.files) == 1
    assert edited_comment.files[0].id == file_id
    assert edited_comment.files[0].type.value == "Pdf"
    assert edited_comment.edited_at is not None
    
    print(f"✅ Successfully added file to comment")
    print(f"✅ Comment files after edit: {[f.id for f in edited_comment.files]}")
    print(f"✅ File details: {edited_comment.files[0].original_name} ({edited_comment.files[0].type.value})")
    print(f"✅ Edited at: {edited_comment.edited_at}")


def test_edit_comment_remove_files(client, test_document_id):
    """Test editing a comment to remove files."""
    import os
    from vaiz.models.enums import UploadFileType
    
    # Upload files first
    file_path1 = os.path.join("assets", "example.png")
    file_path2 = os.path.join("assets", "example.pdf")
    
    file_ids = []
    file_types = [UploadFileType.Image, UploadFileType.Pdf]
    
    for file_path, file_type in zip([file_path1, file_path2], file_types):
        if os.path.exists(file_path):
            upload_response = client.upload_file(file_path, file_type)
            file_ids.append(upload_response.file.id)
            print(f"Uploaded: {upload_response.file.id} ({upload_response.file.type.value})")
    
    if len(file_ids) < 2:
        print("Need at least 2 files for this test, skipping")
        return
    
    # Create comment with files
    comment_response = client.post_comment(
        document_id=test_document_id,
        content="<p>Comment with files that will be removed</p>",
        file_ids=file_ids
    )
    
    comment = comment_response.comment
    assert len(comment.files) == len(file_ids)
    print(f"Created comment with {len(file_ids)} files: {comment.id}")
    
    # Edit comment to remove one file
    file_to_remove = file_ids[0]
    file_to_keep = file_ids[1]
    
    edit_response = client.edit_comment(
        comment_id=comment.id,
        content="<p><strong>EDITED:</strong> Removed one file, kept another</p>",
        remove_file_ids=[file_to_remove],
        order_file_ids=[file_to_keep]  # Only the remaining file
    )
    
    edited_comment = edit_response.comment
    assert len(edited_comment.files) == 1
    edited_file_ids = [f.id for f in edited_comment.files]
    assert edited_comment.files[0].id == file_to_keep
    assert file_to_remove not in edited_file_ids
    
    print(f"✅ Successfully removed file from comment")
    print(f"✅ Removed file: {file_to_remove}")
    print(f"✅ Remaining files: {edited_file_ids}")


def test_edit_comment_reorder_files(client, test_document_id):
    """Test editing a comment to reorder files."""
    import os
    from vaiz.models.enums import UploadFileType
    
    # Upload multiple files
    files_to_upload = [
        ("assets/example.png", UploadFileType.Image),
        ("assets/example.pdf", UploadFileType.Pdf)
    ]
    file_ids = []
    
    for file_path, file_type in files_to_upload:
        if os.path.exists(file_path):
            upload_response = client.upload_file(file_path, file_type)
            file_ids.append(upload_response.file.id)
            print(f"Uploaded: {upload_response.file.id} ({upload_response.file.type.value})")
    
    if len(file_ids) < 2:
        print("Need at least 2 files for reorder test, skipping")
        return
    
    # Create comment with files in original order
    comment_response = client.post_comment(
        document_id=test_document_id,
        content="<p>Comment with files in original order</p>",
        file_ids=file_ids
    )
    
    comment = comment_response.comment
    original_order = [f.id for f in comment.files]
    print(f"Original file order: {original_order}")
    
    # Edit comment to reverse the file order
    reversed_order = list(reversed(file_ids))
    
    edit_response = client.edit_comment(
        comment_id=comment.id,
        content="<p><strong>EDITED:</strong> Files reordered!</p>",
        order_file_ids=reversed_order
    )
    
    edited_comment = edit_response.comment
    edited_order = [f.id for f in edited_comment.files]
    assert edited_order == reversed_order
    assert edited_order != original_order
    
    print(f"✅ Successfully reordered files")
    print(f"✅ New file order: {edited_order}")


def test_comment_with_files_complete_lifecycle(client, test_document_id):
    """Test complete lifecycle of comment with files: create -> add -> reorder -> remove -> delete."""
    import os
    from vaiz.models.enums import UploadFileType
    
    print("\n=== COMPLETE FILE LIFECYCLE TEST ===")
    
    # 1. Upload initial files
    file_path = os.path.join("assets", "example.png")
    if not os.path.exists(file_path):
        print("Skipping lifecycle test - no files available")
        return
    
    upload1 = client.upload_file(file_path, UploadFileType.Image)
    file_id1 = upload1.file.id
    print(f"1. Uploaded initial file: {file_id1} ({upload1.file.type.value})")
    
    # 2. Create comment with one file
    comment_response = client.post_comment(
        document_id=test_document_id,
        content="<p>Lifecycle test with files</p>",
        file_ids=[file_id1]
    )
    comment_id = comment_response.comment.id
    print(f"2. Created comment with 1 file: {comment_id}")
    
    # 3. Add another file if available
    file_path2 = os.path.join("assets", "example.pdf")
    if os.path.exists(file_path2):
        upload2 = client.upload_file(file_path2, UploadFileType.Pdf)
        file_id2 = upload2.file.id
        print(f"3. Uploaded second file: {file_id2} ({upload2.file.type.value})")
        
        # Add the second file
        edit_response = client.edit_comment(
            comment_id=comment_id,
            content="<p><strong>ADDED:</strong> Second file attached</p>",
            add_file_ids=[file_id2],
            order_file_ids=[file_id1, file_id2]
        )
        print(f"4. Added second file to comment")
        
        # 4. Reorder files (reverse order)
        all_files = edit_response.comment.files
        reversed_file_ids = [f.id for f in reversed(all_files)]
        
        edit_response = client.edit_comment(
            comment_id=comment_id,
            content="<p><strong>REORDERED:</strong> Files in new order</p>",
            order_file_ids=reversed_file_ids
        )
        print(f"5. Reordered files: {[f.id for f in edit_response.comment.files]}")
        
        # 5. Remove one file
        current_file_ids = [f.id for f in edit_response.comment.files]
        file_to_remove = current_file_ids[1]  # Middle file
        remaining_files = [f for f in current_file_ids if f != file_to_remove]
        
        edit_response = client.edit_comment(
            comment_id=comment_id,
            content="<p><strong>REMOVED:</strong> One file removed</p>",
            remove_file_ids=[file_to_remove],
            order_file_ids=remaining_files
        )
        print(f"6. Removed file, remaining: {[f.id for f in edit_response.comment.files]}")
    
    # 6. Delete comment (files remain in system)
    delete_response = client.delete_comment(comment_id=comment_id)
    print(f"7. Deleted comment at: {delete_response.comment.deleted_at}")
    
    print("🎉 Complete file lifecycle test completed!")


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
    test_edit_comment_request_model()
    test_edit_comment_request_minimal()
    test_edit_comment_response_model()
    test_comment_model_with_edited_at()
    test_delete_comment_request_model()
    test_delete_comment_response_model()
    test_comment_model_with_deleted_at()
    print("All model tests passed!")
    
    # Note: API tests now require fixtures, run with pytest instead:
    # pytest tests/test_comments.py -v 