#!/usr/bin/env python3
"""
Example: Document Hierarchy in Vaiz

This example demonstrates how to create and manage nested documents:
1. Creating parent documents
2. Creating child documents
3. Building multi-level hierarchies
4. Managing document structure
"""

import os
from datetime import datetime
from vaiz import VaizClient
from vaiz.models import CreateDocumentRequest, GetDocumentsRequest, Kind


def main():
    # Initialize client
    api_key = os.getenv("VAIZ_API_KEY")
    space_id = os.getenv("VAIZ_SPACE_ID")
    
    if not api_key or not space_id:
        print("Error: Set VAIZ_API_KEY and VAIZ_SPACE_ID environment variables")
        return
    
    client = VaizClient(api_key=api_key, space_id=space_id)
    
    print("=== Document Hierarchy Examples ===\n")
    
    # Get project for examples
    projects = client.get_projects()
    
    if not projects.projects:
        print("No projects available for hierarchy examples")
        return
    
    project_id = projects.projects[0].id
    project_name = projects.projects[0].name
    print(f"Using project: {project_name} (ID: {project_id})\n")
    
    # Example 1: Simple parent-child structure
    print("1. Creating Parent-Child Structure:")
    try:
        # Create parent
        parent_response = client.create_document(
            CreateDocumentRequest(
                kind=Kind.Project,
                kind_id=project_id,
                title="Product Documentation",
                index=0
            )
        )
        
        parent_doc = parent_response.payload.document
        print(f"✅ Parent: {parent_doc.title}")
        print(f"   ID: {parent_doc.id}")
        
        # Create children
        child_sections = ["Getting Started", "API Reference", "Examples"]
        
        for idx, section in enumerate(child_sections):
            child_response = client.create_document(
                CreateDocumentRequest(
                    kind=Kind.Project,
                    kind_id=project_id,
                    title=section,
                    index=idx,
                    parent_document_id=parent_doc.id
                )
            )
            
            child_doc = child_response.payload.document
            print(f"  ✅ Child {idx + 1}: {child_doc.title} (ID: {child_doc.id})")
        
        print(f"\nCreated 1 parent with {len(child_sections)} children")
    except Exception as e:
        print(f"Error: {e}")
    
    print()
    
    # Example 2: Multi-level hierarchy (Book structure)
    print("2. Creating Multi-Level Hierarchy (Book):")
    try:
        # Root document
        book_response = client.create_document(
            CreateDocumentRequest(
                kind=Kind.Project,
                kind_id=project_id,
                title="User Manual",
                index=0
            )
        )
        
        book_doc = book_response.payload.document
        print(f"📚 Book: {book_doc.title}")
        
        # Chapters
        chapters = [
            ("Chapter 1: Introduction", ["1.1 Overview", "1.2 Installation", "1.3 Quick Start"]),
            ("Chapter 2: Features", ["2.1 Core Features", "2.2 Advanced Features"]),
            ("Chapter 3: Configuration", ["3.1 Basic Setup", "3.2 Advanced Settings", "3.3 Troubleshooting"])
        ]
        
        for chapter_idx, (chapter_title, sections) in enumerate(chapters):
            # Create chapter
            chapter_response = client.create_document(
                CreateDocumentRequest(
                    kind=Kind.Project,
                    kind_id=project_id,
                    title=chapter_title,
                    index=chapter_idx,
                    parent_document_id=book_doc.id
                )
            )
            
            chapter_doc = chapter_response.payload.document
            print(f"  📖 {chapter_doc.title}")
            
            # Create sections
            for section_idx, section_title in enumerate(sections):
                section_response = client.create_document(
                    CreateDocumentRequest(
                        kind=Kind.Project,
                        kind_id=project_id,
                        title=section_title,
                        index=section_idx,
                        parent_document_id=chapter_doc.id
                    )
                )
                
                section_doc = section_response.payload.document
                print(f"    📄 {section_doc.title}")
        
        print(f"\n✅ Created hierarchical book structure with 3 chapters")
    except Exception as e:
        print(f"Error: {e}")
    
    print()
    
    # Example 3: Project wiki structure
    print("3. Creating Project Wiki Structure:")
    try:
        # Wiki root
        wiki_response = client.create_document(
            CreateDocumentRequest(
                kind=Kind.Project,
                kind_id=project_id,
                title="Project Wiki",
                index=0
            )
        )
        
        wiki_doc = wiki_response.payload.document
        print(f"📝 Wiki: {wiki_doc.title}")
        
        # Wiki sections
        wiki_structure = {
            "Architecture": ["System Design", "Database Schema", "API Design"],
            "Development": ["Coding Standards", "Git Workflow", "Testing Strategy"],
            "Deployment": ["Environment Setup", "CI/CD Pipeline", "Monitoring"]
        }
        
        for section_idx, (section_name, pages) in enumerate(wiki_structure.items()):
            # Create section
            section_response = client.create_document(
                CreateDocumentRequest(
                    kind=Kind.Project,
                    kind_id=project_id,
                    title=section_name,
                    index=section_idx,
                    parent_document_id=wiki_doc.id
                )
            )
            
            section_doc = section_response.payload.document
            print(f"  📁 {section_doc.title}")
            
            # Create pages
            for page_idx, page_title in enumerate(pages):
                page_response = client.create_document(
                    CreateDocumentRequest(
                        kind=Kind.Project,
                        kind_id=project_id,
                        title=page_title,
                        index=page_idx,
                        parent_document_id=section_doc.id
                    )
                )
                print(f"    📃 {page_title}")
        
        print(f"\n✅ Created wiki with {len(wiki_structure)} sections")
    except Exception as e:
        print(f"Error: {e}")
    
    print()
    
    # Example 4: Populating hierarchical documents with content
    print("4. Populating Hierarchical Documents:")
    try:
        # Get some documents from project
        docs = client.get_documents(
            GetDocumentsRequest(kind=Kind.Project, kind_id=project_id)
        )
        
        if len(docs.payload.documents) >= 3:
            # Update first 3 documents with structured content
            for idx, doc in enumerate(docs.payload.documents[:3]):
                content = f"""
# {doc.title}

**Last Updated**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Overview
This is document {idx + 1} in the hierarchy.

Document ID: {doc.id}
Kind: {doc.kind}
"""
                
                client.replace_document(doc.id, content)
                print(f"  ✅ Updated: {doc.title}")
            
            print(f"\n✅ Populated {min(3, len(docs.payload.documents))} documents with content")
        else:
            print("Not enough documents to populate")
    except Exception as e:
        print(f"Error: {e}")
    
    print()
    
    # Example 5: Display document structure
    print("5. Viewing Document Structure:")
    try:
        docs = client.get_documents(
            GetDocumentsRequest(kind=Kind.Project, kind_id=project_id)
        )
        
        print(f"Total documents in project: {len(docs.payload.documents)}")
        print("\nDocument List:")
        for idx, doc in enumerate(docs.payload.documents[:10], 1):
            archived = " [ARCHIVED]" if doc.archived_at else ""
            print(f"  {idx}. {doc.title}{archived}")
            print(f"     ID: {doc.id}, Size: {doc.size} bytes")
        
        if len(docs.payload.documents) > 10:
            print(f"  ... and {len(docs.payload.documents) - 10} more documents")
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n=== Hierarchy Examples Complete ===")


if __name__ == "__main__":
    main()

