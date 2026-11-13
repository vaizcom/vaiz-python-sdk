"""
Tests for replaceMarkdownDocument, appendMarkdownDocument and getMarkdownDocument API endpoints.

These are the recommended document content routes: markdown is converted to
native document blocks on the server and written to the rich editor format.
"""

import pytest
from tests.lexical_utils import find_nodes, mentions
from tests.test_config import get_test_client
from vaiz.models import CreateTaskRequest, TaskPriority


def _create_test_task(client, name: str, description: str = "Initial description"):
    """Create a task and return it (its `.document` is the document ID)."""
    boards = client.get_boards()
    if not boards or not boards.boards:
        pytest.skip("No boards available for testing")

    board = boards.boards[0]

    task_request = CreateTaskRequest(
        name=name,
        group=client.space_id,
        board=board.id,
        priority=TaskPriority.General,
        description=description,
    )

    task_response = client.create_task(task_request)
    assert task_response.task.document, "Task should have a document ID"
    return task_response.task


def _create_test_document(client, name: str, description: str = "Initial description") -> str:
    """Create a task and return its document ID."""
    return _create_test_task(client, name, description).document


def test_get_markdown_document_returns_string():
    """Test that get_markdown_document returns the task description as a markdown string."""
    client = get_test_client()
    document_id = _create_test_document(
        client,
        "Test Get Markdown Document",
        description="MARKDOWN-GET-MARKER plain description",
    )

    markdown = client.get_markdown_document(document_id)

    assert isinstance(markdown, str)
    assert "MARKDOWN-GET-MARKER" in markdown

    print(f"✅ Successfully fetched markdown for document {document_id}")


def test_replace_markdown_document():
    """Test replacing document content with markdown."""
    client = get_test_client()
    document_id = _create_test_document(
        client,
        "Test Replace Markdown Document",
        description="OLD-MD-MARKER - should be removed after replace",
    )

    new_markdown = (
        "# Replaced Title\n\n"
        "Paragraph with **bold** and *italic* and `inline code`.\n\n"
        "- bullet one\n"
        "- bullet two\n\n"
        "1. ordered one\n"
        "2. ordered two\n"
    )

    response = client.replace_markdown_document(document_id=document_id, markdown=new_markdown)
    assert response is not None

    saved = client.get_markdown_document(document_id)

    # Old content must be completely gone
    assert "OLD-MD-MARKER" not in saved, "Old content still exists - replace behaved like append"

    # New content must be present with structure preserved
    assert "Replaced Title" in saved
    assert "**bold**" in saved
    assert "bullet one" in saved
    assert "ordered two" in saved

    print(f"✅ Successfully replaced document {document_id} with markdown content")


def test_append_markdown_document():
    """Test appending markdown content to an existing document."""
    client = get_test_client()
    document_id = _create_test_document(
        client,
        "Test Append Markdown Document",
        description="INITIAL-MD-MARKER initial content",
    )

    response = client.append_markdown_document(
        document_id=document_id,
        markdown="## Appended Section\n\nAPPENDED-MD-MARKER extra notes",
    )
    assert response is not None

    saved = client.get_markdown_document(document_id)

    assert "INITIAL-MD-MARKER" in saved, "Original content should still exist"
    assert "APPENDED-MD-MARKER" in saved, "Appended content should be added"
    assert saved.index("INITIAL-MD-MARKER") < saved.index("APPENDED-MD-MARKER"), (
        "Appended content should come after the original content"
    )

    print(f"✅ Successfully appended markdown to document {document_id}")


def test_markdown_roundtrip_rich_structures():
    """Test that rich markdown structures survive the write/read round-trip."""
    client = get_test_client()
    document_id = _create_test_document(client, "Test Markdown Roundtrip")

    markdown = (
        "# Roundtrip Test\n\n"
        "## Checklist\n\n"
        "- [ ] open item\n"
        "- [x] done item\n\n"
        "## Code\n\n"
        "```python\nprint(\"hello\")\n```\n\n"
        "## Quote\n\n"
        "> quoted line\n\n"
        "[Vaiz](https://vaiz.com)\n"
    )

    client.replace_markdown_document(document_id=document_id, markdown=markdown)
    saved = client.get_markdown_document(document_id)

    assert "Roundtrip Test" in saved
    assert "open item" in saved
    assert "done item" in saved
    assert 'print("hello")' in saved
    assert "quoted line" in saved
    assert "https://vaiz.com" in saved

    print(f"✅ Markdown round-trip preserved rich structures for document {document_id}")


