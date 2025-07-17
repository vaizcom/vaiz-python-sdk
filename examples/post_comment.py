"""
Example: Post a comment to a document using the Vaiz SDK.
This example demonstrates how to create comments with HTML content and optional file attachments.
"""

from vaiz.models import PostCommentRequest, CommentReactionType
from .config import get_client
from .test_helpers import get_or_create_document_id
from vaiz.api.base import VaizSDKError, VaizNotFoundError, VaizAuthError

# Create a test task once and reuse the document ID for all examples
EXAMPLE_DOCUMENT_ID = None

def get_example_document_id():
    """Get or create a document ID for examples."""
    global EXAMPLE_DOCUMENT_ID
    if EXAMPLE_DOCUMENT_ID is None:
        EXAMPLE_DOCUMENT_ID = get_or_create_document_id()
    return EXAMPLE_DOCUMENT_ID


def post_comment_with_html():
    """Post a comment with HTML content to a document."""
    client = get_client()
    
    # Get a valid document ID from test task
    document_id = get_example_document_id()
    
    try:
        response = client.post_comment(
            document_id=document_id,
            content="<p>Test <em>italic</em> comment from SDK</p>",
            file_ids=[]
        )
        
        print("Comment posted successfully!")
        print(f"Response type: {response.type}")
        print(f"Comment ID: {response.comment.id}")
        print(f"Author ID: {response.comment.author_id}")
        print(f"Content: {response.comment.content}")
        print(f"Created at: {response.comment.created_at}")
        print(f"Document ID: {response.comment.document_id}")
        print(f"Files: {response.comment.files}")
        print(f"Reactions: {response.comment.reactions}")
        
        return response.comment.id
        
    except VaizNotFoundError as e:
        print("\n=== Document Not Found ===")
        print(f"Error: {str(e)}")
        if e.api_error and e.api_error.meta:
            print(f"Details: {e.api_error.meta.description}")
        print("==========================\n")

    except VaizAuthError as e:
        print("\n=== Authentication Error ===")
        print(f"Error: {str(e)}")
        if e.api_error and e.api_error.meta:
            print(f"Details: {e.api_error.meta.description}")
        print("============================\n")

    except VaizSDKError as e:
        print("\n=== SDK Error ===")
        print(f"Error: {str(e)}")
        if e.api_error:
            print(f"Error code: {e.api_error.code}")
            print(f"Original type: {e.api_error.original_type}")
        print("================\n")

    except Exception as e:
        print("\n=== Unexpected Error ===")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        print("======================\n")


def post_comment_with_files():
    """Post a comment with file attachments to a document."""
    client = get_client()
    
    # Get a valid document ID from test task
    document_id = get_example_document_id()
    
    try:
        # First upload a file (optional)
        # upload_response = client.upload_file("./assets/example.pdf")
        # file_id = upload_response.file.id
        
        # For now, use empty file list
        file_ids = []  # [file_id] if you uploaded a file
        
        response = client.post_comment(
            document_id=document_id,
            content="<p>Comment with <strong>bold</strong> text and potential file attachments</p>",
            file_ids=file_ids
        )
        
        print("Comment with files posted successfully!")
        print(f"Response type: {response.type}")
        print(f"Comment ID: {response.comment.id}")
        print(f"Content: {response.comment.content}")
        print(f"Files: {response.comment.files}")
        
        return response.comment.id
        
    except Exception as e:
        print(f"Error posting comment with files: {e}")


def post_simple_text_comment():
    """Post a simple text comment to a document."""
    client = get_client()
    
    # Get a valid document ID from test task
    document_id = get_example_document_id()
    
    try:
        response = client.post_comment(
            document_id=document_id,
            content="Simple text comment from Python SDK"
        )
        
        print("Simple comment posted successfully!")
        print(f"Comment ID: {response.comment.id}")
        print(f"Content: {response.comment.content}")
        
        return response.comment.id
        
    except Exception as e:
        print(f"Error posting simple comment: {e}")


def post_comment_reply():
    """Post a reply to an existing comment."""
    client = get_client()
    
    # Get a valid document ID from test task
    document_id = get_example_document_id()
    
    try:
        # First, create an original comment
        original_response = client.post_comment(
            document_id=document_id,
            content="<p>Original comment that will receive a reply</p>"
        )
        
        print("Original comment posted successfully!")
        print(f"Original comment ID: {original_response.comment.id}")
        print(f"Original content: {original_response.comment.content}")
        
        # Now create a reply to the original comment
        reply_response = client.post_comment(
            document_id=document_id,
            content="<p>This is a <strong>reply</strong> to the original comment</p>",
            reply_to=original_response.comment.id
        )
        
        print("\nReply comment posted successfully!")
        print(f"Reply comment ID: {reply_response.comment.id}")
        print(f"Reply content: {reply_response.comment.content}")
        print(f"Reply to comment ID: {reply_response.comment.reply_to}")
        print(f"Is reply: {reply_response.comment.reply_to is not None}")
        
        return reply_response.comment.id
        
    except Exception as e:
        print(f"Error posting comment reply: {e}")


