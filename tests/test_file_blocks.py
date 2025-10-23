"""
Tests for file and image block helper functions.
"""

import pytest
from vaiz.helpers import (
    image_block,
    files_block,
    paragraph,
    text,
    heading,
)
from vaiz.models import CreateDocumentRequest, Kind
from vaiz.models.enums import UploadFileType
from tests.test_config import get_test_client, TEST_SPACE_ID
import json


def test_image_block_structure():
    """Test creating an image block with correct structure."""
    result = image_block(
        file_id="test_file_id",
        src="http://example.com/image.png",
        file_name="test.png",
        file_size=12345,
        extension="png",
        file_type="image/png",
        dimensions=[800, 600]
    )
    
    assert result["type"] == "image-block"
    assert result["attrs"]["custom"] == 1
    assert result["attrs"]["contenteditable"] == "false"
    assert result["attrs"]["widthPercent"] == 100
    assert "uid" in result["attrs"]
    
    # Parse JSON content
    content_text = result["content"][0]["text"]
    image_data = json.loads(content_text)
    
    assert image_data["fileId"] == "test_file_id"
    assert image_data["src"] == "http://example.com/image.png"
    assert image_data["fileName"] == "test.png"
    assert image_data["fileSize"] == 12345
    assert image_data["dimensions"] == [800, 600]
    assert image_data["aspectRatio"] == 800 / 600


def test_image_block_with_caption():
    """Test creating an image block with caption."""
    result = image_block(
        file_id="test_id",
        src="http://example.com/image.png",
        file_name="test.png",
        file_size=1000,
        caption="Test caption"
    )
    
    content_text = result["content"][0]["text"]
    image_data = json.loads(content_text)
    
    assert image_data["caption"] == "Test caption"


def test_image_block_custom_width():
    """Test creating an image block with custom width."""
    result = image_block(
        file_id="test_id",
        src="http://example.com/image.png",
        file_name="test.png",
        file_size=1000,
        width_percent=50
    )
    
    assert result["attrs"]["widthPercent"] == 50


def test_files_block_single_file():
    """Test creating a files block with one file."""
    file_item = {
        "fileId": "test_file_id",
        "url": "http://example.com/file.pdf",
        "name": "document.pdf",
        "size": 54321,
        "extension": "pdf",
        "type": "Pdf"
    }
    
    result = files_block(file_item)
    
    assert result["type"] == "files"
    assert result["attrs"]["custom"] == 1
    assert result["attrs"]["contenteditable"] == "false"
    assert "uid" in result["attrs"]
    
    # Parse JSON content
    content_text = result["content"][0]["text"]
    files_data = json.loads(content_text)
    
    assert "files" in files_data
    assert len(files_data["files"]) == 1
    
    file = files_data["files"][0]
    assert file["fileId"] == "test_file_id"
    assert file["url"] == "http://example.com/file.pdf"
    assert file["name"] == "document.pdf"
    assert file["size"] == 54321
    assert file["extension"] == "pdf"
    assert file["type"] == "Pdf"
    assert "id" in file
    assert "createAt" in file


def test_files_block_multiple_files():
    """Test creating a files block with multiple files."""
    file1 = {
        "fileId": "file1",
        "url": "http://example.com/doc1.pdf",
        "name": "doc1.pdf",
        "size": 1000,
        "extension": "pdf",
        "type": "Pdf"
    }
    
    file2 = {
        "fileId": "file2",
        "url": "http://example.com/image.png",
        "name": "image.png",
        "size": 2000,
        "extension": "png",
        "type": "Image"
    }
    
    result = files_block(file1, file2)
    
    content_text = result["content"][0]["text"]
    files_data = json.loads(content_text)
    
    assert len(files_data["files"]) == 2
    assert files_data["files"][0]["fileId"] == "file1"
    assert files_data["files"][1]["fileId"] == "file2"


