from vaiz.api.base import BaseAPIClient
from vaiz.models.documents import (
    ReplaceMarkdownDocumentRequest,
    ReplaceMarkdownDocumentResponse,
    AppendMarkdownDocumentRequest,
    AppendMarkdownDocumentResponse,
    GetMarkdownDocumentRequest,
    GetMarkdownDocumentResponse,
    GetDocumentsRequest,
    GetDocumentsResponse,
    CreateDocumentRequest,
    CreateDocumentResponse,
    EditDocumentRequest,
    EditDocumentResponse
)


class DocumentsAPIClient(BaseAPIClient):
    """API client for document content operations."""

    def replace_markdown_document(self, document_id: str, markdown: str) -> ReplaceMarkdownDocumentResponse:
        """
        Replace document content with Markdown content.

        This is the recommended way to write rich document content. Markdown is
        converted to native document blocks on the server (headings, lists,
        tables, code blocks, checklists, links, etc.).

        Args:
            document_id: The document ID to replace content for
            markdown: New content as a Markdown string

        Returns:
            ReplaceMarkdownDocumentResponse: Empty response object on success

        Raises:
            VaizSDKError: If the API request fails

        Example:
            >>> client.replace_markdown_document(
            ...     document_id="doc_id",
            ...     markdown="# Title\\n\\nSome **bold** text\\n\\n- item 1\\n- item 2"
            ... )
        """
        request = ReplaceMarkdownDocumentRequest(
            document_id=document_id,
            markdown=markdown
        )

        response_data = self._make_request("replaceMarkdownDocument", json_data=request.model_dump())
        return ReplaceMarkdownDocumentResponse(**response_data)

    def append_markdown_document(self, document_id: str, markdown: str) -> AppendMarkdownDocumentResponse:
        """
        Append Markdown content to an existing document.

        This method adds content to the end of the document without removing
        existing content. Markdown is converted to native document blocks on
        the server.

        Args:
            document_id: The document ID to append content to
            markdown: Content to append as a Markdown string

        Returns:
            AppendMarkdownDocumentResponse: Empty response object on success

        Raises:
            VaizSDKError: If the API request fails

        Example:
            >>> client.append_markdown_document(
            ...     document_id="doc_id",
            ...     markdown="## Update\\n\\nAdditional notes"
            ... )
        """
        request = AppendMarkdownDocumentRequest(
            document_id=document_id,
            markdown=markdown
        )

        response_data = self._make_request("appendMarkdownDocument", json_data=request.model_dump())
        return AppendMarkdownDocumentResponse(**response_data)

    def get_markdown_document(self, document_id: str) -> str:
        """
        Fetch document content as Markdown.

        Returns the current document content rendered as Markdown. For legacy
        documents that have no rich content yet, an empty string is returned.

        Args:
            document_id: The document ID to fetch

        Returns:
            str: The document content as a Markdown string

        Raises:
            VaizSDKError: If the API request fails

        Example:
            >>> markdown = client.get_markdown_document("doc_id")
            >>> print(markdown)
            # Title
            Some **bold** text
        """
        request = GetMarkdownDocumentRequest(document_id=document_id)
        response_data = self._make_request("getMarkdownDocument", json_data=request.model_dump())
        response = GetMarkdownDocumentResponse(**response_data)
        return response.markdown

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

    def edit_document(self, request: EditDocumentRequest) -> EditDocumentResponse:
        """
        Edit an existing document (e.g., update title).

        Args:
            request (EditDocumentRequest): The request containing document_id and title

        Returns:
            EditDocumentResponse: The response containing the edited document

        Raises:
            VaizSDKError: If the API request fails
        """
        response_data = self._make_request("editDocument", json_data=request.model_dump())
        return EditDocumentResponse(**response_data)
