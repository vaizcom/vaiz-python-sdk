"""
Example: Upload a file from URL using the Vaiz SDK.
"""

from .config import get_client
from vaiz.models.enums import EUploadFileType

def upload_image_from_url_example():
    """
    Example: Upload an image from URL with automatic type detection.
    """
    client = get_client()
    
    # Example image URL (replace with your actual URL)
    image_url = "https://httpbin.org/image/png"
    
    try:
        # Upload with automatic type detection
        response = client.upload_file_from_url(image_url)
        file = response.file
        print("Image uploaded successfully from URL!")
        print(f"ID: {file.id}")
        print(f"Name: {file.name}")
        print(f"URL: {file.url}")
        print(f"Type: {file.type}")
        print(f"Size: {file.size}")
        print(f"MIME: {file.mime}")
    except Exception as e:
        print(f"Error uploading image from URL: {e}")

def upload_pdf_from_url_with_explicit_type():
    """
    Example: Upload a PDF from URL with explicit type specification.
    """
    client = get_client()
    
    # Example PDF URL (replace with your actual URL)
    pdf_url = "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"
    
    try:
        # Upload with explicit file type and custom filename
        response = client.upload_file_from_url(
            file_url=pdf_url, 
            file_type=EUploadFileType.Pdf,
            filename="sample_document.pdf"
        )
        file = response.file
        print("PDF uploaded successfully from URL!")
        print(f"ID: {file.id}")
        print(f"Name: {file.name}")
        print(f"URL: {file.url}")
        print(f"Type: {file.type}")
        print(f"Size: {file.size}")
        print(f"MIME: {file.mime}")
    except Exception as e:
        print(f"Error uploading PDF from URL: {e}")

def upload_multiple_files_from_urls():
    """
    Example: Upload multiple files from different URLs.
    """
    client = get_client()
    
    # List of URLs with their types
    files_to_upload = [
        {
            "url": "https://httpbin.org/image/jpeg", 
            "type": EUploadFileType.Image,
            "filename": "httpbin_image.jpg"
        },
        {
            "url": "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf",
            "type": EUploadFileType.Pdf,
            "filename": "sample_document.pdf"
        },
    ]
    
    for file_info in files_to_upload:
        print(f"\nUploading: {file_info['filename']}")
        try:
            response = client.upload_file_from_url(
                file_url=file_info['url'],
                file_type=file_info['type'],
                filename=file_info['filename']
            )
            print(f"✓ Successfully uploaded {file_info['filename']}")
            print(f"  File ID: {response.file.id}")
            print(f"  File URL: {response.file.url}")
        except Exception as e:
            print(f"✗ Failed to upload {file_info['filename']}: {e}")

def upload_with_auto_detection_example():
    """
    Example: Upload files from URLs with automatic type detection.
    """
    client = get_client()
    
    # URLs with different file types for auto-detection
    urls = [
        "https://httpbin.org/image/png",  # Should detect as Image
        "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf",  # Should detect as PDF
    ]
    
    for url in urls:
        print(f"\nUploading from URL: {url}")
        try:
            response = client.upload_file_from_url(url)  # No explicit type
            file = response.file
            print(f"✓ Auto-detected type: {file.type}")
            print(f"  File name: {file.name}")
            print(f"  File ID: {file.id}")
        except Exception as e:
            print(f"✗ Error: {e}")

if __name__ == "__main__":
    print("=== Upload Image from URL with Auto-Detection ===")
    upload_image_from_url_example()
    
    print("\n=== Upload PDF from URL with Explicit Type ===")
    upload_pdf_from_url_with_explicit_type()
    
    print("\n=== Upload Multiple Files from URLs ===")
    upload_multiple_files_from_urls()
    
    print("\n=== Upload with Auto-Detection ===")
    upload_with_auto_detection_example() 