def test_files_block_unique_ids():
    """Test that each file in files block gets unique ID."""
    file1 = {
        "fileId": "same_file_id",
        "url": "http://example.com/file.pdf",
        "name": "file.pdf",
        "size": 1000,
        "extension": "pdf",
        "type": "Pdf"
    }
    
    file2 = {
        "fileId": "same_file_id",
        "url": "http://example.com/file.pdf",
        "name": "file.pdf",
        "size": 1000,
        "extension": "pdf",
        "type": "Pdf"
    }
    
    result = files_block(file1, file2)
    
    content_text = result["content"][0]["text"]
    files_data = json.loads(content_text)
    
    file_ids = [f["id"] for f in files_data["files"]]
    assert len(file_ids) == 2
    assert file_ids[0] != file_ids[1]  # Each should have unique internal ID


def test_create_document_with_file_blocks():
    """Integration test: Create document with real uploaded files."""
    client = get_test_client()
    
    # Upload test files
    image_path = "assets/example.png"
    pdf_path = "assets/example.pdf"
    
    # Upload image
    image_uploaded = client.upload_file(image_path, file_type=UploadFileType.Image)
    assert image_uploaded.file.id is not None
    
    # Upload PDF
    pdf_uploaded = client.upload_file(pdf_path, file_type=UploadFileType.Pdf)
    assert pdf_uploaded.file.id is not None
    
    # Create document
    create_request = CreateDocumentRequest(
        kind=Kind.Space,
        kind_id=TEST_SPACE_ID,
        title="Test: File and Image Blocks",
        index=0
    )
    
    doc_response = client.create_document(create_request)
    test_doc_id = doc_response.payload.document.id
    
    try:
        # Build content with file blocks
        content = [
            heading(1, "File Blocks Test"),
            
            paragraph(text("Image block:")),
            
            image_block(
                file_id=image_uploaded.file.id,
                src=image_uploaded.file.url,
                file_name=image_uploaded.file.name,
                file_size=image_uploaded.file.size,
                extension=image_uploaded.file.ext,
                file_type=image_uploaded.file.mime or "image/png",
                dimensions=image_uploaded.file.dimension if image_uploaded.file.dimension else None
            ),
            
            paragraph(text("Files block:")),
            
            files_block({
                "fileId": pdf_uploaded.file.id,
                "url": pdf_uploaded.file.url,
                "name": pdf_uploaded.file.name,
                "size": pdf_uploaded.file.size,
                "extension": pdf_uploaded.file.ext,
                "type": "Pdf"
            })
        ]
        
        # Replace document content
        client.replace_json_document(test_doc_id, content)
        
        # Verify blocks were created
        doc_content = client.get_json_document(test_doc_id)
        
        assert doc_content is not None
        assert "default" in doc_content
        assert "content" in doc_content["default"]
        
        doc_nodes = doc_content["default"]["content"]
        
        # Find file blocks
        image_blocks = [n for n in doc_nodes if n.get("type") == "image-block"]
        files_blocks = [n for n in doc_nodes if n.get("type") == "files"]
        
        assert len(image_blocks) == 1, "Image block not found"
        assert len(files_blocks) == 1, "Files block not found"
        
        # Verify image block structure
        image_block_node = image_blocks[0]
        assert "content" in image_block_node
        image_content = image_block_node["content"][0]["text"]
        image_data = json.loads(image_content)
        assert image_data["fileId"] == image_uploaded.file.id
        
        # Verify files block structure
        files_block_node = files_blocks[0]
        assert "content" in files_block_node
        files_content = files_block_node["content"][0]["text"]
        files_data = json.loads(files_content)
        assert "files" in files_data
        assert len(files_data["files"]) == 1
        assert files_data["files"][0]["fileId"] == pdf_uploaded.file.id
        
        print(f"\n✅ Successfully created and verified document with file blocks")
        print(f"   Document ID: {test_doc_id}")
        print(f"   Image block: {image_uploaded.file.name}")
        print(f"   Files block: {pdf_uploaded.file.name}")
        print(f"   View at: https://vaiz.app/document/{test_doc_id}")
        
    finally:
        pass  # Could add cleanup here


if __name__ == "__main__":
    test_create_document_with_file_blocks()

