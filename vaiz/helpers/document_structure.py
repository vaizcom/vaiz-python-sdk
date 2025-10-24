"""
Helper functions for building valid Document Structure JSON content.

This module provides type-safe builders for document nodes and marks,
ensuring only validated elements are used with the replace_json_document API.
"""

from typing import List, Optional, Literal, Union
from typing_extensions import TypedDict, NotRequired


# Type definitions for text formatting marks
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


# Type definitions for text node
class TextNode(TypedDict):
    """Text node with optional formatting marks."""
    type: Literal["text"]
    text: str
    marks: NotRequired[List[Mark]]


# Type definitions for heading attributes
class HeadingAttrs(TypedDict):
    """Attributes for heading node."""
    level: Literal[1, 2, 3, 4, 5, 6]
    uid: NotRequired[str]


# Type definitions for ordered list attributes
class OrderedListAttrs(TypedDict):
    """Attributes for ordered list node."""
    start: NotRequired[int]


# Type definitions for file and image blocks
class ImageBlockData(TypedDict):
    """Data for image block (stored as JSON string in content)."""
    id: str
    src: str
    thumbSrc: NotRequired[str]
    fileName: str
    caption: NotRequired[str]
    fileType: str
    extension: str
    title: str
    aspectRatio: NotRequired[float]
    fileSize: int
    dimensions: NotRequired[List[int]]
    fileId: str
    dominantColor: NotRequired[dict]


class ImageBlockAttrs(TypedDict):
    """Attributes for image block."""
    uid: str
    custom: Literal[1]
    contenteditable: Literal["false"]
    widthPercent: NotRequired[int]


class ImageBlockNode(TypedDict):
    """Image block node for displaying images."""
    type: Literal["image-block"]
    attrs: ImageBlockAttrs
    content: List[TextNode]


class FileItem(TypedDict):
    """Individual file item in files block."""
    id: str
    fileId: str
    createAt: int
    url: str
    extension: str
    name: str
    size: int
    type: str  # Pdf, Image, Video, etc.
    dominantColor: NotRequired[dict]


class FilesBlockData(TypedDict):
    """Data for files block (stored as JSON string in content)."""
    files: List[FileItem]


class FilesBlockAttrs(TypedDict):
    """Attributes for files block."""
    uid: str
    custom: Literal[1]
    contenteditable: Literal["false"]


class FilesBlockNode(TypedDict):
    """Files block node for displaying file attachments."""
    type: Literal["files"]
    attrs: FilesBlockAttrs
    content: List[TextNode]


# Type definitions for mention blocks
class MentionItem(TypedDict):
    """Item reference in mention block."""
    id: str
    kind: Literal["User", "Document", "Task", "Milestone"]


class MentionData(TypedDict):
    """Data for mention block."""
    item: MentionItem


class MentionAttrs(TypedDict):
    """Attributes for mention block."""
    uid: str
    custom: Literal[1]
    inline: Literal[True]
    data: MentionData


class MentionNode(TypedDict):
    """Mention node for referencing users, documents, tasks, or milestones."""
    type: Literal["custom-mention"]
    attrs: MentionAttrs
    content: List[TextNode]


# Type definitions for doc-siblings block (TOC, Anchors, Siblings, etc.)
class DocSiblingsData(TypedDict):
    """Data for doc-siblings block."""
    type: Literal["toc", "anchors", "siblings"]


class DocSiblingsAttrs(TypedDict):
    """Attributes for doc-siblings block."""
    uid: str
    custom: Literal[1]
    contenteditable: Literal["false"]


class DocSiblingsNode(TypedDict):
    """Doc-siblings node for special document elements like TOC, Anchors, and Siblings."""
    type: Literal["doc-siblings"]
    attrs: DocSiblingsAttrs
    content: List[TextNode]


# Type definitions for code block
class CodeBlockAttrs(TypedDict):
    """Attributes for code block."""
    uid: NotRequired[str]
    language: NotRequired[str]


