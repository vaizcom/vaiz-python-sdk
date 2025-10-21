#!/usr/bin/env python3
"""
Example: Advanced Document Workflows in Vaiz

This example demonstrates advanced scenarios:
1. Working with specific documents by ID
2. Batch operations across multiple scopes
3. Document content migration and updates
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
    
    client = VaizClient(api_key=api_key, space_id=space_id)
    
    print("=== Advanced Document Workflows ===\n")
    
    # Example 1: Update specific document by ID
    print("1. Update Specific Document by ID:")
    print("   Note: When you know the document ID, work with it directly.")
    print("   Avoid loading all documents to search by title - this doesn't scale.")
    try:
        # Get a few documents to demonstrate
        docs = client.get_documents(
            GetDocumentsRequest(kind=Kind.Space, kind_id=space_id)
        )
        
        if docs.payload.documents:
            # Work with first document as example
            target_doc = docs.payload.documents[0]
            print(f"   Working with: {target_doc.title}")
            print(f"   ID: {target_doc.id}")
            
            # Update content with timestamp
            new_content = f"""
# Document Content - Updated

Last updated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Latest Updates
- Content updated via SDK
- Timestamp added automatically
- Document ID: {target_doc.id}
"""
            
            client.replace_document(target_doc.id, new_content)
            print("   ✅ Document updated")
        else:
            print("   No documents found")
    except Exception as e:
        print(f"   Error: {e}")
    
    print()
    
    # Example 2: Document content audit across scopes
    print("2. Document Content Audit:")
    try:
        profile = client.get_profile()
        member_id = profile.profile.member_id  # Use memberId for Member documents
        
        scopes = [
            (Kind.Space, space_id, "Space"),
            (Kind.Member, member_id, "Member"),
        ]
        
        total_docs = 0
        total_size = 0
        
        for kind, kind_id, scope_name in scopes:
            docs = client.get_documents(
                GetDocumentsRequest(kind=kind, kind_id=kind_id)
            )
            
            scope_size = sum(doc.size for doc in docs.payload.documents)
            total_docs += len(docs.payload.documents)
            total_size += scope_size
            
            print(f"   {scope_name}:")
            print(f"   - Documents: {len(docs.payload.documents)}")
            print(f"   - Total size: {scope_size:,} bytes")
        
        print("\n   Total across scopes:")
        print(f"   - Documents: {total_docs}")
        print(f"   - Total size: {total_size:,} bytes")
    except Exception as e:
        print(f"   Error: {e}")
    
    print()
    
    # Example 3: Batch content standardization
    print("3. Batch Content Standardization:")
    try:
        # Get project documents
        projects = client.get_projects()
        
        if projects.projects:
            project_id = projects.projects[0].id
            docs = client.get_documents(
                GetDocumentsRequest(kind=Kind.Project, kind_id=project_id)
            )
            
            standard_header = f"""
# Project Documentation

**Project**: {projects.projects[0].name}
**Last Updated**: {datetime.now().strftime("%Y-%m-%d")}

---

"""
            
            updated = 0
            for doc in docs.payload.documents[:5]:  # Limit to 5 docs
                try:
                    # Get current content
                    content = client.get_document_body(doc.id)
                    
                    # Add standard header
                    standardized = standard_header + f"Document: {doc.title}\n\n[Content]"
                    
                    client.replace_document(doc.id, standardized)
                    updated += 1
                    print(f"   ✅ Standardized: {doc.title}")
                except Exception as e:
                    print(f"   ❌ Failed: {doc.title} - {e}")
            
            print(f"\n   Total standardized: {updated} documents")
        else:
            print("   No projects available")
    except Exception as e:
        print(f"   Error: {e}")
    
    print()
    
    # Example 4: Document backup
    print("4. Document Content Backup:")
    try:
        backup_data = []
        
        docs = client.get_documents(
            GetDocumentsRequest(kind=Kind.Space, kind_id=space_id)
        )
        
        for doc in docs.payload.documents[:3]:  # Backup first 3
            content = client.get_document_body(doc.id)
            
            backup_data.append({
                'id': doc.id,
                'title': doc.title,
                'size': doc.size,
                'created_at': doc.created_at.isoformat(),
                'content': content,
                'backup_timestamp': datetime.now().isoformat()
            })
            
            print(f"   ✅ Backed up: {doc.title}")
        
        print(f"\n   Total backed up: {len(backup_data)} documents")
        print("   Backup can be saved to file or database")
    except Exception as e:
        print(f"   Error: {e}")
    
    print()
    
    # Example 5: Content migration between documents
    print("5. Content Migration Example:")
    try:
        source_docs = client.get_documents(
            GetDocumentsRequest(kind=Kind.Space, kind_id=space_id)
        )
        
        if len(source_docs.payload.documents) >= 2:
            source_doc = source_docs.payload.documents[0]
            target_doc = source_docs.payload.documents[1]
            
            print(f"   Source: {source_doc.title}")
            print(f"   Target: {target_doc.title}")
            
            # Create migration note (in real scenario, you'd use source content)
            migration_content = f"""
# Migrated Content

Original document: {source_doc.title}
Migration date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

---

[Migrated content would go here]

---

Source document ID: {source_doc.id}
"""
            
            # Update target with migrated content
            client.replace_document(target_doc.id, migration_content)
            print("   ✅ Content migrated successfully")
        else:
            print("   Not enough documents for migration example")
    except Exception as e:
        print(f"   Error: {e}")
    
    print()
    
    # Example 6: Smart content updates
    print("6. Smart Content Updates (Conditional):")
    try:
        docs = client.get_documents(
            GetDocumentsRequest(kind=Kind.Space, kind_id=space_id)
        )
        
        # Only update documents that haven't been updated recently
        from datetime import timedelta
        cutoff_date = datetime.now() - timedelta(days=7)
        
        updated = 0
        skipped = 0
        
        for doc in docs.payload.documents[:5]:
            if doc.updated_at < cutoff_date:
                new_content = f"""
Document: {doc.title}

This document was automatically updated because it was last modified on {doc.updated_at.strftime("%Y-%m-%d")}.

Updated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""
                
                client.replace_document(doc.id, new_content)
                updated += 1
                print(f"   ✅ Updated (old): {doc.title}")
            else:
                skipped += 1
                print(f"   ⏭️  Skipped (recent): {doc.title}")
        
        print(f"\n   Updated: {updated}, Skipped: {skipped}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print("\n=== Advanced Workflows Complete ===")


if __name__ == "__main__":
    main()

