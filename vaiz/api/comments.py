from vaiz.api.base import BaseAPIClient
from vaiz.models.comments import PostCommentRequest, PostCommentResponse
from typing import List, Optional


class CommentsAPIClient(BaseAPIClient):
    """API client for comment operations."""
    
    def post_comment(
        self, 
        document_id: str, 
        content: str, 
        file_ids: Optional[List[str]] = None
    ) -> PostCommentResponse:
        """
        Post a comment to a document.
        
        Args:
            document_id (str): The ID of the document to comment on
            content (str): The comment content (can include HTML)
            file_ids (Optional[List[str]]): List of file IDs to attach to the comment
            
        Returns:
            PostCommentResponse: The created comment information
            
        Raises:
            VaizSDKError: If the API request fails
        """
        request = PostCommentRequest(
            document_id=document_id,
            content=content,
            file_ids=file_ids or []
        )
        
        response_data = self._make_request("postComment", json_data=request.model_dump())
        return PostCommentResponse(**response_data) 