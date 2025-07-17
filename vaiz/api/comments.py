from vaiz.api.base import BaseAPIClient
from vaiz.models.comments import PostCommentRequest, PostCommentResponse, ReactToCommentRequest, ReactToCommentResponse, GetCommentsRequest, GetCommentsResponse, EditCommentRequest, EditCommentResponse, DeleteCommentRequest, DeleteCommentResponse
from vaiz.models.enums import CommentReactionType, COMMENT_REACTION_METADATA
from typing import List, Optional


class CommentsAPIClient(BaseAPIClient):
    """API client for comment operations."""
    
    def post_comment(
        self, 
        document_id: str, 
        content: str, 
        file_ids: Optional[List[str]] = None,
        reply_to: Optional[str] = None
    ) -> PostCommentResponse:
        """
        Post a comment to a document.
        
        Args:
            document_id (str): The ID of the document to comment on
            content (str): The comment content (can include HTML)
            file_ids (Optional[List[str]]): List of file IDs to attach to the comment
            reply_to (Optional[str]): ID of the comment to reply to (for threaded replies)
            
        Returns:
            PostCommentResponse: The created comment information
            
        Raises:
            VaizSDKError: If the API request fails
        """
        request = PostCommentRequest(
            document_id=document_id,
            content=content,
            file_ids=file_ids or [],
            reply_to=reply_to
        )
        
        response_data = self._make_request("postComment", json_data=request.model_dump())
        return PostCommentResponse(**response_data)
    
    def react_to_comment(
        self,
        comment_id: str,
        emoji_id: str,
        emoji_name: str,
        emoji_native: str,
        emoji_unified: str,
        emoji_keywords: Optional[List[str]] = None,
        emoji_shortcodes: Optional[str] = None
    ) -> ReactToCommentResponse:
        """
        Add a reaction to a comment.
        
        Args:
            comment_id (str): The ID of the comment to react to
            emoji_id (str): The emoji ID (e.g., "kissing_smiling_eyes")
            emoji_name (str): The human-readable emoji name (e.g., "Kissing Face with Smiling Eyes")
            emoji_native (str): The emoji character (e.g., "😙")
            emoji_unified (str): The Unicode codepoint (e.g., "1f619")
            emoji_keywords (Optional[List[str]]): Keywords for the emoji
            emoji_shortcodes (Optional[str]): Shortcode for the emoji (e.g., ":kissing_smiling_eyes:")
            
        Returns:
            ReactToCommentResponse: The reaction information
            
        Raises:
            VaizSDKError: If the API request fails
        """
        request = ReactToCommentRequest(
            comment_id=comment_id,
            id=emoji_id,
            name=emoji_name,
            native=emoji_native,
            unified=emoji_unified,
            keywords=emoji_keywords or [],
            shortcodes=emoji_shortcodes or f":{emoji_id}:"
        )
        
        response_data = self._make_request("reactToComment", json_data=request.model_dump())
        return ReactToCommentResponse(**response_data)
    
    def add_reaction(
        self,
        comment_id: str,
        reaction: CommentReactionType
    ) -> ReactToCommentResponse:
        """
        Add a popular emoji reaction to a comment (simplified API).
        
        Args:
            comment_id (str): The ID of the comment to react to
            reaction (CommentReactionType): The type of reaction to add
            
        Returns:
            ReactToCommentResponse: The reaction information
            
        Raises:
            VaizSDKError: If the API request fails
        """
        metadata = COMMENT_REACTION_METADATA[reaction]
        
        return self.react_to_comment(
            comment_id=comment_id,
            emoji_id=metadata["id"],
            emoji_name=metadata["name"],
            emoji_native=metadata["native"], 
            emoji_unified=metadata["unified"],
            emoji_keywords=metadata["keywords"],
            emoji_shortcodes=metadata["shortcodes"]
        )
    
    def get_comments(self, document_id: str) -> GetCommentsResponse:
        """
        Get all comments for a document.
        
        Args:
            document_id (str): The ID of the document to get comments for
            
        Returns:
            GetCommentsResponse: The list of comments for the document
            
        Raises:
            VaizSDKError: If the API request fails
        """
        request = GetCommentsRequest(document_id=document_id)
        
        response_data = self._make_request("getComments", json_data=request.model_dump())
        return GetCommentsResponse(**response_data)
    
    def edit_comment(
        self, 
        comment_id: str, 
        content: str, 
        add_file_ids: Optional[List[str]] = None,
        order_file_ids: Optional[List[str]] = None,
        remove_file_ids: Optional[List[str]] = None
    ) -> EditCommentResponse:
        """
        Edit an existing comment.
        
        Args:
            comment_id (str): The ID of the comment to edit
            content (str): The new content for the comment (HTML supported)
            add_file_ids (Optional[List[str]]): File IDs to add to the comment
            order_file_ids (Optional[List[str]]): File IDs in new order
            remove_file_ids (Optional[List[str]]): File IDs to remove from the comment
            
        Returns:
            EditCommentResponse: The updated comment
            
        Raises:
            VaizSDKError: If the API request fails
        """
        request = EditCommentRequest(
            content=content,
            comment_id=comment_id,
            add_file_ids=add_file_ids or [],
            order_file_ids=order_file_ids or [],
            remove_file_ids=remove_file_ids or []
        )
        
        response_data = self._make_request("editComment", json_data=request.model_dump())
        return EditCommentResponse(**response_data)
    
    def delete_comment(self, comment_id: str) -> DeleteCommentResponse:
        """
        Delete a comment (soft delete).
        
        Args:
            comment_id (str): The ID of the comment to delete
            
        Returns:
            DeleteCommentResponse: The deleted comment with deleted_at timestamp
            
        Raises:
            VaizSDKError: If the API request fails
        """
        request = DeleteCommentRequest(comment_id=comment_id)
        
        response_data = self._make_request("deleteComment", json_data=request.model_dump())
        return DeleteCommentResponse(**response_data) 