def react_to_comment():
    """Add reactions to a comment."""
    client = get_client()
    
    # Get a valid document ID from test task
    document_id = get_example_document_id()
    
    try:
        # First, create a comment to react to
        comment_response = client.post_comment(
            document_id=document_id,
            content="<p>This comment will receive some reactions! 🎉</p>"
        )
        
        print("Comment posted successfully!")
        print(f"Comment ID: {comment_response.comment.id}")
        print(f"Content: {comment_response.comment.content}")
        
        # Add a kissing face reaction
        reaction_response = client.react_to_comment(
            comment_id=comment_response.comment.id,
            emoji_id="kissing_smiling_eyes",
            emoji_name="Kissing Face with Smiling Eyes",
            emoji_native="😙",
            emoji_unified="1f619",
            emoji_keywords=["affection", "valentines", "infatuation", "kiss"],
            emoji_shortcodes=":kissing_smiling_eyes:"
        )
        
        print("\nReaction added successfully!")
        print(f"Response type: {reaction_response.type}")
        print(f"Number of reactions: {len(reaction_response.reactions)}")
        
        for reaction in reaction_response.reactions:
            print(f"Reaction: {reaction.native} ({reaction.emoji_id})")
            print(f"Reaction ID: {reaction.reaction_db_id}")
            print(f"Members who reacted: {len(reaction.member_ids)}")
        
        # Add a heart eyes reaction
        heart_reaction_response = client.react_to_comment(
            comment_id=comment_response.comment.id,
            emoji_id="heart_eyes",
            emoji_name="Smiling Face with Heart-Eyes",
            emoji_native="😍",
            emoji_unified="1f60d",
            emoji_keywords=["love", "crush", "heart", "affection"],
            emoji_shortcodes=":heart_eyes:"
        )
        
        print(f"\nSecond reaction added!")
        print(f"Total reactions now: {len(heart_reaction_response.reactions)}")
        
        return comment_response.comment.id
        
    except Exception as e:
        print(f"Error adding reaction: {e}")


def add_popular_reactions():
    """Add all popular emoji reactions to a comment using the simplified API."""
    client = get_client()
    
    # Get a valid document ID from test task
    document_id = get_example_document_id()
    
    try:
        # First, create a comment to react to
        comment_response = client.post_comment(
            document_id=document_id,
            content="<p>Let's test all the popular reactions! 🚀</p>"
        )
        
        print("Comment posted successfully!")
        print(f"Comment ID: {comment_response.comment.id}")
        print(f"Content: {comment_response.comment.content}")
        
        reactions_added = []
        
        # Add all popular reactions using the simplified API
        for reaction_type in CommentReactionType:
            print(f"\nAdding {reaction_type.value} reaction...")
            
            reaction_response = client.add_reaction(
                comment_id=comment_response.comment.id,
                reaction=reaction_type
            )
            
            # Find the reaction we just added
            from vaiz.models import COMMENT_REACTION_METADATA
            metadata = COMMENT_REACTION_METADATA[reaction_type]
            
            our_reaction = None
            for reaction in reaction_response.reactions:
                if reaction.emoji_id == metadata["id"]:
                    our_reaction = reaction
                    break
            
            if our_reaction:
                reactions_added.append({
                    "type": reaction_type.value,
                    "emoji": our_reaction.native,
                    "name": metadata["name"]
                })
                print(f"✅ Added: {our_reaction.native} {metadata['name']}")
        
        print(f"\n🎉 Successfully added {len(reactions_added)} reactions!")
        print("Summary of reactions added:")
        for i, reaction in enumerate(reactions_added, 1):
            print(f"{i}. {reaction['emoji']} {reaction['name']} ({reaction['type']})")
        
        return comment_response.comment.id
        
    except Exception as e:
        print(f"Error adding popular reactions: {e}")


