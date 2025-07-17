"""
Example: Post a comment to a document using the Vaiz SDK.
This example demonstrates how to create comments with HTML content and optional file attachments.
"""

from vaiz.models import PostCommentRequest
from .config import get_client
from vaiz.api.base import VaizSDKError, VaizNotFoundError, VaizAuthError


def post_comment_with_html():
    """Post a comment with HTML content to a document."""
    client = get_client()
    
    # Example document ID - replace with actual document ID
    document_id = "68766185f2fdb46f0f91737d"
    
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
    
    # Example document ID - replace with actual document ID
    document_id = "68766185f2fdb46f0f91737d"
    
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
    
    # Example document ID - replace with actual document ID
    document_id = "68766185f2fdb46f0f91737d"
    
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
    
    # Example document ID - replace with actual document ID
    document_id = "68766185f2fdb46f0f91737d"
    
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


if __name__ == "__main__":
    main() 