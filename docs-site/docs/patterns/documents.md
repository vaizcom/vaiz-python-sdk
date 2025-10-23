---
sidebar_position: 4
title: Document Patterns — Management & Hierarchies | Vaiz Python SDK
description: Learn patterns for document management and hierarchies in the Vaiz Python SDK. Includes mentions, nested content, and document organization strategies.
---

# Working with Documents

Patterns for document management and hierarchies.

## Getting the Right Member ID

For Member (personal) documents, use `member_id` from profile, not user `id`:

```python
# ✅ Correct way
profile = client.get_profile()
member_id = profile.profile.member_id  # Use this!

# Get personal documents
from vaiz.models import GetDocumentsRequest, Kind

docs = client.get_documents(
    GetDocumentsRequest(
        kind=Kind.Member,
        kind_id=member_id  # Use member_id
    )
)

# ❌ Wrong way
user_id = profile.profile.id  # This won't work for Member documents!
```

## Creating Document Hierarchies

Organize documents in nested structures:

```python
from vaiz.models import CreateDocumentRequest, Kind

# 1. Create parent
parent = client.create_document(
    CreateDocumentRequest(
        kind=Kind.Project,
        kind_id=project_id,
        title="Documentation",
        index=0
    )
).payload.document

# 2. Create children
for idx, title in enumerate(["Getting Started", "API Ref", "Examples"]):
    child = client.create_document(
        CreateDocumentRequest(
            kind=Kind.Project,
            kind_id=project_id,
            title=title,
            index=idx,
            parent_document_id=parent.id  # Link to parent
        )
    ).payload.document
    
    print(f"Created: {child.title}")
```

## Project Knowledge Base Builder

Create a structured knowledge base for a project:

```python
from vaiz.models import CreateDocumentRequest, Kind

def create_project_wiki(client, project_id: str):
    """Create a structured knowledge base for a project."""
    
    # Create wiki root
    wiki = client.create_document(
        CreateDocumentRequest(
            kind=Kind.Project,
            kind_id=project_id,
            title="Project Wiki",
            index=0
        )
    ).payload.document
    
    # Define wiki structure
    sections = {
        "Getting Started": ["Setup", "Configuration", "First Steps"],
        "Development": ["Coding Standards", "Git Workflow", "Testing"],
        "Deployment": ["Environments", "CI/CD", "Monitoring"],
        "Team": ["Contacts", "Roles", "Meetings"]
    }
    
    # Create sections and pages
    for section_idx, (section_name, pages) in enumerate(sections.items()):
        # Create section
        section = client.create_document(
            CreateDocumentRequest(
                kind=Kind.Project,
                kind_id=project_id,
                title=section_name,
                index=section_idx,
                parent_document_id=wiki.id
            )
        ).payload.document
        
        # Create pages
        for page_idx, page_name in enumerate(pages):
            page = client.create_document(
                CreateDocumentRequest(
                    kind=Kind.Project,
                    kind_id=project_id,
                    title=page_name,
                    index=page_idx,
                    parent_document_id=section.id
                )
            ).payload.document
            
            # Add initial content
            content = f"# {page_name}\n\n[Add content here]"
            client.replace_document(page.id, content)
    
    return wiki

# Usage
wiki = create_project_wiki(client, project_id)
print(f"✅ Created wiki: {wiki.id}")
```

## See Also

- [Documents Guide](../guides/documents) - Document API usage
- [Documents API Reference](../api-reference/documents) - Complete API documentation