class CodeBlockNode(TypedDict):
    """Code block node for displaying code with syntax highlighting."""
    type: Literal["codeBlock"]
    attrs: NotRequired[CodeBlockAttrs]
    content: NotRequired[List[TextNode]]


# Forward references for recursive types
DocumentContent = Union[TextNode, 'ParagraphNode', 'HeadingNode', 'BulletListNode', 'OrderedListNode', 'ListItemNode', 'TableNode', 'HorizontalRuleNode', 'BlockquoteNode', 'DetailsNode', 'DetailsSummaryNode', 'DetailsContentNode', MentionNode, ImageBlockNode, FilesBlockNode, DocSiblingsNode, CodeBlockNode]


class ParagraphNode(TypedDict):
    """Paragraph node containing text and other inline content."""
    type: Literal["paragraph"]
    content: NotRequired[List[DocumentContent]]


class HeadingNode(TypedDict):
    """Heading node with level 1-6."""
    type: Literal["heading"]
    attrs: HeadingAttrs
    content: NotRequired[List[DocumentContent]]


class ListItemNode(TypedDict):
    """List item node, can contain paragraphs and nested lists."""
    type: Literal["listItem"]
    content: NotRequired[List[DocumentContent]]


class BulletListNode(TypedDict):
    """Bullet (unordered) list node."""
    type: Literal["bulletList"]
    content: List[ListItemNode]


class OrderedListNode(TypedDict):
    """Ordered (numbered) list node."""
    type: Literal["orderedList"]
    attrs: NotRequired[OrderedListAttrs]
    content: List[ListItemNode]


# Table-related attributes
class TableCellAttrs(TypedDict):
    """Attributes for table cell."""
    colspan: NotRequired[int]
    rowspan: NotRequired[int]


class TableRowAttrs(TypedDict):
    """Attributes for table row."""
    showRowNumbers: NotRequired[bool]


class ExtensionTableAttrs(TypedDict):
    """Attributes for extension-table."""
    uid: NotRequired[str]
    showRowNumbers: NotRequired[bool]


# Table-related nodes
class TableCellNode(TypedDict):
    """Table cell node."""
    type: Literal["tableCell"]
    attrs: NotRequired[TableCellAttrs]
    content: NotRequired[List[DocumentContent]]


class TableHeaderNode(TypedDict):
    """Table header cell node (th)."""
    type: Literal["tableHeader"]
    attrs: NotRequired[TableCellAttrs]
    content: NotRequired[List[DocumentContent]]


# Union type for table cells (both data and header cells)
TableCellOrHeader = Union[TableCellNode, TableHeaderNode]


class TableRowNode(TypedDict):
    """Table row node containing cells or headers."""
    type: Literal["tableRow"]
    attrs: NotRequired[TableRowAttrs]
    content: List[TableCellOrHeader]


class TableNode(TypedDict):
    """Extension table node containing rows."""
    type: Literal["extension-table"]
    attrs: NotRequired[ExtensionTableAttrs]
    content: List[TableRowNode]


# Horizontal rule node
class HorizontalRuleNode(TypedDict):
    """Horizontal rule (divider line)."""
    type: Literal["horizontalRule"]


# Blockquote node
class BlockquoteNode(TypedDict):
    """Blockquote node for quoted text."""
    type: Literal["blockquote"]
    content: NotRequired[List[DocumentContent]]


# Details (collapsible) nodes
class DetailsSummaryNode(TypedDict):
    """Details summary node (always visible header)."""
    type: Literal["detailsSummary"]
    content: NotRequired[List[DocumentContent]]


class DetailsContentNode(TypedDict):
    """Details content node (collapsible body)."""
    type: Literal["detailsContent"]
    content: NotRequired[List[DocumentContent]]


class DetailsNode(TypedDict):
    """Details node (collapsible section with summary and content)."""
    type: Literal["details"]
    content: List[Union[DetailsSummaryNode, DetailsContentNode]]