def test_markdown_table_roundtrip():
    """Test that GFM tables survive the round-trip, including inline formatting in cells."""
    client = get_test_client()
    document_id = _create_test_document(client, "Test Markdown Table Roundtrip")

    table_lines = [
        "| Feature | Status | Notes |",
        "| --- | --- | --- |",
        "| **Bold cell** | `code cell` | plain |",
        "| [Link](https://vaiz.com) | ~~strike~~ | *italic* |",
        "| Alice | Dev | 30 |",
    ]
    markdown = "# Table Test\n\n" + "\n".join(table_lines) + "\n\nAfter table.\n"

    client.replace_markdown_document(document_id=document_id, markdown=markdown)
    saved = client.get_markdown_document(document_id)

    # The whole table block must survive verbatim
    for line in table_lines:
        assert line in saved, f"Table line lost in round-trip: {line}"

    assert "After table." in saved

    print(f"✅ Table round-trip preserved structure and cell formatting for document {document_id}")


def test_markdown_nested_lists_roundtrip():
    """Test that nested bullet and ordered lists (4-space indents) survive the round-trip."""
    client = get_test_client()
    document_id = _create_test_document(client, "Test Markdown Nested Lists")

    markdown = (
        "- level 1\n"
        "    - level 2\n"
        "        - level 3\n"
        "\n"
        "1. first\n"
        "    1. nested first\n"
        "2. second\n"
    )

    client.replace_markdown_document(document_id=document_id, markdown=markdown)
    saved = client.get_markdown_document(document_id)

    assert "- level 1" in saved
    assert "    - level 2" in saved, "2nd nesting level lost"
    assert "        - level 3" in saved, "3rd nesting level lost"
    assert "1. first" in saved
    assert "    1. nested first" in saved, "Nested ordered list lost"
    assert "2. second" in saved

    print(f"✅ Nested lists round-trip preserved indentation for document {document_id}")


def test_markdown_complex_document_roundtrip():
    """Test a large mixed document: headings, table, hr, quote, code, checklist, equations."""
    client = get_test_client()
    document_id = _create_test_document(client, "Test Markdown Complex Document")

    markdown = (
        "# Release Report\n\n"
        "## Summary\n\n"
        "Stats for ==current== sprint with $E=mc^2$ inline math.\n\n"
        "| Metric | Value |\n"
        "| --- | --- |\n"
        "| Tasks done | **42** |\n"
        "| Bugs fixed | `17` |\n\n"
        "---\n\n"
        "## Checklist\n\n"
        "- [x] deploy api\n"
        "- [ ] deploy app\n\n"
        "## Snippet\n\n"
        "```ts\nconst x: number = 1;\n```\n\n"
        "> Note: numbers are preliminary\n\n"
        "$$\\int_0^1 x dx$$\n"
    )

    client.replace_markdown_document(document_id=document_id, markdown=markdown)
    saved = client.get_markdown_document(document_id)

    # Headings
    assert "# Release Report" in saved
    assert "## Summary" in saved
    # Table with formatted cells
    assert "| Metric | Value |" in saved
    assert "| Tasks done | **42** |" in saved
    assert "| Bugs fixed | `17` |" in saved
    # Horizontal rule
    assert "---" in saved
    # Checklist with states
    assert "- [x] deploy api" in saved
    assert "- [ ] deploy app" in saved
    # Code block with language
    assert "```ts" in saved
    assert "const x: number = 1;" in saved
    # Quote
    assert "> Note: numbers are preliminary" in saved
    # Equations and highlight
    assert "$E=mc^2$" in saved
    assert "\\int_0^1 x dx" in saved
    assert "==current==" in saved

    print(f"✅ Complex document round-trip preserved all structures for document {document_id}")


def test_markdown_append_table_to_existing_content():
    """Test appending a table after existing rich content keeps both parts intact."""
    client = get_test_client()
    document_id = _create_test_document(client, "Test Append Table")

    client.replace_markdown_document(
        document_id=document_id,
        markdown="# Base Document\n\nIntro paragraph.\n",
    )

    client.append_markdown_document(
        document_id=document_id,
        markdown="## Data\n\n| Col A | Col B |\n| --- | --- |\n| 1 | 2 |\n",
    )

    saved = client.get_markdown_document(document_id)

    assert "# Base Document" in saved
    assert "Intro paragraph." in saved
    assert "| Col A | Col B |" in saved
    assert "| 1 | 2 |" in saved
    assert saved.index("Intro paragraph.") < saved.index("| Col A | Col B |"), (
        "Appended table should come after the original content"
    )

    print(f"✅ Appended table after existing content for document {document_id}")


