"""
Example: Upload a file using the Vaiz SDK.
"""

from .config import get_client
from vaiz.models.enums import EUploadFileType

def upload_file_example():
    client = get_client()
    file_path = "./assets/example.pdf"  # Replace with path to your file
    file_type = EUploadFileType.Pdf
    try:
        response = client.upload_file(file_path, file_type=file_type)
        file = response.file
        print("File uploaded successfully!")
        print(f"ID: {file.id}")
        print(f"Name: {file.name}")
        print(f"URL: {file.url}")
        print(f"Type: {file.type}")
        print(f"Size: {file.size}")
        print(f"MIME: {file.mime}")
    except Exception as e:
        print(f"Error uploading file: {e}")

def upload_different_file_types_example():
    """
    Example of uploading different file types using enum
    """
    client = get_client()
    
    # Examples of using different file types
    file_types = [
        ("./image.jpg", EUploadFileType.Image),
        ("./document.pdf", EUploadFileType.Pdf),
        ("./video.mp4", EUploadFileType.Video),
        ("./file.txt", EUploadFileType.File),
    ]
    
    for file_path, file_type in file_types:
        print(f"\nUploading file type: {file_type.value}")
        try:
            response = client.upload_file(file_path, file_type=file_type)
            print(f"File {file_path} successfully uploaded as {response.file.type}")
        except FileNotFoundError:
            print(f"File {file_path} not found")
        except Exception as e:
            print(f"Error uploading {file_path}: {e}")

if __name__ == "__main__":
    upload_file_example()
    # Uncomment to demonstrate different file types
    # upload_different_file_types_example() 