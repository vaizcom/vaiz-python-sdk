"""
Example: Working with document content as Markdown.

Demonstrates the recommended Markdown document API:
- replace_markdown_document - replace content with Markdown
- append_markdown_document - append Markdown to existing content
- get_markdown_document - read content back as Markdown
"""

from examples.config import get_client
from vaiz.models import CreateDocumentRequest, Kind


def main():
    client = get_client()

    try:
        response = client.create_document(
            CreateDocumentRequest(
                kind=Kind.Space,
                kind_id=client.space_id,
                title="Markdown Document Demo",
                index=0
            )
        )
        document_id = response.payload.document.id
        print(f"Created document: {document_id}\n")

        client.replace_markdown_document(
            document_id=document_id,
            markdown="""# Release Notes

Some **bold** and *italic* text with a [link](https://vaiz.com).

## Checklist

- [x] Implement feature
- [ ] Write docs

## Metrics

| Metric | Value |
|--------|-------|
| Tasks  | 42    |
| Bugs   | 3     |

```python
print("Hello, Vaiz!")
```
"""
        )
        print("✅ Content replaced")

        client.append_markdown_document(
            document_id=document_id,
            markdown="## Update\n\n1. First follow-up\n2. Second follow-up"
        )
        print("✅ Content appended")

        markdown = client.get_markdown_document(document_id)
        print("\n=== Document as Markdown ===\n")
        print(markdown)

    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
