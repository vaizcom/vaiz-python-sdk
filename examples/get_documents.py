#!/usr/bin/env python3
"""
Example of getting documents list from Vaiz.

This example demonstrates how to get documents list from different scopes:
- Space - shared space documents
- Member - personal member documents
- Project - project documents
"""

import os
from vaiz import VaizClient
from vaiz.models import GetDocumentsRequest, Kind


def main():
    # Initialize client
    # Get API key and space ID from environment variables
    api_key = os.getenv("VAIZ_API_KEY")
    space_id = os.getenv("VAIZ_SPACE_ID")
    
    if not api_key or not space_id:
        print("Error: Set environment variables VAIZ_API_KEY and VAIZ_SPACE_ID")
        return
    
    client = VaizClient(api_key=api_key, space_id=space_id, verbose=True)
    
    print("=== Getting documents list ===\n")
    
    # Example 1: Getting space documents
    print("1. Getting space documents (Space):")
    try:
        space_request = GetDocumentsRequest(
            kind=Kind.Space,
            kind_id="68f7519ba65f977ddb66db8c"  # Replace with actual space ID
        )
        space_documents = client.get_documents(space_request)
        
        print(f"Found documents: {len(space_documents.payload.documents)}")
        for doc in space_documents.payload.documents:
            print(f"  - {doc.title} (ID: {doc.id}, size: {doc.size} bytes)")
            print(f"    Creator: {doc.creator}, created: {doc.created_at}")
            print(f"    Type: {doc.kind}, Type ID: {doc.kind_id}")
            print()
    except Exception as e:
        print(f"Error getting space documents: {e}")
    
    # Example 2: Getting member documents
    print("2. Getting member documents (Member):")
    try:
        member_request = GetDocumentsRequest(
            kind=Kind.Member,
            kind_id="68f7519ca65f977ddb66db8e"  # Replace with actual member ID
        )
        member_documents = client.get_documents(member_request)
        
        print(f"Found documents: {len(member_documents.payload.documents)}")
        for doc in member_documents.payload.documents:
            print(f"  - {doc.title} (ID: {doc.id}, size: {doc.size} bytes)")
            print(f"    Creator: {doc.creator}, created: {doc.created_at}")
            print(f"    Contributors: {doc.contributor_ids}")
            print()
    except Exception as e:
        print(f"Error getting member documents: {e}")
    
    # Example 3: Getting project documents
    print("3. Getting project documents (Project):")
    try:
        project_request = GetDocumentsRequest(
            kind=Kind.Project,
            kind_id="68f756ddd9d111649a74ee88"  # Replace with actual project ID
        )
        project_documents = client.get_documents(project_request)
        
        print(f"Found documents: {len(project_documents.payload.documents)}")
        for doc in project_documents.payload.documents:
            print(f"  - {doc.title} (ID: {doc.id}, size: {doc.size} bytes)")
            print(f"    Creator: {doc.creator}, created: {doc.created_at}")
            print(f"    Archived: {'Yes' if doc.archived_at else 'No'}")
            print(f"    Followers: {list(doc.followers.keys())}")
            print()
    except Exception as e:
        print(f"Error getting project documents: {e}")
    
    print("=== Example completed ===")


if __name__ == "__main__":
    main()
