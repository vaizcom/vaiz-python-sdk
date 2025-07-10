import pytest
import os
from tests.test_config import get_test_client
from vaiz.models.enums import EUploadFileType

@pytest.fixture(scope="module")
def client():
    return get_test_client()

def test_upload_pdf_file(client):
    """Test uploading a real PDF file from assets."""
    file_path = "./assets/example.pdf"
    if not os.path.exists(file_path):
        pytest.skip(f"Test file {file_path} not found")
    
    try:
        response = client.upload_file(file_path, file_type=EUploadFileType.Pdf)
    except Exception as e:
        if hasattr(e, 'response') and e.response is not None:
            print("SERVER RESPONSE:", e.response.text)
        raise
    
    assert response.type == "UploadFile"
    file = response.file
    assert file.url.startswith("http")
    assert file.name == "example.pdf"
    assert file.type == EUploadFileType.Pdf
    assert file.mime == "application/pdf"
    assert file.size > 0

def test_upload_image_file(client):
    """Test uploading a real image file from assets."""
    file_path = "./assets/example.png"
    if not os.path.exists(file_path):
        pytest.skip(f"Test file {file_path} not found")
    
    try:
        response = client.upload_file(file_path, file_type=EUploadFileType.Image)
    except Exception as e:
        if hasattr(e, 'response') and e.response is not None:
            print("SERVER RESPONSE:", e.response.text)
        raise
    
    assert response.type == "UploadFile"
    file = response.file
    assert file.url.startswith("http")
    assert file.name == "example.png"
    assert file.type == EUploadFileType.Image
    assert file.mime == "image/png"
    assert file.size > 0

def test_upload_video_file(client):
    """Test uploading a real video file from assets."""
    file_path = "./assets/example.mp4"
    if not os.path.exists(file_path):
        pytest.skip(f"Test file {file_path} not found")
    
    try:
        response = client.upload_file(file_path, file_type=EUploadFileType.Video)
    except Exception as e:
        if hasattr(e, 'response') and e.response is not None:
            print("SERVER RESPONSE:", e.response.text)
        raise
    
    assert response.type == "UploadFile"
    file = response.file
    assert file.url.startswith("http")
    assert file.name == "example.mp4"
    assert file.type == EUploadFileType.Video
    assert file.mime == "video/mp4"
    assert file.size > 0

def test_upload_file_with_default_type(client):
    """Test uploading a file with default file type (Pdf)."""
    file_path = "./assets/example.pdf"
    if not os.path.exists(file_path):
        pytest.skip(f"Test file {file_path} not found")
    
    try:
        response = client.upload_file(file_path)  # No file_type specified
    except Exception as e:
        if hasattr(e, 'response') and e.response is not None:
            print("SERVER RESPONSE:", e.response.text)
        raise
    
    assert response.type == "UploadFile"
    file = response.file
    assert file.url.startswith("http")
    assert file.name == "example.pdf"
    assert file.type == EUploadFileType.Pdf  # Default type
    assert file.mime == "application/pdf"
    assert file.size > 0

def test_upload_multiple_files(client):
    """Test uploading multiple real files from assets."""
    files_to_upload = [
        ("./assets/example.pdf", EUploadFileType.Pdf),
        ("./assets/example.png", EUploadFileType.Image),
        ("./assets/example.mp4", EUploadFileType.Video)
    ] 