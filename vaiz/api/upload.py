from vaiz.api.base import BaseAPIClient
from vaiz.models import UploadFileResponse
from typing import IO, Optional
import os

class UploadAPIClient(BaseAPIClient):
    def upload_file(self, file_path: str, file_type: str = "Pdf") -> UploadFileResponse:
        """
        Upload a file to the Vaiz platform.

        Args:
            file_path (str): Path to the file to upload.
            file_type (str): Type of the file (e.g., "Pdf").

        Returns:
            UploadFileResponse: The uploaded file information.
        """
        url = f"{self.base_url}/UploadFile"
        with open(file_path, "rb") as f:
            files = {
                "file": (os.path.basename(file_path), f),
                "type": (None, file_type),
            }
            response = self.session.post(url, files=files, verify=self.verify_ssl)
        response.raise_for_status()
        response_data = response.json()
        return UploadFileResponse(**response_data) 