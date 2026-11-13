---
sidebar_position: 10
sidebar_label: Markdown Syntax
title: Markdown Syntax — Document Content Dialect | Vaiz Python SDK
description: Reference for the Markdown dialect used to write Vaiz document and task description content, including containers (callout, details, columns) and mentions.
---

# Markdown Syntax

Markdown is the only way to write document content with the SDK. The server converts it to native editor blocks, and `get_markdown_document()` renders the document back into the same dialect, so content survives a read → edit → write round trip.

Use this syntax with [`replace_markdown_document`](./documents#replace_markdown_document) and [`append_markdown_document`](./documents#append_markdown_document). It applies to standalone documents and task descriptions alike.

## Standard Markdown

| Element | Syntax |
|---------|--------|
| Headings | `# H1`, `## H2`, … `###### H6` |
| Bold | `**text**` |
| Italic | `*text*` |
| Strikethrough | `~~text~~` |
| Inline code | `` `code` `` |
| Highlight | `==text==` |
| Link | `[text](https://example.com)` |
| Bullet list | `- item` (also `*` and `+`) |
| Ordered list | `1. item` |
| Checklist | `- [ ] open` and `- [x] done` |
| Table | GFM pipe table with a `\| --- \|` divider line |
| Fenced code | ```` ```python ```` … ```` ``` ```` |
| Horizontal rule | `---` (also `***` and `___`) |
| Blockquote | `> quoted text` |
| Image | `![alt](https://example.com/image.png)` on its own line |
| Diagram | ```` ```mermaid ```` … ```` ``` ```` |
| Inline equation | `$E=mc^2$` |
| Block equation | `$$\int_0^1 x\,dx$$` on its own line |

Always put a language after the opening code fence: a fence without one is assigned a default language by the editor.

Inline HTML tags are supported for formats Markdown has no syntax for: `<ins>underline</ins>`, `<sub>subscript</sub>`, `<sup>superscript</sup>`.

```python
client.replace_markdown_document(
    document_id,
    """# Release Report

Stats for ==current== sprint, written with **bold**, *italic* and `code`.

- [x] Deploy API
- [ ] Deploy app

| Metric | Value |
| --- | --- |
| Tasks done | **42** |
| Bugs fixed | `17` |

```python
print("hello")
```

> Numbers are preliminary

![Chart](https://example.com/chart.png)
""",
)
```

### Lists and nesting

Nest bullet, ordered and checklist items by indenting the child by **4 spaces** (a tab counts as one level; 2-space indents also work for checklists):

```markdown
- level 1
    - level 2
        - level 3

1. first
    1. nested
2. second

- [x] Phase 1
    - [x] Subtask
    - [ ] Another subtask
```

### Tables

Tables use GFM syntax. The first row becomes the header row. Cells support inline formatting (bold, italic, strikethrough, code, links) and mentions. Column alignment markers (`:---`, `---:`) are accepted but not stored.

```markdown
| Feature | Status |
| --- | --- |
| **Tables** | `done` |
| [Docs](https://vaiz.com) | ~~todo~~ |
```

### Images

An image is converted to an image block only when it is the only thing on its line. Inline `data:` images are not supported - upload the file first (see [Files](../guides/files)) and use its URL.

## Containers

Containers wrap other content between a start line `:::name{attributes}` and a closing `:::` line. Attribute values are double-quoted strings (no escaping); a bare key is a flag.

### Callout

```markdown
:::callout{icon="Light" color="blue"}
Plain callout text.
:::
```

- `icon` - editor icon name (default `Info`)
- `color` - editor color name, such as `blue` or `red` (neutral gray when omitted)

Callout content is plain text: inline Markdown markers such as `**bold**` are stripped, keeping the text.

### Details

A collapsible block. `summary` is the always-visible title; the `open` flag makes it expanded (collapsed by default). The body can hold any Markdown, including nested containers.

```markdown
:::details{summary="Click to expand" open}
Hidden **content** with a list:

- one
- two
:::
```

### Columns

A 2-, 3- or 4-column layout. Columns are separated by `::col` lines; extra columns beyond four are dropped, and a single column is padded to two. Each column can hold any Markdown.

```markdown
:::columns
::col
### Left
Left column text.
::col
### Right
Right column text.
:::
```

Containers can be nested; each `:::name` line opens a level and every bare `:::` closes the innermost one. A container that is never closed consumes the rest of the document.

## Mentions

Mentions reference workspace entities with `@[Label](kind:id)`:

| Kind | Syntax |
|------|--------|
| User (member) | `@[Name](user:<memberId>)` |
| Task | `@[Title](task:<id>)` |
| Document | `@[Title](document:<id>)` |
| Milestone | `@[Title](milestone:<id>)` |
| Project | `@[Name](project:<id>)` |
| Board | `@[Name](board:<id>)` |

`kind` must be one of the values above and `id` may contain letters, digits, `_` and `-`. For users, `<memberId>` is the member ID (for example `client.get_profile().profile.member_id`), not the user ID.

The label is cosmetic: only the kind and ID are stored, and the editor shows the live name of the entity. When you read a document back, labels are replaced with the kind (`@[task](task:<id>)`).

```python
member_id = client.get_profile().profile.member_id

client.replace_markdown_document(
    task.document,
    f"Assigned to @[Me](user:{member_id}), see @[Spec](document:{spec_id}).",
)
```

## Reading Content Back

`get_markdown_document()` returns the same dialect, with a few normalizations to be aware of:

- Special characters in text are escaped (`INITIAL_MARKER` is returned as `INITIAL\_MARKER`).
- Mention labels become the entity kind, as described above.
- Table alignment markers are normalized to `| --- |`.
- Video blocks are exported as links (`[title](url)`) and file blocks as `- [name](url)` list items.

## See Also

- [Documents Guide](../guides/documents) - Usage examples
- [Documents API Reference](./documents) - Methods and models
