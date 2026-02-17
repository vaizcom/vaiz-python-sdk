"""
Integration test for embed blocks - creates a real document with various embed types.
"""

from tests.test_config import get_test_client
from vaiz.models import CreateDocumentRequest, Kind
from vaiz import (
    heading, paragraph, text,
    embed_block, EmbedType,
    horizontal_rule, bullet_list
)


def test_create_document_with_embed_blocks():
    """Create a document with various embed block types."""
    client = get_test_client()
    
    # Create Space document
    doc_response = client.create_document(
        CreateDocumentRequest(
            kind=Kind.Space,
            kind_id=client.space_id,
            title="🎬 SDK Test - Embed Blocks Demo",
            index=0
        )
    )
    
    document_id = doc_response.payload.document.id
    assert document_id is not None
    
    # Create content with various embed types
    content = [
        heading(1, "🎬 Embed Blocks Demo"),
        
        paragraph(
            "This document demonstrates all ",
            text("embed block types", bold=True),
            " supported by the Vaiz Python SDK."
        ),
        
        horizontal_rule(),
        
        # YouTube example
        heading(2, "📺 YouTube Video"),
        paragraph("Example of embedded YouTube video:"),
        embed_block(
            url="https://www.youtube.com/watch?v=aY9M6MKXX7Y",
            embed_type=EmbedType.YOUTUBE,
            size="large"
        ),
        
        horizontal_rule(),
        
        # Figma example
        heading(2, "🎨 Figma Design"),
        paragraph("Example of embedded Figma design file:"),
        embed_block(
            url="https://www.figma.com/design/sNL3kbNERHQvP9cqB3tbSG/Figma-File-Template--Community-?node-id=0-1&p=f&t=uIEJLQJDmYT74g6r-0",
            embed_type=EmbedType.FIGMA,
            size="large"
        ),
        
        horizontal_rule(),
        
        # CodeSandbox example
        heading(2, "💻 CodeSandbox"),
        paragraph("Example of embedded CodeSandbox:"),
        embed_block(
            url="https://codesandbox.io/p/sandbox/define-api-post-request-forked-rvbj1",
            embed_type=EmbedType.CODESANDBOX,
            size="large"
        ),
        
        horizontal_rule(),
        
        # GitHub Gist example
        heading(2, "📝 GitHub Gist"),
        paragraph("Example of embedded GitHub Gist:"),
        embed_block(
            url="https://gist.github.com/gdb/b6365e79be6052e7531e7ba6ea8caf23",
            embed_type=EmbedType.GITHUB_GIST
        ),
        
        horizontal_rule(),
        
        # Miro example
        heading(2, "📋 Miro Board"),
        paragraph("Example of embedded Miro board:"),
        embed_block(
            url="https://miro.com/app/board/uXjVO0TkGLc=/",
            embed_type=EmbedType.MIRO,
            size="large"
        ),
        
        horizontal_rule(),
        
        # Generic Iframe example (Google Docs)
        heading(2, "🌐 Google Docs (Iframe)"),
        paragraph("Example of generic iframe embed with Google Docs:"),
        embed_block(
            url="https://docs.google.com/document/d/1nnI3fxDeMlUsmK7CZpQXWcpdfHMgB9XcFjRq18ceiZY/edit?tab=t.0",
            size="medium"
        ),
        
        horizontal_rule(),
        
        # Summary
        heading(2, "📋 Summary"),
        
        paragraph(text("Supported Embed Types:", bold=True)),
        
        bullet_list(
            "YouTube - Video hosting platform (real example)",
            "Figma - Design and prototyping tool (Figma File Template)",
            "CodeSandbox - Online code editor and sandbox (API POST request example)",
            "GitHub Gist - Code snippet hosting",
            "Miro - Collaborative whiteboard (real board)",
            "Iframe - Generic iframe embeds (Google Docs example)"
        ),
        
        horizontal_rule(),
        
        paragraph(
            text("Created with: ", italic=True),
            text("Vaiz Python SDK - embed_block() helper", code=True)
        )
    ]
    
    # Add content to document
    response = client.replace_json_document(document_id, content)
    assert response is not None
    
    # Verify content was saved
    saved = client.get_json_document(document_id)
    saved_blocks = saved.get("default", {}).get("content", [])
    
    assert len(saved_blocks) > 0, "Document should have content blocks"
    
    # Count embed blocks
    embed_blocks = sum(1 for b in saved_blocks if b.get("type") == "embed")
    headings = sum(1 for b in saved_blocks if b.get("type") == "heading")
    
    assert embed_blocks >= 6, f"Should have at least 6 embed blocks, found {embed_blocks}"
    assert headings >= 7, f"Should have at least 7 headings, found {headings}"
    
    # Verify embed block structure
    first_embed = next((b for b in saved_blocks if b.get("type") == "embed"), None)
    assert first_embed is not None, "Should find at least one embed block"
    assert "content" in first_embed, "Embed block should have content"
    
    # Verify embed data is in content
    embed_content = first_embed["content"]
    assert len(embed_content) > 0, "Embed should have content"
    assert embed_content[0]["type"] == "text", "Embed content should be text node"
    
    # Parse embed data JSON
    import json
    embed_data = json.loads(embed_content[0]["text"])
    assert "type" in embed_data, "Embed data should have type"
    assert "url" in embed_data, "Embed data should have url"
    assert "extractedUrl" in embed_data, "Embed data should have extractedUrl"
    
    print(f"\n✅ First embed block structure:")
    print(f"   Type: {embed_data['type']}")
    print(f"   URL: {embed_data['url']}")
    
    print(f"\n✅ Document with embed blocks created successfully!")
    print(f"   Document ID: {document_id}")
    print(f"   Title: {doc_response.payload.document.title}")
    print(f"   Total blocks: {len(saved_blocks)}")
    print(f"   Embed blocks: {embed_blocks}")
    print(f"   Headings: {headings}")
    print(f"\n📍 Location: Space docs section")
    print(f"🔗 Check your Vaiz interface to see all embed blocks:")
    print(f"   - YouTube video")
    print(f"   - Figma design")
    print(f"   - CodeSandbox")
    print(f"   - GitHub Gist")
    print(f"   - Miro board")
    print(f"   - Google Docs (iframe)")


