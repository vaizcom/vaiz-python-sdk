"""
Helper functions for building valid TipTap JSON content.

This module provides type-safe builders for TipTap document nodes and marks,
ensuring only validated elements are used with the replace_json_document API.
"""

from typing import List, Dict, Any, Optional, Literal, Union
from typing_extensions import TypedDict, NotRequired


# Type definitions for TipTap marks
class BoldMark(TypedDict):
    """Bold text formatting mark."""
    type: Literal["bold"]


class ItalicMark(TypedDict):
    """Italic text formatting mark."""
    type: Literal["italic"]


class CodeMark(TypedDict):
    """Inline code formatting mark."""
    type: Literal["code"]


class LinkMarkAttrs(TypedDict):
    """Attributes for link mark."""
    href: str
    target: NotRequired[str]


class LinkMark(TypedDict):
    """Link mark with href and optional target."""
    type: Literal["link"]
    attrs: LinkMarkAttrs


# Union type for all supported marks
Mark = Union[BoldMark, ItalicMark, CodeMark, LinkMark]


# Type definitions for TipTap text node
class TextNode(TypedDict):
    """Text node with optional formatting marks."""
    type: Literal["text"]
    text: str
    marks: NotRequired[List[Mark]]


# Type definitions for heading attributes
class HeadingAttrs(TypedDict):
    """Attributes for heading node."""
    level: Literal[1, 2, 3, 4, 5, 6]


# Type definitions for ordered list attributes
class OrderedListAttrs(TypedDict):
    """Attributes for ordered list node."""
    start: NotRequired[int]


# Forward references for recursive types
TipTapContent = Union[TextNode, 'ParagraphNode', 'HeadingNode', 'BulletListNode', 'OrderedListNode', 'ListItemNode']


class ParagraphNode(TypedDict):
    """Paragraph node containing text and other inline content."""
    type: Literal["paragraph"]
    content: NotRequired[List[TipTapContent]]


class HeadingNode(TypedDict):
    """Heading node with level 1-6."""
    type: Literal["heading"]
    attrs: HeadingAttrs
    content: NotRequired[List[TipTapContent]]


class ListItemNode(TypedDict):
    """List item node, can contain paragraphs and nested lists."""
    type: Literal["listItem"]
    content: NotRequired[List[TipTapContent]]


class BulletListNode(TypedDict):
    """Bullet (unordered) list node."""
    type: Literal["bulletList"]
    content: List[ListItemNode]


class OrderedListNode(TypedDict):
    """Ordered (numbered) list node."""
    type: Literal["orderedList"]
    attrs: NotRequired[OrderedListAttrs]
    content: List[ListItemNode]


# Main content type
TipTapNode = Union[ParagraphNode, HeadingNode, BulletListNode, OrderedListNode, ListItemNode]


# Helper functions

def text(content: str, bold: bool = False, italic: bool = False, 
         code: bool = False, link: Optional[str] = None, 
         link_target: str = "_blank") -> TextNode:
    """
    Create a text node with optional formatting.
    
    Args:
        content: The text content
        bold: Apply bold formatting
        italic: Apply italic formatting
        code: Apply inline code formatting
        link: URL for link (if provided, makes text a hyperlink)
        link_target: Link target attribute (default: "_blank")
    
    Returns:
        TextNode: A valid TipTap text node
        
    Example:
        >>> text("Hello World", bold=True)
        {'type': 'text', 'text': 'Hello World', 'marks': [{'type': 'bold'}]}
    """
    node: TextNode = {"type": "text", "text": content}
    marks: List[Mark] = []
    
    if bold:
        marks.append({"type": "bold"})
    if italic:
        marks.append({"type": "italic"})
    if code:
        marks.append({"type": "code"})
    if link:
        marks.append({"type": "link", "attrs": {"href": link, "target": link_target}})
    
    if marks:
        node["marks"] = marks
    
    return node


def paragraph(*content: Union[TextNode, str]) -> ParagraphNode:
    """
    Create a paragraph node.
    
    Args:
        *content: Text nodes or strings (strings will be converted to text nodes)
    
    Returns:
        ParagraphNode: A valid TipTap paragraph node
        
    Example:
        >>> paragraph("Hello ", text("World", bold=True))
        {'type': 'paragraph', 'content': [{'type': 'text', 'text': 'Hello '}, ...]}
    """
    node: ParagraphNode = {"type": "paragraph"}
    if content:
        node["content"] = [
            item if isinstance(item, dict) else text(item)
            for item in content
        ]
    return node


