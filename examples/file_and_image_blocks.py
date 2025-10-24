"""
Example: Using File and Image Blocks in Documents

This example demonstrates how to:
1. Upload files to Vaiz
2. Create image blocks for images
3. Create files blocks for documents/PDFs
4. Combine them in rich document content
"""

from examples.config import get_client, SPACE_ID
from vaiz import (
    heading,
    paragraph,
    text,
    image_block,
    files_block,
    horizontal_rule,
)
from vaiz.models import CreateDocumentRequest, Kind
from vaiz.models.enums import UploadFileType
import os


def main():
    client = get_client()
    client.verbose = True
    
    print("=== Creating Document with File and Image Blocks ===\n")
    
    # Step 1: Upload files
    print("Step 1: Uploading files...")
    
    # Upload an image
    image_path = "assets/example.png"
    if not os.path.exists(image_path):
        print(f"⚠️  Image file not found: {image_path}")
        print("Skipping image upload...")
        image_uploaded = None
    else:
        image_uploaded = client.upload_file(image_path, file_type=UploadFileType.Image)
        print(f"✓ Uploaded image: {image_uploaded.file.name}")
        print(f"  File ID: {image_uploaded.file.id}")
        print(f"  URL: {image_uploaded.file.url}")
        print(f"  Size: {image_uploaded.file.size} bytes")
    
    # Upload a PDF
    pdf_path = "assets/example.pdf"
    if not os.path.exists(pdf_path):
        print(f"⚠️  PDF file not found: {pdf_path}")
        print("Skipping PDF upload...")
        pdf_uploaded = None
    else:
        pdf_uploaded = client.upload_file(pdf_path, file_type=UploadFileType.Pdf)
        print(f"✓ Uploaded PDF: {pdf_uploaded.file.name}")
        print(f"  File ID: {pdf_uploaded.file.id}")
        print(f"  URL: {pdf_uploaded.file.url}")
        print(f"  Size: {pdf_uploaded.file.size} bytes")
    
    # Step 2: Create document
    print("\nStep 2: Creating document...")
    
    create_request = CreateDocumentRequest(
        kind=Kind.Space,
        kind_id=SPACE_ID,
        title="Example: File and Image Blocks",
        index=0
    )
    doc_response = client.create_document(create_request)
    document_id = doc_response.payload.document.id
    print(f"✓ Created document: {document_id}")
    
    # Step 3: Build content with file and image blocks
    print("\nStep 3: Adding file and image blocks...")
    
    content = [
        heading(1, "Document with Files and Images"),
        
        paragraph(
            text("This document demonstrates file and image blocks.")
        ),
        
        horizontal_rule(),
    ]
    
    # Add image block if image was uploaded
    if image_uploaded:
        content.extend([
            heading(2, "Image Block Example"),
            
            paragraph(text("Here's an embedded image:")),
            
            # New simple API - just pass the file!
            image_block(file=image_uploaded.file),
            
            paragraph(text("Image displayed above", italic=True)),
            
            horizontal_rule(),
        ])
    
    # Add files block if files were uploaded
    files_to_attach = []
    
    if pdf_uploaded:
        files_to_attach.append({
            "fileId": pdf_uploaded.file.id,
            "url": pdf_uploaded.file.url,
            "name": pdf_uploaded.file.name,
            "size": pdf_uploaded.file.size,
            "extension": pdf_uploaded.file.ext,
            "type": "Pdf"  # Pdf, Image, Video, etc.
        })
    
    # You can add more files here
    # if another_file_uploaded:
    #     files_to_attach.append({...})
    
    if files_to_attach:
        content.extend([
            heading(2, "Files Block Example"),
            
            paragraph(text("Attached files:")),
            
            files_block(*files_to_attach),
            
            paragraph(
                text(f"{len(files_to_attach)} file(s) attached above", italic=True)
            ),
            
            horizontal_rule(),
        ])
    
    # Add summary
    content.extend([
        heading(2, "Summary"),
        
        paragraph(
            text("This document contains:", bold=True)
        ),
        
        paragraph(
            text(f"• Image blocks: {1 if image_uploaded else 0}")
        ),
        paragraph(
            text(f"• Files blocks: {1 if files_to_attach else 0}")
        ),
        paragraph(
            text(f"• Total files: {len(files_to_attach) + (1 if image_uploaded else 0)}")
        ),
    ])
    
    # Step 4: Update document
    try:
        client.replace_json_document(document_id, content)
        print("\n✅ Document updated successfully with file and image blocks!")
        print(f"\n🔗 View document: https://vaiz.app/document/{document_id}")
        
        # Verify blocks were created
        print("\nVerifying blocks...")
        doc_content = client.get_json_document(document_id)
        
        image_block_count = 0
        files_block_count = 0
        
        for node in doc_content.get("default", {}).get("content", []):
            if node.get("type") == "image-block":
                image_block_count += 1
            elif node.get("type") == "files":
                files_block_count += 1
        
        print(f"✓ Found {image_block_count} image block(s)")
        print(f"✓ Found {files_block_count} files block(s)")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n=== Example completed ===")


if __name__ == "__main__":
    main()

