"""
Tests for special document blocks: TOC, Anchors, Siblings, Code Block, and Task Lists.
"""

import json
from vaiz import toc_block, anchors_block, siblings_block, code_block, heading, task_list, task_item, paragraph


def test_toc_block_structure():
    """Test that toc_block creates correct structure."""
    toc = toc_block()
    
    # Check basic structure
    assert toc["type"] == "doc-siblings"
    assert "attrs" in toc
    assert "content" in toc
    
    # Check attributes
    attrs = toc["attrs"]
    assert attrs["custom"] == 1
    assert attrs["contenteditable"] == "false"
    assert "uid" in attrs
    assert len(attrs["uid"]) > 0
    
    # Check content
    assert len(toc["content"]) == 1
    content_item = toc["content"][0]
    assert content_item["type"] == "text"
    
    # Parse the JSON text content
    data = json.loads(content_item["text"])
    assert data["type"] == "toc"


def test_toc_block_serialization():
    """Test that toc_block can be serialized to JSON."""
    toc = toc_block()
    
    # Should be serializable without errors
    json_str = json.dumps(toc, ensure_ascii=False)
    assert isinstance(json_str, str)
    assert '"type": "doc-siblings"' in json_str
    # The inner JSON is escaped, so we check for the escaped version
    assert '\\"type\\": \\"toc\\"' in json_str or '"type": "toc"' in json_str


def test_multiple_toc_blocks_have_unique_uids():
    """Test that multiple TOC blocks get unique UIDs."""
    toc1 = toc_block()
    toc2 = toc_block()
    
    uid1 = toc1["attrs"]["uid"]
    uid2 = toc2["attrs"]["uid"]
    
    assert uid1 != uid2
    assert len(uid1) > 0
    assert len(uid2) > 0


def test_anchors_block_structure():
    """Test that anchors_block creates correct structure."""
    anchors = anchors_block()
    
    # Check basic structure
    assert anchors["type"] == "doc-siblings"
    assert "attrs" in anchors
    assert "content" in anchors
    
    # Check attributes
    attrs = anchors["attrs"]
    assert attrs["custom"] == 1
    assert attrs["contenteditable"] == "false"
    assert "uid" in attrs
    assert len(attrs["uid"]) > 0
    
    # Check content
    assert len(anchors["content"]) == 1
    content_item = anchors["content"][0]
    assert content_item["type"] == "text"
    
    # Parse the JSON text content
    data = json.loads(content_item["text"])
    assert data["type"] == "anchors"


def test_anchors_block_serialization():
    """Test that anchors_block can be serialized to JSON."""
    anchors = anchors_block()
    
    # Should be serializable without errors
    json_str = json.dumps(anchors, ensure_ascii=False)
    assert isinstance(json_str, str)
    assert '"type": "doc-siblings"' in json_str
    # The inner JSON is escaped, so we check for the escaped version
    assert '\\"type\\": \\"anchors\\"' in json_str or '"type": "anchors"' in json_str


def test_toc_and_anchors_blocks_can_coexist():
    """Test that TOC and Anchors blocks can be used together."""
    toc = toc_block()
    anchors = anchors_block()
    
    # Both should have different UIDs
    assert toc["attrs"]["uid"] != anchors["attrs"]["uid"]
    
    # Both should be doc-siblings type
    assert toc["type"] == "doc-siblings"
    assert anchors["type"] == "doc-siblings"
    
    # But different data types
    toc_data = json.loads(toc["content"][0]["text"])
    anchors_data = json.loads(anchors["content"][0]["text"])
    
    assert toc_data["type"] == "toc"
    assert anchors_data["type"] == "anchors"


def test_siblings_block_structure():
    """Test that siblings_block creates correct structure."""
    siblings = siblings_block()
    
    # Check basic structure
    assert siblings["type"] == "doc-siblings"
    assert "attrs" in siblings
    assert "content" in siblings
    
    # Check attributes
    attrs = siblings["attrs"]
    assert attrs["custom"] == 1
    assert attrs["contenteditable"] == "false"
    assert "uid" in attrs
    assert len(attrs["uid"]) > 0
    
    # Check content
    assert len(siblings["content"]) == 1
    content_item = siblings["content"][0]
    assert content_item["type"] == "text"
    
    # Parse the JSON text content
    data = json.loads(content_item["text"])
    assert data["type"] == "siblings"


def test_all_doc_siblings_blocks_have_unique_types():
    """Test that all doc-siblings blocks have correct and unique types."""
    toc = toc_block()
    anchors = anchors_block()
    siblings = siblings_block()
    
    # All should be doc-siblings type
    assert toc["type"] == "doc-siblings"
    assert anchors["type"] == "doc-siblings"
    assert siblings["type"] == "doc-siblings"
    
    # All should have unique UIDs
    uids = [toc["attrs"]["uid"], anchors["attrs"]["uid"], siblings["attrs"]["uid"]]
    assert len(uids) == len(set(uids))  # All unique
    
    # But different data types
    toc_data = json.loads(toc["content"][0]["text"])
    anchors_data = json.loads(anchors["content"][0]["text"])
    siblings_data = json.loads(siblings["content"][0]["text"])
    
    assert toc_data["type"] == "toc"
    assert anchors_data["type"] == "anchors"
    assert siblings_data["type"] == "siblings"


