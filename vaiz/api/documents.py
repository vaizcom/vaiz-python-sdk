from typing import Any, Dict, List, Union, Optional
import json

from vaiz.api.base import BaseAPIClient
from vaiz.models.documents import (
    GetDocumentRequest, 
    ReplaceDocumentRequest, 
    ReplaceDocumentResponse,
    ReplaceJSONDocumentRequest,
    ReplaceJSONDocumentResponse,
    AppendDocumentRequest,
    AppendDocumentResponse,
    AppendJSONDocumentRequest,
    AppendJSONDocumentResponse,
    GetDocumentsRequest,
    GetDocumentsResponse,
    CreateDocumentRequest,
    CreateDocumentResponse
)

# Import Document Structure types for better type hints
try:
    from vaiz.helpers.document_structure import DocumentNode
except ImportError:
    DocumentNode = Dict[str, Any]  # Fallback if typing_extensions not available

class DocumentsAPIClient(BaseAPIClient):
    """API client for document content operations."""

    def get_json_document(self, document_id: str) -> Dict[str, Any]:
        """
        Fetch JSON document content by document ID.

        This universal method allows retrieving the content of a task description
        or a standalone document body.

        Args:
            document_id: The document ID to fetch

        Returns:
            Dict[str, Any]: The JSON document as returned by the API (unmodeled)
        """
        request = GetDocumentRequest(document_id=document_id)
        response_data = self._make_request("getJSONDocument", json_data=request.model_dump())
        # API returns shape: { payload: { json: "{...}" }, type: "GetJSONDocument" }
        payload = response_data.get("payload", {})
        json_str = payload.get("json", "{}")
        try:
            parsed = json.loads(json_str)
        except (TypeError, json.JSONDecodeError):
            parsed = {}
        return parsed

    def replace_document(self, document_id: str, description: str) -> ReplaceDocumentResponse:
        """
        Replace document content completely.

        Args:
            document_id: The document ID to replace content for
            description: New description content as plain text string

        Returns:
            ReplaceDocumentResponse: Empty response object on success

        Raises:
            VaizSDKError: If the API request fails
        """
        request = ReplaceDocumentRequest(
            document_id=document_id,
            description=description
        )
        
        response_data = self._make_request("replaceDocument", json_data=request.model_dump())
        return ReplaceDocumentResponse(**response_data)

    def replace_json_document(
        self, 
        document_id: str, 
        content: Union[List[DocumentNode], List[Dict[str, Any]]]
    ) -> ReplaceJSONDocumentResponse:
        """
        Replace document content with structured JSON content.
        
        This method allows you to replace document content with structured JSON content
        using the document editor format. This is useful when you need to set rich content with
        specific formatting, links, lists, etc.
        
        **Tip:** Use document structure builder functions from `vaiz` for type-safe content creation:
        `text()`, `paragraph()`, `heading()`, `bullet_list()`, `ordered_list()`, `link_text()`

        Args:
            document_id: The document ID to replace content for
            content: JSONContent array in document structure format, or use helper functions

        Returns:
            ReplaceJSONDocumentResponse: Empty response object on success

        Raises:
            VaizSDKError: If the API request fails
            
        Example with raw JSON:
            >>> content = [
            ...     {
            ...         "type": "paragraph",
            ...         "content": [
            ...             {"type": "text", "text": "Hello, "},
            ...             {"type": "text", "marks": [{"type": "bold"}], "text": "World"}
            ...         ]
            ...     }
            ... ]
            >>> client.replace_json_document(document_id, content)
            
        Example with helper functions:
            >>> from vaiz import paragraph, text, heading
            >>> content = [
            ...     heading(1, "Welcome"),
            ...     paragraph(
            ...         "Hello, ",
            ...         text("World", bold=True)
            ...     )
            ... ]
            >>> client.replace_json_document(document_id, content)
        """
        request = ReplaceJSONDocumentRequest(
            document_id=document_id,
            content=content
        )
        
        response_data = self._make_request("replaceJSONDocument", json_data=request.model_dump())
        return ReplaceJSONDocumentResponse(**response_data)

    def append_document(
        self,
        document_id: str,
        description: Optional[str] = None,
        files: Optional[List[Any]] = None
    ) -> AppendDocumentResponse:
        """
        Append plain text content to an existing document.
        
        This method adds content to the end of the document without removing existing content.

        Args:
            document_id: The document ID to append content to
            description: Plain text content to append (optional)
            files: Files to attach (optional)

        Returns:
            AppendDocumentResponse: Empty response object on success

        Raises:
            VaizSDKError: If the API request fails
            
        Example:
            >>> client.append_document(
            ...     document_id="doc_id",
            ...     description="Additional content to add"
            ... )
        """
        request = AppendDocumentRequest(
            document_id=document_id,
            description=description,
            files=files
        )
        
        response_data = self._make_request("appendDocument", json_data=request.model_dump())
        return AppendDocumentResponse(**response_data)

    def append_json_document(
        self,
        document_id: str,
        content: Union[List[DocumentNode], List[Dict[str, Any]]]
    ) -> AppendJSONDocumentResponse:
        """
        Append structured JSON content to an existing document.
        
        This method adds content to the end of the document without removing existing content.
        Use document structure builder functions for type-safe content creation.

        Args:
            document_id: The document ID to append content to
            content: JSONContent array in document structure format

        Returns:
            AppendJSONDocumentResponse: Empty response object on success

        Raises:
            VaizSDKError: If the API request fails
            
        Example with raw JSON:
            >>> content = [
            ...     {
            ...         "type": "paragraph",
            ...         "content": [{"type": "text", "text": "Added content"}]
            ...     }
            ... ]
            >>> client.append_json_document(document_id, content)
            
        Example with helpers:
            >>> from vaiz import paragraph, text
            >>> content = [
            ...     paragraph("Added ", text("content", bold=True))
            ... ]
            >>> client.append_json_document(document_id, content)
        """
        request = AppendJSONDocumentRequest(
            document_id=document_id,
            content=content
        )
        
        response_data = self._make_request("appendJSONDocument", json_data=request.model_dump())
        return AppendJSONDocumentResponse(**response_data)

    def get_documents(self, request: GetDocumentsRequest) -> GetDocumentsResponse:
        """
        Get list of documents by kind and kind ID.

        Args:
            request (GetDocumentsRequest): The request containing kind and kindId

        Returns:
            GetDocumentsResponse: The response containing the list of documents

        Raises:
            VaizSDKError: If the API request fails
        """
        response_data = self._make_request("getDocuments", json_data=request.model_dump())
        return GetDocumentsResponse(**response_data)

    def create_document(self, request: CreateDocumentRequest) -> CreateDocumentResponse:
        """
        Create a new document.

        Args:
            request (CreateDocumentRequest): The request containing document details

        Returns:
            CreateDocumentResponse: The response containing the created document

        Raises:
            VaizSDKError: If the API request fails
        """
        response_data = self._make_request("createDocument", json_data=request.model_dump())
        return CreateDocumentResponse(**response_data)


