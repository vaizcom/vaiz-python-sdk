---
sidebar_position: 9
sidebar_label: Documents
title: Documents API — Create & Edit Rich Documents | Vaiz Python SDK
description: Learn how to use the Vaiz Python SDK to create, edit, and manage rich-text documents. Write content with Markdown and read it back as Markdown or Lexical JSON.
---

# Documents

Complete reference for document-related methods and models. Document content is written as Markdown - see [Markdown Syntax](./markdown-syntax) for the supported dialect.

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

### `replace_markdown_document`

```python
replace_markdown_document(document_id: str, markdown: str) -> ReplaceMarkdownDocumentResponse
```

Replace document content with Markdown. Markdown is converted to native editor blocks on the server (headings, lists, tables, code blocks, checklists, mentions, callouts, and more). This is the recommended way to write document content. Works for standalone documents and task descriptions.

**Parameters:**
- `document_id` - Document ID to replace content for
- `markdown` - New content as a Markdown string (see [Markdown Syntax](./markdown-syntax))

**Returns:** `ReplaceMarkdownDocumentResponse` (empty on success)

**Example:**
```python
client.replace_markdown_document(
    document_id="doc_id",
    markdown="# Title\n\nSome **bold** text\n\n- item 1\n- item 2"
)
```

---

### `append_markdown_document`

```python
append_markdown_document(document_id: str, markdown: str) -> AppendMarkdownDocumentResponse
```

Append Markdown content to the end of a document without removing existing content.

**Parameters:**
- `document_id` - Document ID to append content to
- `markdown` - Content to append as a Markdown string

**Returns:** `AppendMarkdownDocumentResponse` (empty on success)

**Example:**
```python
client.append_markdown_document(
    document_id="doc_id",
    markdown="## Update\n\nAdditional notes"
)
```

---

### `get_markdown_document`

```python
get_markdown_document(document_id: str) -> str
```

Fetch document content rendered as Markdown. Returns an empty string for legacy documents that have no rich content yet.

**Parameters:**
- `document_id` - Document ID to fetch

**Returns:** `str` - Document content as Markdown

**Example:**
```python
markdown = client.get_markdown_document("doc_id")
print(markdown)
```

---

### `get_json_document`

```python
get_json_document(document_id: str) -> Dict[str, Any]
```

Fetch document content as Lexical JSON (the format of the Vaiz rich editor). Prefer [`get_markdown_document`](#get_markdown_document) for reading content; use this method only when you need the raw node tree.

**Parameters:**
- `document_id` - Document ID (from a task or a standalone document)

**Returns:** `Dict[str, Any]` - Lexical `SerializedEditorState`:

```python
{
    "root": {
        "type": "root",
        "children": [
            {"type": "heading", "tag": "h1", "children": [{"type": "text", "text": "Title", "format": 0}]},
            {"type": "list", "listType": "check", "children": [
                {"type": "listitem", "checked": True, "children": [{"type": "text", "text": "Done"}]}
            ]},
        ]
    }
}
```

Common Lexical node types:

| Content | Lexical node `type` |
|---------|---------------------|
| Paragraph, heading | `paragraph`, `heading` (`tag`: `h1`…`h6`) |
| Bullet / ordered list / checklist | `list` with `listType`: `bullet` / `number` / `check` |
| List item | `listitem` (`checked` for checklists) |
| Blockquote | `quote` |
| Code block | `code` (`language`) |
| Horizontal rule | `document-hr` |
| Table | `table` → `tablerow` → `tablecell` (`colSpan`, `rowSpan`, `headerState`) |
| Details | `details` → `detailsSummary`, `detailsContent` |
| Mention | `user-mention` (`userId`) or `entity-mention` (`entityKind`, `entityId`) |
| Image | `document-image` (`data.src`, `data.caption`) |
| Files | `document-files` (`data.files`) |
| Embed | `document-embed` (`data.provider`, `data.url`) |
| Navigation (TOC, anchors, siblings) | `document-navigation` (`data.navigationType`) |

Text marks are stored as a `format` bitmask on `text` nodes: bold = 1, italic = 2, strikethrough = 4, underline = 8, code = 16. Links are `link` nodes with `url`.

**Example:**
```python
# Standalone document
content = client.get_json_document("document_id")
for block in content["root"]["children"]:
    print(block["type"])

# Task description
task_response = client.get_task("PRJ-123")
description = client.get_json_document(task_response.task.document)
```

---

### `replace_document`

```python
replace_document(document_id: str, description: str) -> ReplaceDocumentResponse
```

Replace document content with a plain text string. Use [`replace_markdown_document`](#replace_markdown_document) for formatted content.

**Parameters:**
- `document_id` - Document ID
- `description` - New content as plain text

**Returns:** `ReplaceDocumentResponse` (empty on success)

**Example:**
```python
client.replace_document(document_id="doc_id", description="New document content")
```

---

### `append_document`

```python
append_document(
    document_id: str,
    description: Optional[str] = None,
    files: Optional[List[Any]] = None
) -> AppendDocumentResponse
```

Append plain text to the end of a document without removing existing content.

**Parameters:**
- `document_id` - Document ID
- `description` - Plain text to append (optional)
- `files` - Files to attach (optional)

**Returns:** `AppendDocumentResponse` (empty on success)

**Example:**
```python
client.append_document(document_id="doc_id", description="\n\nAdditional content")
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

### AppendDocumentRequest

```python
class AppendDocumentRequest:
    document_id: str                    # Required - Document ID
    description: Optional[str]          # Optional - Plain text to append
    files: Optional[List[Any]]          # Optional - Files to attach
```

---

### AppendDocumentResponse

```python
class AppendDocumentResponse:
    # Empty response on success
    pass
```

---

### ReplaceMarkdownDocumentRequest

```python
class ReplaceMarkdownDocumentRequest:
    document_id: str                    # Required - Document ID
    markdown: str                       # Required - New content as Markdown
```

---

### ReplaceMarkdownDocumentResponse

```python
class ReplaceMarkdownDocumentResponse:
    # Empty response on success
    pass
```

---

### AppendMarkdownDocumentRequest

```python
class AppendMarkdownDocumentRequest:
    document_id: str                    # Required - Document ID
    markdown: str                       # Required - Content to append as Markdown
```

---

### AppendMarkdownDocumentResponse

```python
class AppendMarkdownDocumentResponse:
    # Empty response on success
    pass
```

---

### GetMarkdownDocumentRequest

```python
class GetMarkdownDocumentRequest:
    document_id: str                    # Required - Document ID
```

---

### GetMarkdownDocumentResponse

```python
class GetMarkdownDocumentResponse:
    payload: GetMarkdownDocumentPayload # Response payload
    type: str                           # Response type

    @property
    def markdown(self) -> str: ...      # Shortcut for payload.markdown
```

---

### GetMarkdownDocumentPayload

```python
class GetMarkdownDocumentPayload:
    markdown: str                       # Document content as Markdown ("" if empty)
```

---

## See Also

- [Documents Guide](../guides/documents) - Usage examples and patterns
- [Markdown Syntax](./markdown-syntax) - Supported Markdown dialect, containers and mentions
- [Enums](./enums) - Kind enum for document scopes

