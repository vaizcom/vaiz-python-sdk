from vaiz.api.base import BaseAPIClient
from vaiz.models import UploadFileResponse
from vaiz.models.enums import EUploadFileType
from typing import IO, Optional
import os


class UploadAPIClient(BaseAPIClient):
    def upload_file(self, file_path: str, file_type: EUploadFileType) -> UploadFileResponse:
        """
        Upload a file to the Vaiz platform.

        Args:
            file_path (str): Path to the file to upload.
            file_type (EUploadFileType): Type of the file (Image, Video, Pdf, or File).
                - Image: Will display as image preview in interface
                - Video: Will display as video player in interface  
                - Pdf: Will display as PDF viewer in interface
                - File: Will display as downloadable file attachment

        Returns:
            UploadFileResponse: The uploaded file information.
        """
        url = f"{self.base_url}/UploadFile"
        with open(file_path, "rb") as f:
            files = {
                "file": (os.path.basename(file_path), f),
                "type": (None, file_type.value),
            }
            response = self.session.post(url, files=files, verify=self.verify_ssl)
        response.raise_for_status()
        response_data = response.json()
        return UploadFileResponse(**response_data) 