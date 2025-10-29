---
sidebar_position: 9
sidebar_label: Documents
title: Documents API — Create & Edit Rich Documents | Vaiz Python SDK
description: Learn how to use the Vaiz Python SDK to create, edit, and manage rich-text documents with structured content. Includes JSON format, blocks, and formatting.
---

# Documents

Complete reference for document-related methods and models.

## Methods

### `create_document`

```python
create_document(request: CreateDocumentRequest) -> CreateDocumentResponse
```

Create a new document in specified scope (Space/Member/Project).

**Parameters:**
- `request` - CreateDocumentRequest with kind, kind_id, title, index, and optional parent_document_id

**Returns:** `CreateDocumentResponse` with created document

**Example:**
```python
from vaiz.models import CreateDocumentRequest, Kind

response = client.create_document(
    CreateDocumentRequest(
        kind=Kind.Project,
        kind_id="project_id",
        title="Project Plan",
        index=0
    )
)

document = response.payload.document
print(f"Created: {document.id}")
```

---

### `edit_document`

```python
edit_document(request: EditDocumentRequest) -> EditDocumentResponse
```

Edit document metadata such as title.

**Parameters:**
- `request` - EditDocumentRequest with document_id and title

**Returns:** `EditDocumentResponse` with updated document

**Example:**
```python
from vaiz.models import EditDocumentRequest

response = client.edit_document(
    EditDocumentRequest(
        document_id="doc_id",
        title="Updated Title"
    )
)

edited_doc = response.payload.document
print(f"Updated: {edited_doc.title}")
```

---

### `get_documents`

```python
get_documents(request: GetDocumentsRequest) -> GetDocumentsResponse
```

Get list of documents filtered by scope (Space/Member/Project) and scope ID.

**Parameters:**
- `request` - GetDocumentsRequest with kind and kind_id

**Returns:** `GetDocumentsResponse` with list of documents

**Example:**
```python
from vaiz.models import GetDocumentsRequest, Kind

docs = client.get_documents(
    GetDocumentsRequest(
        kind=Kind.Project,
        kind_id="project_id"
    )
)
```

---

## Models

### Document

Main document model representing a document in the system.

```python
class Document:
    id: str                             # Document ID
    title: str                          # Document title
    size: int                           # Document size in bytes
    contributor_ids: List[str]          # List of contributor IDs
    archiver: Optional[str]             # User who archived (if archived)
    followers: Dict[str, str]           # Document followers
    archived_at: Optional[datetime]     # Archive timestamp
    kind_id: str                        # ID of document
    kind: Kind                          # Document scope (Space/Member/Project)
    creator: str                        # Creator user ID
    map: List[Any]                      # Document structure map
    created_at: datetime                # Creation timestamp
    updated_at: datetime                # Last update timestamp
    bucket: str                         # Storage bucket ID
```

---

### EditDocument

Model representing an edited document (without internal fields like map).

```python
class EditDocument:
    id: str                             # Document ID
    title: str                          # Document title
    space: str                          # Space ID
    size: int                           # Document size in bytes
    contributor_ids: List[str]          # List of contributor IDs
    archiver: Optional[str]             # User who archived (if archived)
    followers: Dict[str, str]           # Document followers
    archived_at: Optional[datetime]     # Archive timestamp
    kind_id: str                        # ID of document scope
    kind: Kind                          # Document scope (Space/Member/Project)
    creator: str                        # Creator user ID
    created_at: datetime                # Creation timestamp
    updated_at: datetime                # Last update timestamp
    bucket: str                         # Storage bucket ID
    content: Optional[str]              # Document content (encoded)
    content_updated_at: Optional[datetime]  # Content update timestamp
```

---

## Request Models

### CreateDocumentRequest

```python
class CreateDocumentRequest:
    kind: Kind                          # Required - Document scope (Space/Member/Project)
    kind_id: str                        # Required - ID of space/member/project
    title: str                          # Required - Document title
    index: int                          # Required - Position in document list
    parent_document_id: Optional[str]   # Optional - Parent document ID for nesting
```

---

### EditDocumentRequest

```python
class EditDocumentRequest:
    document_id: str                    # Required - Document ID to edit
    title: str                          # Required - New document title
```

---

## Response Models

### CreateDocumentResponse

```python
class CreateDocumentResponse:
    payload: CreateDocumentPayload      # Response payload
    type: str                           # Response type ("CreateDocument")
```

---

### CreateDocumentPayload

```python
class CreateDocumentPayload:
    document: Document                  # Created document
```

---

### EditDocumentResponse

```python
class EditDocumentResponse:
    payload: EditDocumentPayload        # Response payload
    type: str                           # Response type ("EditDocument")
```

---

### EditDocumentPayload

```python
class EditDocumentPayload:
    document: EditDocument              # Edited document
```

---

### GetDocumentsRequest

```python
class GetDocumentsRequest:
    kind: Kind                          # Required - Document scope (Space/Member/Project)
    kind_id: str                        # Required - ID of space/member/project
```

---

### GetDocumentsResponse

```python
class GetDocumentsResponse:
    payload: GetDocumentsPayload        # Response payload
    type: str                           # Response type ("GetDocuments")
```

---

### GetDocumentsPayload

```python
class GetDocumentsPayload:
    documents: List[Document]           # List of documents
```

---

### GetDocumentRequest

```python
class GetDocumentRequest:
    document_id: str                    # Required - Document ID
```

---

### ReplaceDocumentRequest

```python
class ReplaceDocumentRequest:
    document_id: str                    # Required - Document ID
    description: str                    # Required - New document content
```

---

### ReplaceDocumentResponse

```python
class ReplaceDocumentResponse:
    # Empty response on success
    pass
```

---

### ReplaceJSONDocumentRequest

```python
class ReplaceJSONDocumentRequest:
    document_id: str                    # Required - Document ID
    content: List[Dict[str, Any]]       # Required - JSONContent array in document structure format
```

---

### ReplaceJSONDocumentResponse

```python
class ReplaceJSONDocumentResponse:
    # Empty response on success
    pass
```

---

## See Also

- [Documents Guide](../guides/documents) - Usage examples and patterns
- [Enums](./enums) - Kind enum for document scopes

