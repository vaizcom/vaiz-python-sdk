"""
Example: Comprehensive Document with All Block Types

This example demonstrates combining mentions, files, images, tables,
and other document elements in one rich document.
"""

from examples.config import get_client, SPACE_ID
from vaiz import (
    heading,
    paragraph,
    text,
    bullet_list,
    list_item,
    table,
    table_row,
    table_header,
    table_cell,
    horizontal_rule,
    blockquote,
    mention_user,
    mention_task,
    mention_document,
    image_block,
    files_block,
)
from vaiz.models import CreateDocumentRequest, Kind, GetDocumentsRequest, GetTasksRequest
from vaiz.models.enums import UploadFileType
import os


def main():
    client = get_client()
    client.verbose = True
    
    print("=== Creating Comprehensive Document with All Block Types ===\n")
    
    # Step 1: Get entity IDs for mentions
    print("Step 1: Getting entity IDs...")
    
    profile = client.get_profile()
    member_id = profile.profile.member_id
    print(f"✓ Member ID: {member_id}")
    
    docs_response = client.get_documents(
        GetDocumentsRequest(kind=Kind.Space, kind_id=SPACE_ID)
    )
    ref_doc_id = docs_response.payload.documents[0].id if docs_response.payload.documents else None
    if ref_doc_id:
        print(f"✓ Reference Document ID: {ref_doc_id}")
    
    tasks_response = client.get_tasks(GetTasksRequest())
    task_id = tasks_response.payload.tasks[0].id if tasks_response.payload.tasks else None
    if task_id:
        print(f"✓ Task ID: {task_id}")
    
    # Step 2: Upload files
    print("\nStep 2: Uploading files...")
    
    image_path = "assets/example.png"
    pdf_path = "assets/example.pdf"
    
    image_uploaded = None
    if os.path.exists(image_path):
        image_uploaded = client.upload_file(image_path, file_type=UploadFileType.Image)
        print(f"✓ Uploaded image: {image_uploaded.file.name}")
    
    pdf_uploaded = None
    if os.path.exists(pdf_path):
        pdf_uploaded = client.upload_file(pdf_path, file_type=UploadFileType.Pdf)
        print(f"✓ Uploaded PDF: {pdf_uploaded.file.name}")
    
    # Step 3: Create document
    print("\nStep 3: Creating document...")
    
    create_request = CreateDocumentRequest(
        kind=Kind.Space,
        kind_id=SPACE_ID,
        title="Comprehensive Example: All Block Types",
        index=0
    )
    doc_response = client.create_document(create_request)
    document_id = doc_response.payload.document.id
    print(f"✓ Created document: {document_id}")
    
    # Step 4: Build rich content with all block types
    print("\nStep 4: Building comprehensive content...")
    
    content = [
        heading(1, "📋 Project Status Report"),
        
        paragraph(
            text("Report Date: 2025-10-23", bold=True),
            text(" | Prepared by: "),
            mention_user(member_id) if member_id else text("Team")
        ),
        
        horizontal_rule(),
        
        # Section with task assignment
        heading(2, "👥 Team Assignments"),
        
        paragraph(
            text("Current assignee: "),
            mention_user(member_id) if member_id else text("TBD")
        ),
    ]
    
    # Add table with mentions if task available
    if task_id and member_id:
        content.extend([
            paragraph(text("Task assignments table:")),
            
            table(
                table_row(
                    table_header("Assignee"),
                    table_header("Task"),
                    table_header("Status")
                ),
                table_row(
                    table_cell(paragraph(mention_user(member_id))),
                    table_cell(paragraph(mention_task(task_id))),
                    table_cell("In Progress")
                )
            ),
        ])
    
    content.append(horizontal_rule())
    
    # Section with image
    if image_uploaded:
        content.extend([
            heading(2, "📸 Visual Assets"),
            
            paragraph(text("Project screenshot:")),
            
            image_block(
                file_id=image_uploaded.file.id,
                src=image_uploaded.file.url,
                file_name=image_uploaded.file.name,
                file_size=image_uploaded.file.size,
                extension=image_uploaded.file.ext,
                file_type=image_uploaded.file.mime or "image/png",
                dimensions=image_uploaded.file.dimension if image_uploaded.file.dimension else None,
                caption="Project Screenshot",
                width_percent=80
            ),
            
            paragraph(text("Image caption: Project Screenshot", italic=True)),
            
            horizontal_rule(),
        ])
    
    # Section with files
    files_to_attach = []
    
    if pdf_uploaded:
        files_to_attach.append({
            "fileId": pdf_uploaded.file.id,
            "url": pdf_uploaded.file.url,
            "name": pdf_uploaded.file.name,
            "size": pdf_uploaded.file.size,
            "extension": pdf_uploaded.file.ext,
            "type": "Pdf"
        })
    
    if files_to_attach:
        content.extend([
            heading(2, "📎 Attached Documents"),
            
            paragraph(text("Reference materials:")),
            
            files_block(*files_to_attach),
            
            paragraph(
                text(f"{len(files_to_attach)} document(s) attached", italic=True)
            ),
            
            horizontal_rule(),
        ])
    
    # Section with references
    if ref_doc_id:
        content.extend([
            heading(2, "🔗 Related Resources"),
            
            bullet_list(
                list_item(paragraph(
                    text("Reference document: "),
                    mention_document(ref_doc_id)
                )),
                list_item(paragraph(
                    text("Task link: "),
                    mention_task(task_id) if task_id else text("N/A")
                ))
            ),
            
            horizontal_rule(),
        ])
    
    # Summary section
    content.extend([
        heading(2, "📊 Summary"),
        
        blockquote(
            paragraph(
                text("This document demonstrates all supported block types:", bold=True)
            ),
            paragraph("• Headings and formatted text"),
            paragraph("• User mentions and task references"),
            paragraph("• Image blocks with embedded images"),
            paragraph("• Files blocks with attachments"),
            paragraph("• Tables with structured data"),
            paragraph("• Lists and blockquotes")
        ),
        
        paragraph(
            text("Last updated by "),
            mention_user(member_id) if member_id else text("System"),
            text(" on 2025-10-23", italic=True)
        )
    ])
    
    # Step 5: Update document
    try:
        client.replace_json_document(document_id, content)
        print("\n✅ Comprehensive document created successfully!")
        print(f"\n🔗 View document: https://vaiz.app/document/{document_id}")
        
        # Verify all blocks
        print("\nVerifying blocks...")
        doc_content = client.get_json_document(document_id)
        
        mention_count = 0
        image_block_count = 0
        files_block_count = 0
        table_count = 0
        
        for node in doc_content.get("default", {}).get("content", []):
            node_type = node.get("type")
            
            if node_type == "paragraph" and "content" in node:
                for child in node["content"]:
                    if child.get("type") == "custom-mention":
                        mention_count += 1
            elif node_type == "image-block":
                image_block_count += 1
            elif node_type == "files":
                files_block_count += 1
            elif node_type == "extension-table":
                table_count += 1
        
        print(f"✓ Found {mention_count} mention(s)")
        print(f"✓ Found {image_block_count} image block(s)")
        print(f"✓ Found {files_block_count} files block(s)")
        print(f"✓ Found {table_count} table(s)")
        
        total_blocks = mention_count + image_block_count + files_block_count + table_count
        print(f"\n📦 Total interactive blocks: {total_blocks}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n=== Example completed ===")


if __name__ == "__main__":
    main()