# Main content type
DocumentNode = Union[ParagraphNode, HeadingNode, BulletListNode, OrderedListNode, ListItemNode, TableNode, HorizontalRuleNode, BlockquoteNode, DetailsNode, ImageBlockNode, FilesBlockNode, MentionNode, DocSiblingsNode, CodeBlockNode]


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
        TextNode: A valid document text node
        
    Example:
        >>> text("Hello World", bold=True)
        {'type': 'text', 'text': 'Hello World', 'marks': [{'type': 'bold'}]}
    """
    # Normalize empty text to a single space to avoid server validation errors
    normalized_content = " " if content == "" else content
    node: TextNode = {"type": "text", "text": normalized_content}
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
        ParagraphNode: A valid document paragraph node
        
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


def _generate_uid() -> str:
    """
    Generate a unique identifier for document elements.
    Format: 12 characters, mix of uppercase, lowercase letters and digits.
    Example: "sEeaN9ddIDsL"
    
    Returns:
        str: A unique identifier string
    """
    import random
    import string
    
    # Generate random string with letters (upper + lower) and digits
    chars = string.ascii_letters + string.digits  # a-z, A-Z, 0-9
    uid = ''.join(random.choice(chars) for _ in range(12))
    return uid


def heading(level: Literal[1, 2, 3, 4, 5, 6], *content: Union[TextNode, str]) -> HeadingNode:
    """
    Create a heading node with automatic UID generation for TOC support.
    
    Args:
        level: Heading level (1-6)
        *content: Text nodes or strings
    
    Returns:
        HeadingNode: A valid document heading node with UID
        
    Example:
        >>> heading(1, "Title")
        {'type': 'heading', 'attrs': {'level': 1, 'uid': '...'}, 'content': [{'type': 'text', 'text': 'Title'}]}
    """
    node: HeadingNode = {
        "type": "heading",
        "attrs": {
            "level": level,
            "uid": _generate_uid()
        }
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
        ListItemNode: A valid document list item node
        
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
        BulletListNode: A valid document bullet list node
        
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
        OrderedListNode: A valid document ordered list node
        
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


def horizontal_rule() -> HorizontalRuleNode:
    """
    Create a horizontal rule (divider line).
    
    Returns:
        HorizontalRuleNode: A horizontal rule node
        
    Example:
        >>> horizontal_rule()
        {'type': 'horizontalRule'}
    """
    return {"type": "horizontalRule"}


def blockquote(*content: Union[ParagraphNode, str]) -> BlockquoteNode:
    """
    Create a blockquote node for quoted text.
    
    Args:
        *content: Paragraphs or strings (strings will be wrapped in paragraphs)
    
    Returns:
        BlockquoteNode: A valid blockquote node
        
    Example:
        >>> blockquote("This is a quote")
        {'type': 'blockquote', 'content': [{'type': 'paragraph', 'content': [{'type': 'text', 'text': 'This is a quote'}]}]}
        
        >>> blockquote(paragraph("First line"), paragraph("Second line"))
        {'type': 'blockquote', 'content': [{'type': 'paragraph', ...}, {'type': 'paragraph', ...}]}
    """
    node: BlockquoteNode = {"type": "blockquote"}
    if content:
        node["content"] = [
            item if isinstance(item, dict) else paragraph(item)
            for item in content
        ]
    return node


def details_summary(*content: Union[TextNode, str]) -> DetailsSummaryNode:
    """
    Create a details summary node (always visible header of collapsible section).
    
    Args:
        *content: Text nodes or strings (strings will be converted to text nodes)
    
    Returns:
        DetailsSummaryNode: A valid details summary node
        
    Example:
        >>> details_summary("Click to expand")
        {'type': 'detailsSummary', 'content': [{'type': 'text', 'text': 'Click to expand'}]}
    """
    node: DetailsSummaryNode = {"type": "detailsSummary"}
    if content:
        node["content"] = [
            item if isinstance(item, dict) else text(item)
            for item in content
        ]
    return node


def details_content(*content: Union[ParagraphNode, str]) -> DetailsContentNode:
    """
    Create a details content node (collapsible body).
    
    Args:
        *content: Paragraphs or strings (strings will be wrapped in paragraphs)
    
    Returns:
        DetailsContentNode: A valid details content node
        
    Example:
        >>> details_content(paragraph("Hidden content"))
        {'type': 'detailsContent', 'content': [{'type': 'paragraph', ...}]}
    """
    node: DetailsContentNode = {"type": "detailsContent"}
    if content:
        node["content"] = [
            item if isinstance(item, dict) else paragraph(item)
            for item in content
        ]
    return node


def details(summary: Union[DetailsSummaryNode, str], *content: Union[DetailsContentNode, ParagraphNode, str]) -> DetailsNode:
    """
    Create a collapsible details section (HTML <details> element).
    
    Args:
        summary: Summary node or string (always visible header)
        *content: Content nodes, paragraphs, or strings (collapsible body)
    
    Returns:
        DetailsNode: A valid details node
        
    Example:
        >>> details("Click to expand", paragraph("Hidden content"))
        {'type': 'details', 'content': [{'type': 'detailsSummary', ...}, {'type': 'detailsContent', ...}]}
        
        >>> details(
        ...     details_summary(text("Additional Info", bold=True)),
        ...     details_content(
        ...         paragraph("Here is more information"),
        ...         paragraph("With multiple paragraphs")
        ...     )
        ... )
    """
    # Create summary node if string provided
    summary_node: DetailsSummaryNode
    if isinstance(summary, str):
        summary_node = details_summary(summary)
    else:
        summary_node = summary
    
    # Create content node
    content_items: List[DocumentContent] = []
    for item in content:
        if isinstance(item, dict):
            # If it's already a DetailsContentNode, use it; otherwise wrap in paragraph
            if item.get("type") == "detailsContent":
                content_items.append(item)
            else:
                content_items.append(item)
        else:
            # String - wrap in paragraph
            content_items.append(paragraph(item))
    
    # Wrap content in detailsContent if not already wrapped
    if content_items and all(item.get("type") != "detailsContent" for item in content_items):
        content_node = details_content(*content_items)
        result_content: List[Union[DetailsSummaryNode, DetailsContentNode]] = [summary_node, content_node]
    else:
        result_content = [summary_node] + [item for item in content_items if item.get("type") == "detailsContent"]
    
    return {"type": "details", "content": result_content}


def table_cell(*content: Union[ParagraphNode, str], colspan: int = 1, rowspan: int = 1) -> TableCellNode:
    """
    Create a table cell node.
    
    Args:
        *content: Paragraphs or strings (strings will be wrapped in paragraphs)
        colspan: Number of columns to span (default: 1)
        rowspan: Number of rows to span (default: 1)
    
    Returns:
        TableCellNode: A valid table cell node
        
    Example:
        >>> table_cell("Cell content")
        {'type': 'tableCell', 'attrs': {'colspan': 1, 'rowspan': 1}, 'content': [...]}
    """
    node: TableCellNode = {
        "type": "tableCell",
        "attrs": {"colspan": colspan, "rowspan": rowspan}
    }
    if content:
        node["content"] = [
            item if isinstance(item, dict) else paragraph(item)
            for item in content
        ]
    return node


def table_header(*content: Union[ParagraphNode, str], colspan: int = 1, rowspan: int = 1) -> TableHeaderNode:
    """
    Create a table header cell node (th).
    
    Args:
        *content: Paragraphs or strings (strings will be wrapped in paragraphs)
        colspan: Number of columns to span (default: 1)
        rowspan: Number of rows to span (default: 1)
    
    Returns:
        TableHeaderNode: A valid table header cell node
        
    Example:
        >>> table_header("Column Name")
        {'type': 'tableHeader', 'attrs': {'colspan': 1, 'rowspan': 1}, 'content': [...]}
    """
    node: TableHeaderNode = {
        "type": "tableHeader",
        "attrs": {"colspan": colspan, "rowspan": rowspan}
    }
    if content:
        node["content"] = [
            item if isinstance(item, dict) else paragraph(item)
            for item in content
        ]
    return node


def table_row(*cells: Union[TableCellNode, TableHeaderNode, str], show_row_numbers: bool = False) -> TableRowNode:
    """
    Create a table row node.
    
    Args:
        *cells: Table cell nodes, table header nodes, or strings (strings will be wrapped in cells)
        show_row_numbers: Show row numbers (default: False)
    
    Returns:
        TableRowNode: A valid table row node
        
    Example:
        >>> table_row("Cell 1", "Cell 2", "Cell 3")
        {'type': 'tableRow', 'attrs': {'showRowNumbers': False}, 'content': [...]}
        
        >>> table_row(table_header("Name"), table_header("Status"))
        {'type': 'tableRow', 'attrs': {'showRowNumbers': False}, 'content': [<headers>]}
    """
    content: List[TableCellOrHeader] = []
    for cell in cells:
        if isinstance(cell, str):
            content.append(table_cell(cell))
        else:
            content.append(cell)
    
    return {
        "type": "tableRow",
        "attrs": {"showRowNumbers": show_row_numbers},
        "content": content
    }


def table(*rows: TableRowNode, show_row_numbers: bool = False) -> TableNode:
    """
    Create an extension-table node.
    
    Args:
        *rows: Table row nodes
        show_row_numbers: Show row numbers (default: False)
    
    Returns:
        TableNode: A valid extension-table node
        
    Example:
        >>> table(
        ...     table_row("Name", "Status"),
        ...     table_row("Task 1", "Done"),
        ...     table_row("Task 2", "In Progress")
        ... )
        {'type': 'extension-table', 'attrs': {'showRowNumbers': False}, 'content': [...]}
    """
    import uuid
    return {
        "type": "extension-table",
        "attrs": {
            "uid": str(uuid.uuid4())[:12].replace('-', ''),
            "showRowNumbers": show_row_numbers
        },
        "content": list(rows)
    }


def mention(item_id: str, kind: Literal["User", "Document", "Task", "Milestone"]) -> MentionNode:
    """
    Create a mention node for referencing users, documents, tasks, or milestones.
    
    Args:
        item_id: The ID of the item to mention
        kind: The type of item ("User", "Document", "Task", or "Milestone")
    
    Returns:
        MentionNode: A valid mention node
        
    Example:
        >>> mention("68fa5e14cdb30e1c96755975", "User")
        {'type': 'custom-mention', 'attrs': {'uid': ..., 'custom': 1, 'inline': True, 'data': {'item': {'id': '68fa5e14cdb30e1c96755975', 'kind': 'User'}}}, 'content': [{'type': 'text', 'text': ' '}]}
        
        >>> mention("68fa67d262f676bcd1bc162f", "Task")
        {'type': 'custom-mention', 'attrs': {..., 'data': {'item': {'id': '68fa67d262f676bcd1bc162f', 'kind': 'Task'}}}, ...}
    """
    import uuid
    return {
        "type": "custom-mention",
        "attrs": {
            "uid": str(uuid.uuid4())[:12].replace('-', ''),
            "custom": 1,
            "inline": True,
            "data": {
                "item": {
                    "id": item_id,
                    "kind": kind
                }
            }
        },
        "content": [{"type": "text", "text": " "}]
    }


def mention_user(member_id: str) -> MentionNode:
    """
    Create a mention node for a user (team member).
    
    Args:
        member_id: The member ID to mention
    
    Returns:
        MentionNode: A valid user mention node
        
    Example:
        >>> mention_user("68fa5e14cdb30e1c96755975")
        {'type': 'custom-mention', 'attrs': {..., 'data': {'item': {'id': '68fa5e14cdb30e1c96755975', 'kind': 'User'}}}, ...}
    """
    return mention(member_id, "User")


def mention_document(document_id: str) -> MentionNode:
    """
    Create a mention node for a document.
    
    Args:
        document_id: The document ID to mention
    
    Returns:
        MentionNode: A valid document mention node
        
    Example:
        >>> mention_document("68fa6c7b62f676bcd1bcecae")
        {'type': 'custom-mention', 'attrs': {..., 'data': {'item': {'id': '68fa6c7b62f676bcd1bcecae', 'kind': 'Document'}}}, ...}
    """
    return mention(document_id, "Document")


def mention_task(task_id: str) -> MentionNode:
    """
    Create a mention node for a task.
    
    Args:
        task_id: The task ID to mention
    
    Returns:
        MentionNode: A valid task mention node
        
    Example:
        >>> mention_task("68fa67d262f676bcd1bc162f")
        {'type': 'custom-mention', 'attrs': {..., 'data': {'item': {'id': '68fa67d262f676bcd1bc162f', 'kind': 'Task'}}}, ...}
    """
    return mention(task_id, "Task")


def mention_milestone(milestone_id: str) -> MentionNode:
    """
    Create a mention node for a milestone.
    
    Args:
        milestone_id: The milestone ID to mention
    
    Returns:
        MentionNode: A valid milestone mention node
        
    Example:
        >>> mention_milestone("68fa650bcdb30e1c9677562e")
        {'type': 'custom-mention', 'attrs': {..., 'data': {'item': {'id': '68fa650bcdb30e1c9677562e', 'kind': 'Milestone'}}}, ...}
    """
    return mention(milestone_id, "Milestone")


def image_block(
    file_id: str,
    src: str,
    file_name: str,
    file_size: int,
    file_type: str = "image/png",
    extension: str = "png",
    width_percent: int = 100,
    dimensions: Optional[List[int]] = None,
    caption: str = "",
    aspect_ratio: Optional[float] = None,
    dominant_color: Optional[dict] = None
) -> ImageBlockNode:
    """
    Create an image block node.
    
    Args:
        file_id: The file ID from upload_file response
        src: The URL of the uploaded image
        file_name: Name of the file
        file_size: Size of the file in bytes
        file_type: MIME type (default: "image/png")
        extension: File extension (default: "png")
        width_percent: Width as percentage (default: 100)
        dimensions: [width, height] of the image
        caption: Optional image caption
        aspect_ratio: Aspect ratio (width/height)
        dominant_color: Dominant color dict with 'color' and 'isDark' keys
    
    Returns:
        ImageBlockNode: A valid image block node
        
    Example:
        >>> # First, upload the image
        >>> uploaded = client.upload_file("path/to/image.png")
        >>> file_id = uploaded.file.id
        >>> 
        >>> # Then create image block
        >>> image_block(
        ...     file_id=file_id,
        ...     src=uploaded.file.url,
        ...     file_name="image.png",
        ...     file_size=12345,
        ...     dimensions=[800, 600]
        ... )
    """
    import uuid
    import json
    
    # Generate unique IDs
    block_uid = str(uuid.uuid4())[:12].replace('-', '')
    image_id = str(uuid.uuid4())[:12].replace('-', '')
    
    # Build image data
    image_data: ImageBlockData = {
        "id": image_id,
        "src": src,
        "fileName": file_name,
        "fileType": file_type,
        "extension": extension,
        "title": file_name,
        "fileSize": file_size,
        "fileId": file_id,
    }
    
    if dimensions:
        image_data["dimensions"] = dimensions
        if len(dimensions) == 2 and dimensions[1] > 0:
            image_data["aspectRatio"] = dimensions[0] / dimensions[1]
    elif aspect_ratio is not None:
        image_data["aspectRatio"] = aspect_ratio
    
    if caption:
        image_data["caption"] = caption
    
    if dominant_color:
        image_data["dominantColor"] = dominant_color
    
    # Create image block node
    return {
        "type": "image-block",
        "attrs": {
            "uid": block_uid,
            "custom": 1,
            "contenteditable": "false",
            "widthPercent": width_percent
        },
        "content": [
            {"type": "text", "text": json.dumps(image_data, ensure_ascii=False)}
        ]
    }


def files_block(*file_items: dict) -> FilesBlockNode:
    """
    Create a files block node with one or more file attachments.
    
    Args:
        *file_items: File item dictionaries with file metadata
    
    Returns:
        FilesBlockNode: A valid files block node
        
    Example:
        >>> # First, upload files
        >>> uploaded1 = client.upload_file("document.pdf")
        >>> uploaded2 = client.upload_file("image.png")
        >>> 
        >>> # Create file items
        >>> file1 = {
        ...     "fileId": uploaded1.file.id,
        ...     "url": uploaded1.file.url,
        ...     "name": "document.pdf",
        ...     "size": uploaded1.file.size,
        ...     "extension": "pdf",
        ...     "type": "Pdf"
        ... }
        >>> 
        >>> file2 = {
        ...     "fileId": uploaded2.file.id,
        ...     "url": uploaded2.file.url,
        ...     "name": "image.png",
        ...     "size": uploaded2.file.size,
        ...     "extension": "png",
        ...     "type": "Image"
        ... }
        >>> 
        >>> # Create files block
        >>> files_block(file1, file2)
    """
    import uuid
    import json
    import time
    
    block_uid = str(uuid.uuid4())[:12].replace('-', '')
    current_timestamp = int(time.time() * 1000)
    
    # Build file items list
    files_list = []
    for item in file_items:
        file_item: FileItem = {
            "id": str(uuid.uuid4())[:12].replace('-', ''),
            "fileId": item["fileId"],
            "createAt": current_timestamp,
            "url": item["url"],
            "extension": item["extension"],
            "name": item["name"],
            "size": item["size"],
            "type": item["type"],
        }
        
        if "dominantColor" in item:
            file_item["dominantColor"] = item["dominantColor"]
        
        files_list.append(file_item)
    
    # Create files block node
    files_data: FilesBlockData = {"files": files_list}
    
    return {
        "type": "files",
        "attrs": {
            "uid": block_uid,
            "custom": 1,
            "contenteditable": "false"
        },
        "content": [
            {"type": "text", "text": json.dumps(files_data, ensure_ascii=False)}
        ]
    }


def toc_block() -> DocSiblingsNode:
    """
    Create a Table of Contents (TOC) block that automatically generates document outline.
    
    Returns:
        DocSiblingsNode: A valid TOC block node
        
    Example:
        >>> from vaiz import toc_block, heading, paragraph
        >>> content = [
        ...     toc_block(),
        ...     heading(1, "Introduction"),
        ...     paragraph("Welcome to our document"),
        ...     heading(2, "Getting Started"),
        ...     paragraph("First steps...")
        ... ]
        >>> client.replace_json_document(document_id, content)
    """
    import uuid
    import json
    
    block_uid = str(uuid.uuid4())[:12].replace('-', '')
    
    toc_data: DocSiblingsData = {"type": "toc"}
    
    return {
        "type": "doc-siblings",
        "attrs": {
            "uid": block_uid,
            "custom": 1,
            "contenteditable": "false"
        },
        "content": [
            {"type": "text", "text": json.dumps(toc_data, ensure_ascii=False)}
        ]
    }


def anchors_block() -> DocSiblingsNode:
    """
    Create an Anchors block that displays related documents and backlinks.
    
    This block automatically shows:
    - Documents linked to this document
    - Documents that link to this document (backlinks)
    - Related documents from the same space
    
    Returns:
        DocSiblingsNode: A valid Anchors block node
        
    Example:
        >>> from vaiz import anchors_block, toc_block, heading, paragraph
        >>> content = [
        ...     toc_block(),
        ...     anchors_block(),
        ...     heading(1, "Main Content"),
        ...     paragraph("Document with TOC and related links")
        ... ]
        >>> client.replace_json_document(document_id, content)
    """
    import uuid
    import json
    
    block_uid = str(uuid.uuid4())[:12].replace('-', '')
    
    anchors_data: DocSiblingsData = {"type": "anchors"}
    
    return {
        "type": "doc-siblings",
        "attrs": {
            "uid": block_uid,
            "custom": 1,
            "contenteditable": "false"
        },
        "content": [
            {"type": "text", "text": json.dumps(anchors_data, ensure_ascii=False)}
        ]
    }


def siblings_block() -> DocSiblingsNode:
    """
    Create a Siblings block that displays sibling documents (documents at the same level).
    
    This block automatically shows documents that are siblings in the document hierarchy:
    - Documents in the same folder/collection
    - Documents at the same level in the structure
    
    Returns:
        DocSiblingsNode: A valid Siblings block node
        
    Example:
        >>> from vaiz import siblings_block, heading, paragraph
        >>> content = [
        ...     siblings_block(),
        ...     heading(1, "Current Document"),
        ...     paragraph("Sibling documents will be shown above")
        ... ]
        >>> client.replace_json_document(document_id, content)
    """
    import uuid
    import json
    
    block_uid = str(uuid.uuid4())[:12].replace('-', '')
    
    siblings_data: DocSiblingsData = {"type": "siblings"}
    
    return {
        "type": "doc-siblings",
        "attrs": {
            "uid": block_uid,
            "custom": 1,
            "contenteditable": "false"
        },
        "content": [
            {"type": "text", "text": json.dumps(siblings_data, ensure_ascii=False)}
        ]
    }


def code_block(code: str = "", language: str = "") -> CodeBlockNode:
    """
    Create a code block for displaying code with syntax highlighting.
    
    Args:
        code: The code content to display
        language: Programming language for syntax highlighting (e.g., "python", "javascript", "typescript", etc.)
    
    Returns:
        CodeBlockNode: A valid code block node
        
    Example:
        >>> from vaiz import code_block, heading, paragraph
        >>> content = [
        ...     heading(1, "Code Example"),
        ...     paragraph("Here's a Python function:"),
        ...     code_block(
        ...         code='def hello():\\n    print("Hello, World!")',
        ...         language="python"
        ...     )
        ... ]
        >>> client.replace_json_document(document_id, content)
        
        >>> # Or create an empty code block
        >>> empty_code = code_block()
    """
    import uuid
    
    block_uid = str(uuid.uuid4())[:12].replace('-', '')
    
    node: CodeBlockNode = {
        "type": "codeBlock",
    }
    
    # Add attrs if we have uid or language
    attrs: CodeBlockAttrs = {"uid": block_uid}
    if language:
        attrs["language"] = language
    node["attrs"] = attrs
    
    # Add content if code is provided
    if code:
        node["content"] = [{"type": "text", "text": code}]
    
    return node


# Convenience exports
__all__ = [
    # Types
    'DocumentNode',
    'TextNode',
    'ParagraphNode',
    'HeadingNode',
    'BulletListNode',
    'OrderedListNode',
    'ListItemNode',
    'TableNode',
    'TableRowNode',
    'TableCellNode',
    'TableHeaderNode',
    'TableCellOrHeader',
    'HorizontalRuleNode',
    'BlockquoteNode',
    'DetailsNode',
    'DetailsSummaryNode',
    'DetailsContentNode',
    'Mark',
    'MentionNode',
    'MentionAttrs',
    'MentionData',
    'MentionItem',
    'ImageBlockNode',
    'ImageBlockAttrs',
    'ImageBlockData',
    'FilesBlockNode',
    'FilesBlockAttrs',
    'FilesBlockData',
    'FileItem',
    'DocSiblingsNode',
    'DocSiblingsAttrs',
    'DocSiblingsData',
    'CodeBlockNode',
    'CodeBlockAttrs',
    
    # Builders
    'text',
    'paragraph',
    'heading',
    'list_item',
    'bullet_list',
    'ordered_list',
    'link_text',
    'horizontal_rule',
    'blockquote',
    'details',
    'details_summary',
    'details_content',
    'table',
    'table_row',
    'table_cell',
    'table_header',
    'mention',
    'mention_user',
    'mention_document',
    'mention_task',
    'mention_milestone',
    'image_block',
    'files_block',
    'toc_block',
    'anchors_block',
    'siblings_block',
    'code_block',
]