def heading(level: Literal[1, 2, 3, 4, 5, 6], *content: Union[TextNode, str]) -> HeadingNode:
    """
    Create a heading node.
    
    Args:
        level: Heading level (1-6)
        *content: Text nodes or strings
    
    Returns:
        HeadingNode: A valid TipTap heading node
        
    Example:
        >>> heading(1, "Title")
        {'type': 'heading', 'attrs': {'level': 1}, 'content': [{'type': 'text', 'text': 'Title'}]}
    """
    node: HeadingNode = {
        "type": "heading",
        "attrs": {"level": level}
    }
    if content:
        node["content"] = [
            item if isinstance(item, dict) else text(item)
            for item in content
        ]
    return node


def list_item(*content: Union[ParagraphNode, BulletListNode, OrderedListNode]) -> ListItemNode:
    """
    Create a list item node.
    
    Args:
        *content: Paragraphs or nested lists
    
    Returns:
        ListItemNode: A valid TipTap list item node
        
    Example:
        >>> list_item(paragraph("First item"))
        {'type': 'listItem', 'content': [{'type': 'paragraph', ...}]}
    """
    node: ListItemNode = {"type": "listItem"}
    if content:
        node["content"] = list(content)
    return node


def bullet_list(*items: Union[ListItemNode, str]) -> BulletListNode:
    """
    Create a bullet (unordered) list.
    
    Args:
        *items: List item nodes or strings (strings will be wrapped in list items)
    
    Returns:
        BulletListNode: A valid TipTap bullet list node
        
    Example:
        >>> bullet_list("First", "Second")
        {'type': 'bulletList', 'content': [{'type': 'listItem', ...}, ...]}
    """
    content: List[ListItemNode] = []
    for item in items:
        if isinstance(item, str):
            content.append(list_item(paragraph(item)))
        else:
            content.append(item)
    
    return {"type": "bulletList", "content": content}


def ordered_list(*items: Union[ListItemNode, str], start: int = 1) -> OrderedListNode:
    """
    Create an ordered (numbered) list.
    
    Args:
        *items: List item nodes or strings (strings will be wrapped in list items)
        start: Starting number for the list (default: 1)
    
    Returns:
        OrderedListNode: A valid TipTap ordered list node
        
    Example:
        >>> ordered_list("First", "Second", start=1)
        {'type': 'orderedList', 'attrs': {'start': 1}, 'content': [...]}
    """
    content: List[ListItemNode] = []
    for item in items:
        if isinstance(item, str):
            content.append(list_item(paragraph(item)))
        else:
            content.append(item)
    
    node: OrderedListNode = {"type": "orderedList", "content": content}
    if start != 1:
        node["attrs"] = {"start": start}
    
    return node


def link_text(content: str, href: str, target: str = "_blank", 
              bold: bool = False, italic: bool = False) -> TextNode:
    """
    Create a hyperlink text node.
    
    Args:
        content: The link text
        href: The URL
        target: Link target (default: "_blank")
        bold: Apply bold formatting
        italic: Apply italic formatting
    
    Returns:
        TextNode: A text node with link mark
        
    Example:
        >>> link_text("Visit Vaiz", "https://vaiz.app")
        {'type': 'text', 'text': 'Visit Vaiz', 'marks': [{'type': 'link', ...}]}
    """
    return text(content, bold=bold, italic=italic, link=href, link_target=target)


def separator(char: str = "━", length: int = 43) -> ParagraphNode:
    """
    Create a visual separator paragraph.
    
    Args:
        char: Character to use for separator (default: "━")
        length: Length of the separator (default: 43)
    
    Returns:
        ParagraphNode: A paragraph with separator line
        
    Example:
        >>> separator()
        {'type': 'paragraph', 'content': [{'type': 'text', 'text': '━━━...'}]}
    """
    return paragraph(char * length)


# Convenience exports
__all__ = [
    # Types
    'TipTapNode',
    'TextNode',
    'ParagraphNode',
    'HeadingNode',
    'BulletListNode',
    'OrderedListNode',
    'ListItemNode',
    'Mark',
    
    # Builders
    'text',
    'paragraph',
    'heading',
    'list_item',
    'bullet_list',
    'ordered_list',
    'link_text',
    'separator',
]

