#!/usr/bin/env python3
"""
Example: Creating Documents in Vaiz

This example demonstrates how to create new documents in different scopes:
- Space documents (shared across organization)
- Member documents (personal)
- Project documents (project-specific)
"""

import os
from datetime import datetime
from vaiz import VaizClient
from vaiz.models import CreateDocumentRequest, Kind


def main():
    # Initialize client
    api_key = os.getenv("VAIZ_API_KEY")
    space_id = os.getenv("VAIZ_SPACE_ID")
    
    if not api_key or not space_id:
        print("Error: Set VAIZ_API_KEY and VAIZ_SPACE_ID environment variables")
        return
    
    client = VaizClient(api_key=api_key, space_id=space_id, verbose=True)
    
    print("=== Creating Documents Examples ===\n")
    
    # Example 1: Create Space document
    print("1. Creating Space Document:")
    try:
        space_doc_response = client.create_document(
            CreateDocumentRequest(
                kind=Kind.Space,
                kind_id=space_id,
                title="Company Knowledge Base",
                index=0
            )
        )
        
        space_doc = space_doc_response.payload.document
        print("✅ Created Space document")
        print(f"   ID: {space_doc.id}")
        print(f"   Title: {space_doc.title}")
        print(f"   Kind: {space_doc.kind}")
        print(f"   Size: {space_doc.size} bytes (empty)")
    except Exception as e:
        print(f"Error: {e}")
    
    print()
    
    # Example 2: Create Member document
    print("2. Creating Member (Personal) Document:")
    try:
        # Get current user's member ID (use memberId, not _id)
        profile = client.get_profile()
        member_id = profile.profile.member_id
        
        member_doc_response = client.create_document(
            CreateDocumentRequest(
                kind=Kind.Member,
                kind_id=member_id,
                title="My Personal Notes",
                index=0
            )
        )
        
        member_doc = member_doc_response.payload.document
        print("✅ Created Member document")
        print(f"   ID: {member_doc.id}")
        print(f"   Title: {member_doc.title}")
        print(f"   Creator: {member_doc.creator}")
    except Exception as e:
        print(f"Error: {e}")
    
    print()
    
    # Example 3: Create Project document
    print("3. Creating Project Document:")
    try:
        # Get first project
        projects = client.get_projects()
        
        if projects.projects:
            project_id = projects.projects[0].id
            project_name = projects.projects[0].name
            
            project_doc_response = client.create_document(
                CreateDocumentRequest(
                    kind=Kind.Project,
                    kind_id=project_id,
                    title=f"{project_name} - Documentation",
                    index=0
                )
            )
            
            project_doc = project_doc_response.payload.document
            print("✅ Created Project document")
            print(f"   ID: {project_doc.id}")
            print(f"   Title: {project_doc.title}")
            print(f"   Project: {project_name}")
            print(f"   Kind ID: {project_doc.kind_id}")
        else:
            print("No projects available")
    except Exception as e:
        print(f"Error: {e}")
    
    print()
    
    # Example 4: Create and populate document
    print("4. Create and Populate Document:")
    try:
        projects = client.get_projects()
        
        if projects.projects:
            project_id = projects.projects[0].id
            
            # Create document
            response = client.create_document(
                CreateDocumentRequest(
                    kind=Kind.Project,
                    kind_id=project_id,
                    title="Sprint Planning",
                    index=0
                )
            )
            
            doc = response.payload.document
            print(f"✅ Created document: {doc.id}")
            
            # Populate with content
            content = f"""
# Sprint Planning

**Date**: {datetime.now().strftime("%Y-%m-%d")}
**Sprint**: Week {datetime.now().isocalendar()[1]}

## Goals
- Complete feature implementation
- Fix critical bugs
- Update documentation

## Team Capacity
- Available developers: 5
- Sprint duration: 2 weeks

## Planned Stories
1. User authentication improvements
2. API optimization
3. UI/UX enhancements

## Notes
This document was created and populated automatically via SDK.
"""
            
            client.replace_document(doc.id, content)
            print("✅ Document populated with content")
            
            # Verify
            retrieved = client.get_document_body(doc.id)
            print(f"✅ Content verified (keys: {list(retrieved.keys())})")
        else:
            print("No projects available")
    except Exception as e:
        print(f"Error: {e}")
    
    print()
    
    # Example 5: Create multiple documents
    print("5. Creating Multiple Documents:")
    try:
        projects = client.get_projects()
        
        if projects.projects:
            project_id = projects.projects[0].id
            
            document_titles = [
                "Requirements Document",
                "Technical Specification",
                "Test Plan",
                "Deployment Guide"
            ]
            
            created_docs = []
            for idx, title in enumerate(document_titles):
                response = client.create_document(
                    CreateDocumentRequest(
                        kind=Kind.Project,
                        kind_id=project_id,
                        title=title,
                        index=idx
                    )
                )
                created_docs.append(response.payload.document)
                print(f"   ✅ Created: {title}")
            
            print(f"\n   Total created: {len(created_docs)} documents")
        else:
            print("No projects available")
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n=== Examples Complete ===")


if __name__ == "__main__":
    main()