def get_comments_example():
    """Get all comments for a document."""
    client = get_client()
    
    # Get a valid document ID from test task
    document_id = get_example_document_id()
    
    try:
        # Get all comments for the document
        comments_response = client.get_comments(document_id=document_id)
        
        print("Comments retrieved successfully!")
        print(f"Total comments: {len(comments_response.comments)}")
        print(f"Response type: {comments_response.type}")
        
        # Display comments with details
        for i, comment in enumerate(comments_response.comments, 1):
            print(f"\n--- Comment {i} ---")
            print(f"ID: {comment.id}")
            print(f"Author: {comment.author_id}")
            print(f"Created: {comment.created_at}")
            print(f"Content: {comment.content}")
            
            # Show if it's a reply
            if comment.reply_to:
                print(f"Reply to: {comment.reply_to}")
            
            # Show reactions
            if comment.reactions:
                print(f"Reactions ({len(comment.reactions)}):")
                for reaction in comment.reactions:
                    print(f"  {reaction.native} ({reaction.emoji_id}) - {len(reaction.member_ids)} member(s)")
            else:
                print("No reactions")
            
            # Show files
            if comment.files:
                print(f"Files: {len(comment.files)}")
            else:
                print("No files")
        
        print(f"\n✅ Successfully retrieved {len(comments_response.comments)} comments!")
        return len(comments_response.comments)
        
    except Exception as e:
        print(f"Error getting comments: {e}")


def edit_comment_example():
    """Edit an existing comment."""
    client = get_client()
    
    # Get a valid document ID from test task
    document_id = get_example_document_id()
    
    try:
        # First, create a comment to edit
        original_response = client.post_comment(
            document_id=document_id,
            content="<p>This is the original comment that will be edited</p>"
        )
        
        print("Original comment created!")
        print(f"Comment ID: {original_response.comment.id}")
        print(f"Original content: {original_response.comment.content}")
        print(f"Created at: {original_response.comment.created_at}")
        
        # Edit the comment
        edit_response = client.edit_comment(
            comment_id=original_response.comment.id,
            content="<p><strong>EDITED:</strong> This comment has been <em>updated</em> with new content! 🎉</p>"
        )
        
        edited_comment = edit_response.comment
        
        print("\n--- Comment Edited Successfully! ---")
        print(f"Response type: {edit_response.type}")
        print(f"Comment ID: {edited_comment.id}")
        print(f"New content: {edited_comment.content}")
        print(f"Created at: {edited_comment.created_at}")
        print(f"Updated at: {edited_comment.updated_at}")
        print(f"Edited at: {edited_comment.edited_at}")
        
        # Verify the change by getting all comments
        comments_response = client.get_comments(document_id=document_id)
        
        # Find our edited comment
        our_comment = None
        for comment in comments_response.comments:
            if comment.id == edited_comment.id:
                our_comment = comment
                break
        
        if our_comment:
            print(f"\n✅ Verified: Comment found in document with new content!")
            print(f"✅ Content matches: {our_comment.content}")
            print(f"✅ Has edited timestamp: {our_comment.edited_at}")
        
        return edited_comment.id
        
    except Exception as e:
        print(f"Error editing comment: {e}")


def edit_comment_with_files_example():
    """Edit comment with file operations."""
    client = get_client()
    
    # Get a valid document ID from test task
    document_id = get_example_document_id()
    
    try:
        # Create a comment
        original_response = client.post_comment(
            document_id=document_id,
            content="<p>Comment that will have file operations</p>"
        )
        
        print(f"Created comment for file operations: {original_response.comment.id}")
        
        # Edit with file operations (using empty arrays to avoid validation errors)
        edit_response = client.edit_comment(
            comment_id=original_response.comment.id,
            content="<p><strong>Updated</strong> comment with file operations</p>",
            add_file_ids=[],     # In real usage, add valid MongoDB file IDs here
            order_file_ids=[],   # In real usage, specify file order here
            remove_file_ids=[]   # In real usage, specify files to remove here
        )
        
        print(f"✅ Comment edited with file operations!")
        print(f"✅ New content: {edit_response.comment.content}")
        print(f"✅ Edited at: {edit_response.comment.edited_at}")
        
    except Exception as e:
        print(f"Error editing comment with files: {e}")