def test_code_block_structure():
    """Test that code_block creates correct structure."""
    code = code_block(code='print("Hello")', language="python")
    
    # Check basic structure
    assert code["type"] == "codeBlock"
    assert "attrs" in code
    assert "content" in code
    
    # Check attributes
    attrs = code["attrs"]
    assert "uid" in attrs
    assert attrs["language"] == "python"
    
    # Check content
    assert len(code["content"]) == 1
    assert code["content"][0]["type"] == "text"
    assert code["content"][0]["text"] == 'print("Hello")'


def test_code_block_empty():
    """Test creating an empty code block."""
    code = code_block()
    
    # Should have type and attrs
    assert code["type"] == "codeBlock"
    assert "attrs" in code
    assert "uid" in code["attrs"]
    
    # Content may or may not be present when empty
    if "content" in code:
        assert code["content"] == []


def test_code_block_without_language():
    """Test creating a code block without specifying language."""
    code = code_block(code="const x = 1;")
    
    assert code["type"] == "codeBlock"
    assert "content" in code
    assert code["content"][0]["text"] == "const x = 1;"
    # Language may not be set
    if "language" in code["attrs"]:
        assert isinstance(code["attrs"]["language"], str)


def test_code_block_multiline():
    """Test code block with multiline code."""
    multiline_code = """def hello():
    print("Hello, World!")
    return True"""
    
    code = code_block(code=multiline_code, language="python")
    
    assert code["type"] == "codeBlock"
    assert code["attrs"]["language"] == "python"
    assert code["content"][0]["text"] == multiline_code


def test_code_block_serialization():
    """Test that code_block can be serialized to JSON."""
    code = code_block(code='console.log("test")', language="javascript")
    
    # Should be serializable without errors
    json_str = json.dumps(code, ensure_ascii=False)
    assert isinstance(json_str, str)
    assert '"type": "codeBlock"' in json_str
    assert '"language": "javascript"' in json_str


def test_multiple_code_blocks_have_unique_uids():
    """Test that multiple code blocks get unique UIDs."""
    code1 = code_block(code="x = 1")
    code2 = code_block(code="y = 2")
    
    uid1 = code1["attrs"]["uid"]
    uid2 = code2["attrs"]["uid"]
    
    assert uid1 != uid2
    assert len(uid1) > 0
    assert len(uid2) > 0


def test_heading_has_uid():
    """Test that heading automatically gets UID for TOC support."""
    h1 = heading(1, "Test Heading")
    
    # Check that heading has UID
    assert "attrs" in h1
    assert "uid" in h1["attrs"]
    assert len(h1["attrs"]["uid"]) == 12
    
    # UID should contain letters and digits
    uid = h1["attrs"]["uid"]
    assert uid.isalnum()


def test_multiple_headings_have_unique_uids():
    """Test that multiple headings get unique UIDs."""
    h1 = heading(1, "First")
    h2 = heading(2, "Second")
    h3 = heading(1, "Third")
    
    uid1 = h1["attrs"]["uid"]
    uid2 = h2["attrs"]["uid"]
    uid3 = h3["attrs"]["uid"]
    
    # All UIDs should be different
    assert uid1 != uid2
    assert uid1 != uid3
    assert uid2 != uid3
    
    # All should be 12 characters
    assert len(uid1) == 12
    assert len(uid2) == 12
    assert len(uid3) == 12


def test_heading_uid_format():
    """Test that heading UID has correct format (letters and digits only)."""
    h = heading(1, "Test")
    uid = h["attrs"]["uid"]
    
    # Should be exactly 12 characters
    assert len(uid) == 12
    
    # Should contain only alphanumeric characters
    assert uid.isalnum()
    
    # Should have mix of cases (statistically likely with 12 chars)
    # At least one test to ensure we're using both upper and lower
    has_upper = any(c.isupper() for c in uid)
    has_lower = any(c.islower() for c in uid)
    
    # With 12 random chars from [a-zA-Z0-9], very likely to have both
    # But we don't strictly require it in single test
    assert has_upper or has_lower  # At least one letter present


# Task List (Checklist) Tests

def test_task_item_structure():
    """Test that task_item creates correct structure."""
    item = task_item("Buy milk", checked=False)
    
    # Check basic structure
    assert item["type"] == "taskItem"
    assert "attrs" in item
    assert "content" in item
    
    # Check attributes
    assert item["attrs"]["checked"] == False
    
    # Check content
    assert len(item["content"]) == 1
    assert item["content"][0]["type"] == "paragraph"
    assert item["content"][0]["content"][0]["text"] == "Buy milk"