def test_create_tasks_with_embeds_and_move_between_groups():
    """Create tasks with embed blocks in descriptions and move them between board groups."""
    from vaiz.models import CreateTaskRequest, TaskPriority, MoveTaskItem, MoveTasksRequest
    
    client = get_test_client()
    
    # Get boards to find a board to work with
    print("\n📋 Fetching boards...")
    boards_response = client.get_boards()
    assert len(boards_response.boards) > 0, "No boards found in space"
    
    # Use the first board
    test_board = boards_response.boards[0]
    board_id = test_board.id
    print(f"✅ Using board: {test_board.name} (ID: {board_id})")
    
    # Get full board details to access groups
    print("\n📊 Fetching board details with groups...")
    board_response = client.get_board(board_id)
    board = board_response.board
    
    # Check if board has groups
    assert board.groups is not None, f"Board '{board.name}' has no groups"
    assert len(board.groups) >= 2, f"Board '{board.name}' needs at least 2 groups (found {len(board.groups)})"
    
    print(f"✅ Board has {len(board.groups)} groups:")
    for i, group in enumerate(board.groups, 1):
        print(f"   {i}. {group.name} (ID: {group.id})")
    
    # Get first two groups
    group_1 = board.groups[0]
    group_2 = board.groups[1]
    
    # Create tasks with embed blocks in descriptions
    print(f"\n📝 Creating tasks with embed blocks in group '{group_1.name}'...")
    
    task_configs = [
        {
            "name": "🎬 SDK Test - YouTube Embed Task",
            "embed_url": "https://www.youtube.com/watch?v=aY9M6MKXX7Y",
            "embed_type": EmbedType.YOUTUBE,
            "description": "Task with YouTube video embed"
        },
        {
            "name": "🎨 SDK Test - Figma Embed Task",
            "embed_url": "https://www.figma.com/design/sNL3kbNERHQvP9cqB3tbSG/Figma-File-Template",
            "embed_type": EmbedType.FIGMA,
            "description": "Task with Figma design embed"
        },
        {
            "name": "💻 SDK Test - CodeSandbox Embed Task",
            "embed_url": "https://codesandbox.io/p/sandbox/define-api-post-request-forked-rvbj1",
            "embed_type": EmbedType.CODESANDBOX,
            "description": "Task with CodeSandbox embed"
        }
    ]
    
    task_ids = []
    
    for config in task_configs:
        # Create task description with embed block
        description_content = [
            heading(2, config["description"]),
            paragraph(f"This task demonstrates {config['embed_type'].value} embed in task description:"),
            embed_block(
                url=config["embed_url"],
                embed_type=config["embed_type"],
                size="medium"
            ),
            horizontal_rule(),
            paragraph(
                text("Created with: ", italic=True),
                text("Vaiz Python SDK - embed_block() helper", code=True)
            )
        ]
        
        # Create task
        task_request = CreateTaskRequest(
            name=config["name"],
            board=board_id,
            group=group_1.id,
            priority=TaskPriority.General
        )
        
        response = client.create_task(task_request)
        task_id = response.task.id
        task_ids.append(task_id)
        
        # Add embed blocks to task description
        document_id = response.task.document
        client.replace_json_document(document_id, description_content)
        
        print(f"   ✅ Created task: {config['name']} (ID: {task_id})")
    
    print(f"\n✅ Created {len(task_ids)} tasks with embed blocks in group '{group_1.name}'")
    
    # Verify tasks are in group 1
    print(f"\n🔍 Verifying tasks are in group '{group_1.name}'...")
    for i, task_id in enumerate(task_ids, 1):
        task_response = client.get_task(task_id)
        task = task_response.task
        assert task.group == group_1.id, f"Task {i} is not in expected group"
        print(f"   ✅ Task {i} confirmed in group '{group_1.name}'")
    
    # Move tasks to group 2 using moveTasks API
    print(f"\n🔄 Moving tasks to group '{group_2.name}'...")
    move_request = MoveTasksRequest(
        moves=[
            MoveTaskItem(task_id=tid, to_group_id=group_2.id, to_index=i)
            for i, tid in enumerate(task_ids)
        ]
    )
    move_response = client.move_tasks(move_request)
    assert len(move_response.payload.success_ids) == len(task_ids), (
        f"Expected {len(task_ids)} successful moves, got {len(move_response.payload.success_ids)}. "
        f"Failed: {move_response.payload.failed_ids}"
    )
    print(f"   ✅ Moved {len(move_response.payload.success_ids)} tasks to group '{group_2.name}'")
    
    print(f"\n✅ All tasks moved to group '{group_2.name}'")
    
    # Verify tasks are now in group 2
    print(f"\n🔍 Verifying tasks are now in group '{group_2.name}'...")
    for i, task_id in enumerate(task_ids, 1):
        task_response = client.get_task(task_id)
        task = task_response.task
        assert task.group == group_2.id, f"Task {i} is not in group '{group_2.name}'"
        print(f"   ✅ Task {i} confirmed in group '{group_2.name}'")
    
    # Move tasks back to group 1
    print(f"\n🔄 Moving tasks back to group '{group_1.name}'...")
    move_back_request = MoveTasksRequest(
        moves=[
            MoveTaskItem(task_id=tid, to_group_id=group_1.id, to_index=i)
            for i, tid in enumerate(task_ids)
        ]
    )
    move_back_response = client.move_tasks(move_back_request)
    assert len(move_back_response.payload.success_ids) == len(task_ids), (
        f"Expected {len(task_ids)} successful moves back, got {len(move_back_response.payload.success_ids)}. "
        f"Failed: {move_back_response.payload.failed_ids}"
    )
    print(f"   ✅ Moved {len(move_back_response.payload.success_ids)} tasks back to group '{group_1.name}'")
    
    print(f"\n✅ All tasks moved back to group '{group_1.name}'")
    
    # Verify tasks are back in group 1
    print(f"\n🔍 Verifying tasks are back in group '{group_1.name}'...")
    for i, task_id in enumerate(task_ids, 1):
        task_response = client.get_task(task_id)
        task = task_response.task
        assert task.group == group_1.id, f"Task {i} is not back in group '{group_1.name}'"
        print(f"   ✅ Task {i} confirmed in group '{group_1.name}'")
    
    print("\n" + "="*60)
    print("✅ Tasks with embed blocks group movement test completed!")
    print("="*60)
    print(f"\n📊 Summary:")
    print(f"   Board: {board.name}")
    print(f"   Groups tested: {group_1.name} ↔ {group_2.name}")
    print(f"   Tasks created: {len(task_ids)}")
    print(f"   Each task has embed blocks in description")
    print(f"   Movements performed: {len(task_ids) * 2}")
    print(f"\n🔗 Check your Vaiz interface to see the tasks with embeds in '{group_1.name}'")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("Creating document with embed blocks...")
    print("="*60 + "\n")
    
    test_create_document_with_embed_blocks()
    
    print("\n" + "="*60)
    print("Creating tasks with embed blocks and moving between groups...")
    print("="*60 + "\n")
    
    test_create_tasks_with_embeds_and_move_between_groups()
    
    print("\n" + "="*60)
    print("✅ All embed blocks integration tests completed!")
    print("="*60)