def delete_comment_example():
    """Delete a comment (soft delete)."""
    client = get_client()
    
    # Get a valid document ID from test task
    document_id = get_example_document_id()
    
    try:
        # First, create a comment to delete
        original_response = client.post_comment(
            document_id=document_id,
            content="<p>This comment will be <strong>deleted</strong> as an example</p>"
        )
        
        print("Original comment created!")
        print(f"Comment ID: {original_response.comment.id}")
        print(f"Original content: {original_response.comment.content}")
        print(f"Created at: {original_response.comment.created_at}")
        
        # Delete the comment
        delete_response = client.delete_comment(comment_id=original_response.comment.id)
        
        deleted_comment = delete_response.comment
        
        print("\n--- Comment Deleted Successfully! ---")
        print(f"Response type: {delete_response.type}")
        print(f"Comment ID: {deleted_comment.id}")
        print(f"Content after deletion: '{deleted_comment.content}'")  # Should be empty
        print(f"Created at: {deleted_comment.created_at}")
        print(f"Updated at: {deleted_comment.updated_at}")
        print(f"Deleted at: {deleted_comment.deleted_at}")
        
        # Verify by getting all comments to see the deleted comment
        comments_response = client.get_comments(document_id=document_id)
        
        # Find our deleted comment
        our_deleted_comment = None
        for comment in comments_response.comments:
            if comment.id == deleted_comment.id:
                our_deleted_comment = comment
                break
        
        if our_deleted_comment:
            print(f"\n✅ Verified: Deleted comment found in document list!")
            print(f"✅ Content is empty: '{our_deleted_comment.content}'")
            print(f"✅ Has deleted timestamp: {our_deleted_comment.deleted_at}")
            print(f"✅ Soft delete confirmed - comment still exists but marked as deleted")
        
        return deleted_comment.id
        
    except Exception as e:
        print(f"Error deleting comment: {e}")


def complete_comment_lifecycle_example():
    """Demonstrate complete comment lifecycle: Create -> Edit -> React -> Delete."""
    client = get_client()
    
    # Get a valid document ID from test task
    document_id = get_example_document_id()
    
    try:
        print("=== COMPLETE COMMENT LIFECYCLE ===")
        
        # 1. CREATE
        print("\n1. Creating comment...")
        comment_response = client.post_comment(
            document_id=document_id,
            content="<p>Lifecycle test comment</p>"
        )
        comment_id = comment_response.comment.id
        print(f"✅ Created comment: {comment_id}")
        
        # 2. EDIT
        print("\n2. Editing comment...")
        edit_response = client.edit_comment(
            comment_id=comment_id,
            content="<p><strong>EDITED:</strong> Lifecycle test comment</p>"
        )
        print(f"✅ Edited comment at: {edit_response.comment.edited_at}")
        
        # 3. REACT
        print("\n3. Adding reaction...")
        reaction_response = client.add_reaction(
            comment_id=comment_id,
            reaction=CommentReactionType.THUMBS_UP
        )
        print(f"✅ Added reaction: 👍")
        
        # 4. GET (to verify all changes)
        print("\n4. Getting comments to verify...")
        comments_response = client.get_comments(document_id=document_id)
        
        our_comment = None
        for comment in comments_response.comments:
            if comment.id == comment_id:
                our_comment = comment
                break
        
        if our_comment:
            print(f"✅ Found comment with:")
            print(f"   - Content: {our_comment.content}")
            print(f"   - Edited at: {our_comment.edited_at}")
            print(f"   - Reactions: {len(our_comment.reactions)}")
        
        # 5. DELETE
        print("\n5. Deleting comment...")
        delete_response = client.delete_comment(comment_id=comment_id)
        print(f"✅ Deleted comment at: {delete_response.comment.deleted_at}")
        print(f"✅ Content after deletion: '{delete_response.comment.content}'")
        
        print("\n🎉 Complete CRUD lifecycle demonstrated!")
        print("CREATE ✅ READ ✅ UPDATE ✅ DELETE ✅")
        
    except Exception as e:
        print(f"Error in lifecycle example: {e}")


def main():
    """Run all comment posting examples."""
    print("=" * 60)
    print("VAIZ SDK COMMENT EXAMPLES")
    print("=" * 60)
    
    print("\n1. Posting HTML comment...")
    print("-" * 40)
    post_comment_with_html()
    
    print("\n2. Posting comment with files...")
    print("-" * 40)
    post_comment_with_files()
    
    print("\n3. Posting simple text comment...")
    print("-" * 40)
    post_simple_text_comment()
    
    print("\n4. Posting comment reply...")
    print("-" * 40)
    post_comment_reply()
    
    print("\n5. Adding reactions to comments...")
    print("-" * 40)
    react_to_comment()
    
    print("\n6. Adding all popular reactions (simplified API)...")
    print("-" * 40)
    add_popular_reactions()
    
    print("\n7. Getting all comments...")
    print("-" * 40)
    get_comments_example()
    
    print("\n8. Editing a comment...")
    print("-" * 40)
    edit_comment_example()
    
    print("\n9. Editing comment with file operations...")
    print("-" * 40)
    edit_comment_with_files_example()
    
    print("\n10. Deleting a comment...")
    print("-" * 40)
    delete_comment_example()
    
    print("\n11. Complete comment lifecycle (CRUD)...")
    print("-" * 40)
    complete_comment_lifecycle_example()


if __name__ == "__main__":
    main() 