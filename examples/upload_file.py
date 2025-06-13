"""
Example: Upload a file using the Vaiz SDK.
"""

from .config import get_client

def upload_file_example():
    client = get_client()
    file_path = "./example.pdf"  # Замените на путь к вашему файлу
    file_type = "Pdf"
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

if __name__ == "__main__":
    upload_file_example() 