from typing import Any, Dict, List
import json

from vaiz.api.base import BaseAPIClient
from vaiz.models.documents import GetDocumentRequest, ReplaceDocumentRequest, ReplaceDocumentResponse


class DocumentsAPIClient(BaseAPIClient):
    """API client for document content operations."""

    def get_document_body(self, document_id: str) -> Dict[str, Any]:
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

    def replace_document(self, document_id: str, description: str, files: List[str] = None) -> ReplaceDocumentResponse:
        """
        Replace document content completely.

        Args:
            document_id: The document ID to replace content for
            description: New description content as plain text string
            files: List of file IDs to attach to the document

        Returns:
            ReplaceDocumentResponse: Empty response object on success

        Raises:
            VaizSDKError: If the API request fails
        """
        if files is None:
            files = []
            
        request = ReplaceDocumentRequest(
            document_id=document_id,
            description=description,
            files=files
        )
        
        response_data = self._make_request("replaceDocument", json_data=request.model_dump())
        return ReplaceDocumentResponse(**response_data)