def test_task_item_checked():
    """Test that task_item can be marked as checked."""
    item = task_item("Completed task", checked=True)
    
    assert item["type"] == "taskItem"
    assert item["attrs"]["checked"] == True


def test_task_list_structure():
    """Test that task_list creates correct structure."""
    checklist = task_list(
        task_item("Task 1", checked=False),
        task_item("Task 2", checked=True)
    )
    
    # Check basic structure
    assert checklist["type"] == "taskList"
    assert "attrs" in checklist
    assert "content" in checklist
    
    # Check attributes (UID should be auto-generated)
    assert "uid" in checklist["attrs"]
    assert len(checklist["attrs"]["uid"]) > 0
    
    # Check content
    assert len(checklist["content"]) == 2
    assert checklist["content"][0]["type"] == "taskItem"
    assert checklist["content"][1]["type"] == "taskItem"
    assert checklist["content"][0]["attrs"]["checked"] == False
    assert checklist["content"][1]["attrs"]["checked"] == True


def test_task_list_from_strings():
    """Test creating task list from simple strings."""
    checklist = task_list("Todo 1", "Todo 2", "Todo 3")
    
    assert checklist["type"] == "taskList"
    assert len(checklist["content"]) == 3
    
    # All should be task items with checked=False by default
    for item in checklist["content"]:
        assert item["type"] == "taskItem"
        assert item["attrs"]["checked"] == False


def test_nested_task_list():
    """Test creating nested task lists (multi-level checklist)."""
    nested = task_list(
        task_item(
            paragraph("Phase 1: Planning"),
            task_list(
                task_item("Define requirements", checked=True),
                task_item("Create wireframes", checked=False)
            ),
            checked=False
        ),
        task_item(
            paragraph("Phase 2: Development"),
            task_list(
                task_item("Setup project", checked=False),
                task_item("Implement features", checked=False)
            ),
            checked=False
        )
    )
    
    # Check main task list structure
    assert nested["type"] == "taskList"
    assert len(nested["content"]) == 2
    
    # Check first item has nested task list
    first_item = nested["content"][0]
    assert first_item["type"] == "taskItem"
    assert first_item["attrs"]["checked"] == False
    assert len(first_item["content"]) == 2  # paragraph + nested task list
    
    # Check nested task list
    nested_list = first_item["content"][1]
    assert nested_list["type"] == "taskList"
    assert len(nested_list["content"]) == 2
    assert nested_list["content"][0]["attrs"]["checked"] == True
    assert nested_list["content"][1]["attrs"]["checked"] == False


def test_multiple_task_lists_have_unique_uids():
    """Test that multiple task lists get unique UIDs."""
    list1 = task_list("Item 1")
    list2 = task_list("Item 2")
    list3 = task_list("Item 3")
    
    uid1 = list1["attrs"]["uid"]
    uid2 = list2["attrs"]["uid"]
    uid3 = list3["attrs"]["uid"]
    
    # All UIDs should be different
    assert uid1 != uid2
    assert uid1 != uid3
    assert uid2 != uid3
    
    # All should be non-empty
    assert len(uid1) > 0
    assert len(uid2) > 0
    assert len(uid3) > 0


def test_task_list_serialization():
    """Test that task_list can be serialized to JSON."""
    checklist = task_list(
        task_item("Review PR", checked=True),
        task_item("Deploy", checked=False)
    )
    
    # Should be serializable without errors
    json_str = json.dumps(checklist, ensure_ascii=False)
    assert isinstance(json_str, str)
    assert '"type": "taskList"' in json_str
    assert '"type": "taskItem"' in json_str
    assert '"checked": true' in json_str
    assert '"checked": false' in json_str


def test_complex_nested_task_list():
    """Test creating a complex multi-level nested task list."""
    complex_list = task_list(
        task_item(
            paragraph("Main Task"),
            task_list(
                task_item(
                    paragraph("Subtask 1"),
                    task_list(
                        task_item("Sub-subtask 1.1", checked=True),
                        task_item("Sub-subtask 1.2", checked=False)
                    ),
                    checked=False
                ),
                task_item("Subtask 2", checked=True)
            ),
            checked=False
        )
    )
    
    # Check structure is valid
    assert complex_list["type"] == "taskList"
    
    # Navigate through nested structure
    main_item = complex_list["content"][0]
    assert main_item["type"] == "taskItem"
    
    # Get first level nested list
    level1_list = main_item["content"][1]
    assert level1_list["type"] == "taskList"
    assert len(level1_list["content"]) == 2
    
    # Get second level nested list
    level1_item = level1_list["content"][0]
    level2_list = level1_item["content"][1]
    assert level2_list["type"] == "taskList"
    assert len(level2_list["content"]) == 2
    
    # Verify deepest level items
    assert level2_list["content"][0]["attrs"]["checked"] == True
    assert level2_list["content"][1]["attrs"]["checked"] == False