def test_markdown_table_with_header_row_roundtrip():
    """Test that the first table row becomes a header row and columns are preserved."""
    client = get_test_client()
    document_id = _create_test_document(client, "Test Markdown Table Header")

    client.replace_markdown_document(
        document_id=document_id,
        markdown="| Task | Status |\n| --- | --- |\n| API | Done |\n| Docs | Todo |\n",
    )

    saved = client.get_markdown_document(document_id)
    assert "| Task | Status |" in saved
    assert "| --- | --- |" in saved
    assert "| API | Done |" in saved
    assert "| Docs | Todo |" in saved

    tables = find_nodes(client.get_json_document(document_id), "table")
    assert len(tables) == 1, "Markdown table should become one native table block"
    assert len(tables[0]["children"]) == 3, "Expected header row + 2 body rows"

    print(f"✅ Table header row round-trip preserved for document {document_id}")


def test_markdown_checklist_roundtrip():
    """Test that checklists keep their checked state and nesting."""
    client = get_test_client()
    document_id = _create_test_document(client, "Test Markdown Checklist")

    markdown = (
        "# Launch\n\n"
        "- [x] Phase 1\n"
        "    - [x] Define requirements\n"
        "    - [ ] Review with stakeholders\n"
        "- [ ] Phase 2\n"
        "    - [ ] Implement\n"
        "        - [ ] Unit tests\n"
    )

    client.replace_markdown_document(document_id=document_id, markdown=markdown)
    saved = client.get_markdown_document(document_id)

    assert "- [x] Phase 1" in saved
    assert "    - [x] Define requirements" in saved
    assert "    - [ ] Review with stakeholders" in saved
    assert "- [ ] Phase 2" in saved
    assert "        - [ ] Unit tests" in saved, "3rd nesting level of the checklist lost"

    print(f"✅ Checklist round-trip preserved state and nesting for document {document_id}")


def test_markdown_mentions_roundtrip():
    """Test that user, task, document and milestone mentions survive the round-trip."""
    client = get_test_client()
    task = _create_test_task(client, "Test Markdown Mentions")
    document_id = task.document
    member_id = client.get_profile().profile.member_id

    milestones = client.get_milestones().milestones
    milestone_id = milestones[0].id if milestones else None

    expected = {("user", member_id), ("task", task.id), ("document", document_id)}
    markdown = (
        "# Mentions\n\n"
        f"User: @[Me](user:{member_id})\n\n"
        f"Task: @[This task](task:{task.id})\n\n"
        f"Document: @[This doc](document:{document_id})\n"
    )
    if milestone_id:
        expected.add(("milestone", milestone_id))
        markdown += f"\nMilestone: @[Release](milestone:{milestone_id})\n"

    client.replace_markdown_document(document_id=document_id, markdown=markdown)
    saved = client.get_markdown_document(document_id)

    # The label is cosmetic: only kind and id are stored, so the export uses the kind as label
    for kind, entity_id in expected:
        assert f"@[{kind}]({kind}:{entity_id})" in saved, f"{kind} mention lost in round-trip"

    # Native mention nodes were created (not plain text)
    found = mentions(client.get_json_document(document_id))
    assert len(found) == len(expected)
    assert member_id in [entity_id for _, entity_id in found]
    assert task.id in [entity_id for _, entity_id in found]

    print(f"✅ Mentions round-trip preserved for document {document_id}")


def test_markdown_mentions_in_table_and_list():
    """Test that mentions work inside table cells and list items."""
    client = get_test_client()
    document_id = _create_test_document(client, "Test Markdown Mentions In Containers")
    member_id = client.get_profile().profile.member_id

    markdown = (
        "| Role | Member |\n"
        "| --- | --- |\n"
        f"| Lead | @[Me](user:{member_id}) |\n\n"
        f"- Reviewer @[Me](user:{member_id})\n"
    )

    client.replace_markdown_document(document_id=document_id, markdown=markdown)

    found = mentions(client.get_json_document(document_id))
    assert [entity_id for _, entity_id in found] == [member_id, member_id]

    print(f"✅ Mentions inside table and list preserved for document {document_id}")


