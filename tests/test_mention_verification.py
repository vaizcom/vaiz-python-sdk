"""
Test to verify mention blocks structure after creation.
"""

import pytest
from vaiz.helpers import mention_user, mention_document, mention_task, mention_milestone, paragraph, text, heading
from vaiz.models import CreateDocumentRequest, Kind, GetDocumentsRequest, GetTasksRequest
from tests.test_config import get_test_client, TEST_SPACE_ID
import json


def test_verify_mention_structure_after_creation():
    """Verify that mentions are correctly saved and retrieved from API."""
    client = get_test_client()
    
    # Get real IDs (member_id for user mentions)
    profile = client.get_profile()
    member_id = profile.profile.member_id
    
    docs_response = client.get_documents(
        GetDocumentsRequest(kind=Kind.Space, kind_id=TEST_SPACE_ID)
    )
    doc_id = docs_response.payload.documents[0].id if docs_response.payload.documents else None
    
    tasks_response = client.get_tasks(GetTasksRequest())
    task_id = tasks_response.payload.tasks[0].id if tasks_response.payload.tasks else None
    
    milestones_response = client.get_milestones()
    milestone_id = milestones_response.milestones[0].id if milestones_response.milestones else None
    
    # Create document
    create_request = CreateDocumentRequest(
        kind=Kind.Space,
        kind_id=TEST_SPACE_ID,
        title="Test: Mention Structure Verification",
        index=0
    )
    
    doc_response = client.create_document(create_request)
    test_doc_id = doc_response.payload.document.id
    
    print(f"\n📄 Created test document: {test_doc_id}")
    print(f"🔗 View at: https://vaiz.app/document/{test_doc_id}")
    
    try:
        # Create mentions with known structure
        sent_mentions = []
        
        # User mention
        user_mention = mention_user(member_id)
        sent_mentions.append(("User", member_id, user_mention))
        
        content = [
            heading(1, "Mention Structure Test"),
            paragraph(text("User: "), user_mention)
        ]
        
        # Add other mentions if available
        if doc_id:
            doc_mention = mention_document(doc_id)
            sent_mentions.append(("Document", doc_id, doc_mention))
            content.append(paragraph(text("Document: "), doc_mention))
        
        if task_id:
            task_mention = mention_task(task_id)
            sent_mentions.append(("Task", task_id, task_mention))
            content.append(paragraph(text("Task: "), task_mention))
        
        if milestone_id:
            milestone_mention = mention_milestone(milestone_id)
            sent_mentions.append(("Milestone", milestone_id, milestone_mention))
            content.append(paragraph(text("Milestone: "), milestone_mention))
        
        print(f"\n📤 Sending {len(sent_mentions)} mention(s) to API...")
        
        # Print what we're sending
        for kind, entity_id, mention_data in sent_mentions:
            print(f"\n  {kind} mention:")
            print(f"    Entity ID: {entity_id}")
            print(f"    Sent structure: {json.dumps(mention_data, indent=6)}")
        
        # Send to API
        client.replace_json_document(test_doc_id, content)
        
        # Retrieve and verify
        print(f"\n📥 Retrieving document from API...")
        doc_content = client.get_json_document(test_doc_id)
        
        print(f"\n📋 Retrieved document structure:")
        print(json.dumps(doc_content, indent=2))
        
        # Lexical format: mentions persist as serialized markers
        # with __userId / __entityId and __entityKind fields
        doc_str = json.dumps(doc_content)
        received_count = doc_str.count("-mention")

        print(f"\n✅ Found {received_count} mention(s) in response")

        # Assertions
        assert received_count == len(sent_mentions), \
            f"Expected {len(sent_mentions)} mentions, got {received_count}"

        # Verify each sent mention's entity ID survived the round-trip
        for kind, entity_id, _ in sent_mentions:
            assert entity_id in doc_str, f"{kind} mention with ID {entity_id} not found in document"

        print(f"\n📊 Summary:")
        print(f"  ✅ Sent: {len(sent_mentions)} mentions")
        print(f"  ✅ Received: {received_count} mentions")
        print(f"\n🔗 Verify visually in browser: https://vaiz.app/document/{test_doc_id}")
        print(f"   Mentions should display with avatars/icons and be clickable")
        
    finally:
        pass  # Could add cleanup here


if __name__ == "__main__":
    test_verify_mention_structure_after_creation()

