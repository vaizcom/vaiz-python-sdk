from vaiz.api.base import BaseAPIClient
from vaiz.models import UploadFileResponse
from vaiz.models.enums import UploadFileType
from typing import IO, Optional
import os
import requests
import tempfile
from urllib.parse import urlparse


class UploadAPIClient(BaseAPIClient):
    def upload_file(self, file_path: str, file_type: UploadFileType) -> UploadFileResponse:
        """
        Upload a file to the Vaiz platform.

        Args:
            file_path (str): Path to the file to upload.
            file_type (UploadFileType): Type of the file (Image, Video, Pdf, or File).
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

    def upload_file_from_url(self, file_url: str, file_type: Optional[UploadFileType] = None, filename: Optional[str] = None) -> UploadFileResponse:
        """
        Upload a file from URL to the Vaiz platform.

        Args:
            file_url (str): URL of the file to download and upload.
            file_type (Optional[UploadFileType]): Type of the file. If not provided, will try to detect from URL or content type.
            filename (Optional[str]): Custom filename for the uploaded file. If not provided, will extract from URL.

        Returns:
            UploadFileResponse: The uploaded file information.

        Raises:
            requests.RequestException: If the file cannot be downloaded from URL.
            ValueError: If file type cannot be determined.
        """
        # Download file from URL
        download_response = requests.get(file_url, stream=True, verify=self.verify_ssl)
        download_response.raise_for_status()
        
        # Determine filename if not provided
        if filename is None:
            parsed_url = urlparse(file_url)
            filename = os.path.basename(parsed_url.path) or "downloaded_file"
        
        # Determine file type if not provided
        if file_type is None:
            file_type = self._detect_file_type_from_url_and_content(file_url, download_response.headers.get('content-type'))
        
        # Create temporary file and upload
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            try:
                # Write downloaded content to temporary file
                for chunk in download_response.iter_content(chunk_size=8192):
                    temp_file.write(chunk)
                temp_file.flush()
                
                # Upload the temporary file
                url = f"{self.base_url}/UploadFile"
                with open(temp_file.name, "rb") as f:
                    files = {
                        "file": (filename, f),
                        "type": (None, file_type.value),
                    }
                    response = self.session.post(url, files=files, verify=self.verify_ssl)
                response.raise_for_status()
                response_data = response.json()
                return UploadFileResponse(**response_data)
            finally:
                # Clean up temporary file
                try:
                    os.unlink(temp_file.name)
                except OSError:
                    pass

    def _detect_file_type_from_url_and_content(self, file_url: str, content_type: Optional[str]) -> UploadFileType:
        """
        Detect file type from URL extension and content type.

        Args:
            file_url (str): URL of the file.
            content_type (Optional[str]): Content-Type header from the download response.

        Returns:
            UploadFileType: Detected file type.

        Raises:
            ValueError: If file type cannot be determined.
        """
        # First try to detect from URL extension
        parsed_url = urlparse(file_url)
        file_path = parsed_url.path.lower()
        
        # Image extensions
        if any(file_path.endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg']):
            return UploadFileType.Image
        
        # Video extensions
        if any(file_path.endswith(ext) for ext in ['.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm', '.mkv']):
            return UploadFileType.Video
        
        # PDF extension
        if file_path.endswith('.pdf'):
            return UploadFileType.Pdf
        
        # Try to detect from content type if URL extension didn't work
        if content_type:
            content_type = content_type.lower()
            if content_type.startswith('image/'):
                return UploadFileType.Image
            elif content_type.startswith('video/'):
                return UploadFileType.Video
            elif content_type == 'application/pdf':
                return UploadFileType.Pdf
        
        # Default to File type if cannot determine
        return UploadFileType.File 