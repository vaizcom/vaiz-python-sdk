"""
Vaiz SDK Helper Functions

This module provides convenient helper functions for common operations
with the Vaiz SDK, making it easier to work with complex API requests.
"""

from .custom_fields import (
    # Field creation helpers
    make_text_field,
    make_number_field,
    make_checkbox_field,
    make_date_field,
    make_member_field,
    make_task_relations_field,
    make_select_field,
    make_url_field,
    
    # Select field option helpers
    make_select_option,
    SelectOption,
    add_board_custom_field_select_option,
    remove_board_custom_field_select_option,
    edit_board_custom_field_select_field_option,
    
    # Field editing helpers
    edit_custom_field_name,
    edit_custom_field_description,
    edit_custom_field_visibility,
    edit_custom_field_complete,
    
    # Task relations helpers
    make_task_relation_value,
    add_task_relation,
    remove_task_relation,
    
    # Member field helpers
    make_member_value,
    add_member_to_field,
    remove_member_from_field,
    
    # Date field helpers
    make_date_value,
    make_date_range_value,
    
    # Value formatting helpers
    make_text_value,
    make_number_value,
    make_checkbox_value,
    make_url_value,
)

from .document_structure import (
    # Document structure node builders
    text,
    paragraph,
    heading,
    list_item,
    bullet_list,
    ordered_list,
    link_text,
    horizontal_rule,
    blockquote,
    details,
    details_summary,
    details_content,
    table,
    table_row,
    table_cell,
    table_header,
    mention,
    mention_user,
    mention_document,
    mention_task,
    mention_milestone,
    image_block,
    files_block,
    toc_block,
    anchors_block,
    siblings_block,
    code_block,
    
    # Document structure types
    DocumentNode,
    TextNode,
    ParagraphNode,
    HeadingNode,
    BulletListNode,
    OrderedListNode,
    ListItemNode,
    TableNode,
    TableRowNode,
    TableCellNode,
    TableHeaderNode,
    TableCellOrHeader,
    HorizontalRuleNode,
    BlockquoteNode,
    DetailsNode,
    DetailsSummaryNode,
    DetailsContentNode,
    Mark,
    MentionNode,
    MentionAttrs,
    MentionData,
    MentionItem,
    ImageBlockNode,
    ImageBlockAttrs,
    ImageBlockData,
    FilesBlockNode,
    FilesBlockAttrs,
    FilesBlockData,
    FileItem,
    DocSiblingsNode,
    DocSiblingsAttrs,
    DocSiblingsData,
    CodeBlockNode,
    CodeBlockAttrs,
)

__all__ = [
    # Document structure builders
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
    
    # Document structure types
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
    
    # Custom fields (existing)
    # Field creation helpers
    'make_text_field',
    'make_number_field', 
    'make_checkbox_field',
    'make_date_field',
    'make_member_field',
    'make_task_relations_field',
    'make_select_field',
    'make_url_field',
    
    # Select field option helpers
    'make_select_option',
    'SelectOption',
    'add_board_custom_field_select_option',
    'remove_board_custom_field_select_option',
    'edit_board_custom_field_select_field_option',
    
    # Field editing helpers
    'edit_custom_field_name',
    'edit_custom_field_description',
    'edit_custom_field_visibility',
    'edit_custom_field_complete',
    
    # Task relations helpers
    'make_task_relation_value',
    'add_task_relation',
    'remove_task_relation',
    
    # Member field helpers
    'make_member_value',
    'add_member_to_field',
    'remove_member_from_field',
    
    # Date field helpers
    'make_date_value',
    'make_date_range_value',
    
    # Value formatting helpers
    'make_text_value',
    'make_number_value',
    'make_checkbox_value',
    'make_url_value',
] 