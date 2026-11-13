#!/usr/bin/env python3
"""
Example: Tables with header rows in a Personal document, written as Markdown.

In Markdown the first row of a table is its header row, followed by the
`| --- | --- |` divider line. Cells support inline formatting and mentions.
"""

from examples.config import get_client
from vaiz.models import CreateDocumentRequest, Kind


def main():
    print("=== Table Header Example ===\n")

    client = get_client()

    # Get current user's member ID for a Personal document
    profile = client.get_profile()
    member_id = profile.profile.member_id

    doc_response = client.create_document(
        CreateDocumentRequest(
            kind=Kind.Member,
            kind_id=member_id,
            title="Table Headers Demo",
            index=0,
        )
    )
    document_id = doc_response.payload.document.id
    print(f"✅ Document created: {document_id}\n")

    markdown = f"""# 📊 Table Headers Demo

This document demonstrates the header row of Markdown tables.

---

## Example 1: Simple table

| Task | Assignee | Status | Priority |
| --- | --- | --- | --- |
| Implement API | John | ✅ Done | High |
| Write tests | Jane | ⏳ In Progress | High |
| Documentation | Mike | 📋 Todo | Medium |

## Example 2: Formatted headers and cells

| **Component** | **Version** | **Notes** |
| --- | --- | --- |
| `vaiz-sdk` | `1.0.0` | *Markdown only* |
| [Docs](https://vaiz.com) | latest | ~~old~~ new |

## Example 3: Mentions in cells

| Role | Member |
| --- | --- |
| Owner | @[Me](user:{member_id}) |
"""

    client.replace_markdown_document(document_id, markdown)
    print("✅ Document written")

    saved = client.get_markdown_document(document_id)
    rows = [line for line in saved.splitlines() if line.startswith("|")]
    print(f"📊 Table rows in saved document: {len(rows)}")
    print("\n" + saved)


if __name__ == "__main__":
    main()
