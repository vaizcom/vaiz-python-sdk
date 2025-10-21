#!/usr/bin/env python3
"""
Example: Working with Document Content in Vaiz

This example demonstrates how to:
1. Get a list of documents (Space/Member/Project)
2. Read document content using get_document_body()
3. Update document content using replace_document()
"""

import os
from datetime import datetime
from vaiz import VaizClient
from vaiz.models import GetDocumentsRequest, Kind


def main():
    # Initialize client
    api_key = os.getenv("VAIZ_API_KEY")
    space_id = os.getenv("VAIZ_SPACE_ID")
    
    if not api_key or not space_id:
        print("Error: Set VAIZ_API_KEY and VAIZ_SPACE_ID environment variables")
        return
    
    client = VaizClient(api_key=api_key, space_id=space_id, verbose=True)
    
    print("=== Document Content Management Examples ===\n")
    
    # Example 1: Working with Space documents
    print("1. Working with Space Documents:")
    try:
        # Get list of Space documents
        space_docs = client.get_documents(
            GetDocumentsRequest(
                kind=Kind.Space,
                kind_id=space_id  # Use space_id for Space documents
            )
        )
        
        if space_docs.payload.documents:
            doc = space_docs.payload.documents[0]
            print(f"   Found document: {doc.title}")
            print(f"   Document ID: {doc.id}")
            
            # Get current content
            content = client.get_document_body(doc.id)
            print(f"   Current content keys: {list(content.keys())}")
            
            # Update content
            new_content = f"""
# Space Document Update

Updated at: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

This is a shared document accessible to all space members.

## Recent Changes
- Content updated via SDK
- Automatic timestamp added
"""
            
            client.replace_document(doc.id, new_content)
            print("   ✅ Document content updated")
        else:
            print("   No Space documents found")
    except Exception as e:
        print(f"   Error: {e}")
    
    print()
    
    # Example 2: Working with Member documents
    print("2. Working with Member (Personal) Documents:")
    try:
        # Get profile to get member ID
        profile = client.get_profile()
        member_id = profile.profile.id
        
        # Get list of Member documents
        member_docs = client.get_documents(
            GetDocumentsRequest(
                kind=Kind.Member,
                kind_id=member_id
            )
        )
        
        if member_docs.payload.documents:
            doc = member_docs.payload.documents[0]
            print(f"   Found personal document: {doc.title}")
            print(f"   Document ID: {doc.id}")
            
            # Get current content
            content = client.get_document_body(doc.id)
            print(f"   Current size: {doc.size} bytes")
            
            # Update content with personal notes
            new_content = f"""
# Personal Notes

Last updated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## My Tasks
- Review project documentation
- Update SDK examples
- Test new features

## Notes
This is a private document visible only to me.
"""
            
            client.replace_document(doc.id, new_content)
            print("   ✅ Personal document updated")
        else:
            print("   No Member documents found")
    except Exception as e:
        print(f"   Error: {e}")
    
    print()
    
    # Example 3: Working with Project documents
    print("3. Working with Project Documents:")
    try:
        # Get list of projects to find a project ID
        projects = client.get_projects()
        
        if projects.projects:
            project_id = projects.projects[0].id
            print(f"   Using project: {projects.projects[0].name}")
            
            # Get project documents
            project_docs = client.get_documents(
                GetDocumentsRequest(
                    kind=Kind.Project,
                    kind_id=project_id
                )
            )
            
            if project_docs.payload.documents:
                doc = project_docs.payload.documents[0]
                print(f"   Found document: {doc.title}")
                print(f"   Document ID: {doc.id}")
                print(f"   Contributors: {len(doc.contributor_ids)}")
                
                # Get current content
                content = client.get_document_body(doc.id)
                print(f"   Retrieved content")
                
                # Update with project status
                new_content = f"""
# Project Document

Last updated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Project Status
- Document accessible to project members
- Updated via SDK automation

## Team Information
- Contributors: {len(doc.contributor_ids)}
- Created: {doc.created_at.strftime("%Y-%m-%d")}
"""
                
                client.replace_document(doc.id, new_content)
                print("   ✅ Project document updated")
            else:
                print("   No Project documents found")
        else:
            print("   No projects available")
    except Exception as e:
        print(f"   Error: {e}")
    
    print()
    
    # Example 4: Bulk document update
    print("4. Bulk Document Update Example:")
    try:
        project_docs = client.get_documents(
            GetDocumentsRequest(
                kind=Kind.Project,
                kind_id=project_id if 'project_id' in locals() else space_id
            )
        )
        
        updated_count = 0
        for doc in project_docs.payload.documents[:3]:  # Update first 3 documents
            try:
                # Add timestamp footer to each document
                content = client.get_document_body(doc.id)
                
                new_content = f"""
Document: {doc.title}

---
Last batch update: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Document ID: {doc.id}
"""
                
                client.replace_document(doc.id, new_content)
                updated_count += 1
                print(f"   ✅ Updated: {doc.title}")
            except Exception as e:
                print(f"   ❌ Failed to update {doc.title}: {e}")
        
        print(f"   Total updated: {updated_count} documents")
    except Exception as e:
        print(f"   Error: {e}")
    
    print()
    
    # Example 5: Template-based document creation
    print("5. Template-Based Content Update:")
    try:
        template = """
# Meeting Notes Template

**Date**: {date}
**Time**: {time}

## Attendees
- [Add attendees here]

## Agenda
1. Item 1
2. Item 2
3. Item 3

## Discussion
[Add discussion notes]

## Action Items
- [ ] Action item 1
- [ ] Action item 2

## Next Meeting
[Schedule next meeting]
"""
        
        # Apply template to a document
        if 'project_docs' in locals() and project_docs.payload.documents:
            doc = project_docs.payload.documents[0]
            
            formatted_content = template.format(
                date=datetime.now().strftime("%Y-%m-%d"),
                time=datetime.now().strftime("%H:%M")
            )
            
            client.replace_document(doc.id, formatted_content)
            print(f"   ✅ Applied template to: {doc.title}")
            print(f"   Document ID: {doc.id}")
        else:
            print("   No documents available for template")
    except Exception as e:
        print(f"   Error: {e}")
    
    print("\n=== Examples Complete ===")


if __name__ == "__main__":
    main()

