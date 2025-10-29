"""
Edit Document Example

This example demonstrates how to edit a document's title using the editDocument API.
It shows the complete workflow:
1. Creating a new document
2. Editing the document title
3. Verifying the change
"""

from datetime import datetime
from vaiz import VaizClient, CreateDocumentRequest, EditDocumentRequest, GetDocumentsRequest, Kind
from config import API_KEY, SPACE_ID


def main():
    # Initialize client
    client = VaizClient(api_key=API_KEY, space_id=SPACE_ID, verify_ssl=False)
    
    print("=== Edit Document Example ===\n")
    
    # 1. Create a new document
    print("1. Creating a new document...")
    original_title = f"Test Document - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    
    create_request = CreateDocumentRequest(
        kind=Kind.Space,
        kind_id=SPACE_ID,
        title=original_title,
        index=0
    )
    
    create_response = client.create_document(create_request)
    document = create_response.payload.document
    
    print(f"✅ Created document:")
    print(f"   ID: {document.id}")
    print(f"   Title: {document.title}")
    print(f"   Kind: {document.kind}")
    print(f"   Size: {document.size} bytes\n")
    
    # 2. Edit document title
    print("2. Editing document title...")
    new_title = f"Updated Document - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    
    edit_request = EditDocumentRequest(
        document_id=document.id,
        title=new_title
    )
    
    edit_response = client.edit_document(edit_request)
    edited_document = edit_response.payload.document
    
    print(f"✅ Edited document:")
    print(f"   ID: {edited_document.id}")
    print(f"   Old Title: {original_title}")
    print(f"   New Title: {edited_document.title}")
    print(f"   Updated At: {edited_document.updated_at}\n")
    
    # 3. Verify the change
    print("3. Verifying title change in document list...")
    list_request = GetDocumentsRequest(
        kind=Kind.Space,
        kind_id=SPACE_ID
    )
    
    list_response = client.get_documents(list_request)
    
    # Find our document in the list
    found_document = None
    for doc in list_response.payload.documents:
        if doc.id == document.id:
            found_document = doc
            break
    
    if found_document:
        print(f"✅ Document found in list:")
        print(f"   ID: {found_document.id}")
        print(f"   Title: {found_document.title}")
        print(f"   Title matches: {found_document.title == new_title}")
    else:
        print("❌ Document not found in list")
    
    print("\n=== Example completed successfully! ===")


if __name__ == "__main__":
    main()

