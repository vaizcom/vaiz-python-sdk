"""Helpers for inspecting Lexical JSON returned by `get_json_document()`."""

from typing import Any, Dict, Iterator, List, Tuple

TEXT_FORMAT_BOLD = 1
TEXT_FORMAT_ITALIC = 2
TEXT_FORMAT_CODE = 16


def root_children(doc: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Top-level blocks of a Lexical editor state."""
    return doc.get("root", {}).get("children", []) or []


def iter_nodes(doc: Dict[str, Any]) -> Iterator[Dict[str, Any]]:
    """Depth-first iteration over every node of a Lexical editor state."""
    stack = list(reversed(root_children(doc)))
    while stack:
        node = stack.pop()
        yield node
        stack.extend(reversed(node.get("children", []) or []))


def find_nodes(doc: Dict[str, Any], node_type: str, **attrs: Any) -> List[Dict[str, Any]]:
    """All nodes of `node_type` whose attributes match `attrs`."""
    return [
        node for node in iter_nodes(doc)
        if node.get("type") == node_type and all(node.get(k) == v for k, v in attrs.items())
    ]


def has_text_format(doc: Dict[str, Any], format_bit: int) -> bool:
    """Whether any text node carries the given Lexical format bit."""
    return any(
        node.get("type") == "text" and (node.get("format") or 0) & format_bit
        for node in iter_nodes(doc)
    )


def mentions(doc: Dict[str, Any]) -> List[Tuple[str, str]]:
    """(kind, id) pairs of all user and entity mentions in document order."""
    result = []
    for node in iter_nodes(doc):
        if node.get("type") == "user-mention":
            result.append(("User", node.get("userId")))
        elif node.get("type") == "entity-mention":
            result.append((node.get("entityKind"), node.get("entityId")))
    return result


def doc_text(doc: Dict[str, Any]) -> str:
    """Concatenated text of all text nodes in document order."""
    return " ".join(node.get("text", "") for node in iter_nodes(doc) if node.get("type") == "text")