def test_markdown_details_roundtrip():
    """Test that :::details containers keep summary, open state and nested blocks."""
    client = get_test_client()
    document_id = _create_test_document(client, "Test Markdown Details")

    markdown = (
        ":::details{summary=\"Open section\" open}\n"
        "Inner **bold** text\n\n"
        "- item one\n"
        "- item two\n"
        ":::\n\n"
        ":::details{summary=\"Collapsed section\"}\n"
        "Hidden text\n"
        ":::\n"
    )

    client.replace_markdown_document(document_id=document_id, markdown=markdown)
    saved = client.get_markdown_document(document_id)

    assert ':::details{summary="Open section" open}' in saved
    assert "Inner **bold** text" in saved
    assert "- item one" in saved
    assert ':::details{summary="Collapsed section"}' in saved
    assert "Hidden text" in saved
    assert sum(1 for line in saved.splitlines() if line.strip() == ":::") == 2, "Each details block must be closed"

    print(f"✅ Details round-trip preserved summaries and open state for document {document_id}")


def test_markdown_code_roundtrip():
    """Test that fenced code (with languages, multi-line, special chars) and mermaid survive."""
    client = get_test_client()
    document_id = _create_test_document(client, "Test Markdown Code")

    markdown = (
        "Inline `code` here.\n\n"
        "```python\n"
        "def greet(name):\n"
        "    return f\"Hello, {name}!\"  # <tag> & more\n"
        "```\n\n"
        "```bash\n"
        "npm install && npm test\n"
        "```\n\n"
        "```mermaid\n"
        "graph LR\n"
        "    A --> B\n"
        "```\n"
    )

    client.replace_markdown_document(document_id=document_id, markdown=markdown)
    saved = client.get_markdown_document(document_id)

    assert "Inline `code` here." in saved
    assert "```python" in saved
    assert "    return f\"Hello, {name}!\"  # <tag> & more" in saved, "Code indentation or special chars lost"
    assert "```bash" in saved
    assert "npm install && npm test" in saved
    assert "```mermaid\ngraph LR\n    A --> B\n```" in saved, "Mermaid diagram lost"

    print(f"✅ Code round-trip preserved languages and content for document {document_id}")


def test_markdown_callout_columns_and_image_roundtrip():
    """Test callout, columns and standalone image blocks."""
    client = get_test_client()
    document_id = _create_test_document(client, "Test Markdown Containers")

    markdown = (
        ":::callout{icon=\"Light\" color=\"blue\"}\n"
        "Callout text\n"
        ":::\n\n"
        ":::columns\n"
        "::col\n"
        "Left column\n"
        "::col\n"
        "Right column\n"
        ":::\n\n"
        "![Logo](https://vaiz.com/logo.png)\n"
    )

    client.replace_markdown_document(document_id=document_id, markdown=markdown)
    saved = client.get_markdown_document(document_id)

    assert ':::callout{icon="Light" color="blue"}' in saved
    assert "Callout text" in saved
    assert ":::columns" in saved
    assert "::col\nLeft column" in saved
    assert "::col\nRight column" in saved
    assert "![Logo](https://vaiz.com/logo.png)" in saved

    print(f"✅ Callout, columns and image round-trip preserved for document {document_id}")


def test_markdown_append_keeps_checklist_and_mentions():
    """Test appending checklist and mention content after existing blocks."""
    client = get_test_client()
    task = _create_test_task(client, "Test Markdown Append Mixed")
    member_id = client.get_profile().profile.member_id

    client.replace_markdown_document(task.document, "# Base\n\nBase paragraph.\n")
    client.append_markdown_document(
        task.document,
        f"## Follow-up\n\n- [ ] Ask @[Me](user:{member_id})\n- [x] Done item\n",
    )

    saved = client.get_markdown_document(task.document)
    assert "Base paragraph." in saved
    assert "- [ ] Ask @[user](user:" in saved
    assert "- [x] Done item" in saved
    assert saved.index("Base paragraph.") < saved.index("- [ ] Ask")

    print(f"✅ Appended checklist with mention to document {task.document}")


if __name__ == "__main__":
    print("Running markdown document tests...")
    test_get_markdown_document_returns_string()
    test_replace_markdown_document()
    test_append_markdown_document()
    test_markdown_roundtrip_rich_structures()
    test_markdown_table_roundtrip()
    test_markdown_nested_lists_roundtrip()
    test_markdown_complex_document_roundtrip()
    test_markdown_append_table_to_existing_content()
    test_markdown_table_with_header_row_roundtrip()
    test_markdown_checklist_roundtrip()
    test_markdown_mentions_roundtrip()
    test_markdown_mentions_in_table_and_list()
    test_markdown_details_roundtrip()
    test_markdown_code_roundtrip()
    test_markdown_callout_columns_and_image_roundtrip()
    test_markdown_append_keeps_checklist_and_mentions()
    print("All tests passed! ✅")
