#!/usr/bin/env python3
"""
Example: Creating and using checklists in documents with Markdown.

Checklists are written as `- [ ]` (open) and `- [x]` (done) items:
- Checkbox items that can be checked/unchecked
- Nested checklists (indent children by 4 spaces)
- Mixed content (paragraphs, headings and checklists)
"""

from examples.config import get_client
from vaiz.models import CreateDocumentRequest, Kind


SIMPLE_CHECKLIST = """# Daily Tasks

Here's what needs to be done today:

- [x] Review pull requests
- [ ] Update documentation
- [ ] Deploy to production
"""

NESTED_CHECKLIST = """# Project Milestones

- [x] Phase 1: Planning
    - [x] Define requirements
    - [x] Create wireframes
    - [ ] Review with stakeholders
- [ ] Phase 2: Development
    - [x] Setup project structure
    - [ ] Implement features
    - [ ] Testing
        - [ ] Unit tests
        - [ ] Integration tests
        - [ ] E2E tests
- [ ] Phase 3: Deployment
    - [ ] Prepare production environment
    - [ ] Deploy application
    - [ ] Monitor metrics
"""

MIXED_CONTENT = """# Sprint Planning

This sprint we will focus on user authentication.

## Backend Tasks

- [x] Design database schema
- [ ] Implement authentication API
- [ ] Add JWT tokens
- [ ] Write tests

## Frontend Tasks

- [x] Create login page
- [ ] Create registration page
- [ ] Add form validation
- [ ] Connect to API

Review meeting scheduled for Friday.
"""


def main():
    client = get_client()
    client.verbose = True

    print("=== Checklist Examples ===\n")

    try:
        document_id = client.create_document(
            CreateDocumentRequest(
                kind=Kind.Space,
                kind_id=client.space_id,
                title="Checklist Examples",
                index=0,
            )
        ).payload.document.id
        print(f"Created document: {document_id}\n")

        print("1. Writing a simple checklist")
        client.replace_markdown_document(document_id, SIMPLE_CHECKLIST)

        print("2. Appending a nested checklist")
        client.append_markdown_document(document_id, NESTED_CHECKLIST)

        print("3. Appending mixed content with checklists")
        client.append_markdown_document(document_id, MIXED_CONTENT)

        saved = client.get_markdown_document(document_id)
        print("\n=== Document as Markdown ===\n")
        print(saved)

        done = saved.count("- [x]")
        todo = saved.count("- [ ]")
        print(f"\n✅ Checklist items: {done} done, {todo} open")

    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
