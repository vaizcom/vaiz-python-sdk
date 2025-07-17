"""
Examples for working with files in comments.
Demonstrates uploading files and attaching them to comments.
"""

import os
from vaiz.models import CommentReactionType
from .config import get_client
from .test_helpers import get_or_create_document_id


def upload_single_file_comment():
    """Upload a single file and attach it to a comment."""
    client = get_client()
    document_id = get_or_create_document_id()
    
    try:
        print("=== SINGLE FILE COMMENT EXAMPLE ===")
        
        # Upload an image file
        file_path = os.path.join("assets", "example.png")
        if not os.path.exists(file_path):
            print(f"❌ File not found: {file_path}")
            return
        
        print(f"📤 Uploading file: {file_path}")
        upload_response = client.upload_file(file_path)
        file_id = upload_response.file.id
        
        print(f"✅ File uploaded successfully!")
        print(f"   - File ID: {file_id}")
        print(f"   - Original name: {upload_response.file.original_name}")
        print(f"   - Size: {upload_response.file.size} bytes")
        
        # Create comment with the uploaded file
        comment_response = client.post_comment(
            document_id=document_id,
            content="<p>Check out this <strong>awesome image</strong> I uploaded! 📸</p>",
            file_ids=[file_id]
        )
        
        comment = comment_response.comment
        print(f"\n💬 Comment created with file attachment!")
        print(f"   - Comment ID: {comment.id}")
        print(f"   - Content: {comment.content}")
        print(f"   - Attached files: {len(comment.files)}")
        print(f"   - File IDs: {[f.id for f in comment.files]}")
        print(f"   - File names: {[f.original_name for f in comment.files]}")
        
        return comment.id, file_id
        
    except Exception as e:
        print(f"❌ Error: {e}")


def upload_multiple_files_comment():
    """Upload multiple files (image, video, document) and attach them to a comment."""
    client = get_client()
    document_id = get_or_create_document_id()
    
    try:
        print("\n=== MULTIPLE FILES COMMENT EXAMPLE ===")
        
        # Define files to upload with descriptions
        files_to_upload = [
            ("assets/example.png", "🖼️ Image", "PNG image file"),
            ("assets/example.mp4", "🎥 Video", "MP4 video file"),
            ("assets/example.pdf", "📄 Document", "PDF document file")
        ]
        
        uploaded_files = []
        
        # Upload each file
        for file_path, emoji_desc, description in files_to_upload:
            if os.path.exists(file_path):
                print(f"\n📤 Uploading {emoji_desc}: {file_path}")
                upload_response = client.upload_file(file_path)
                uploaded_files.append({
                    'id': upload_response.file.id,
                    'name': upload_response.file.original_name,
                    'size': upload_response.file.size,
                    'description': description,
                    'emoji': emoji_desc
                })
                print(f"   ✅ Uploaded: {upload_response.file.id}")
                print(f"   📝 Name: {upload_response.file.original_name}")
                print(f"   📏 Size: {upload_response.file.size} bytes")
            else:
                print(f"   ⚠️ File not found: {file_path}")
        
        if not uploaded_files:
            print("❌ No files were uploaded")
            return
        
        # Create comment with all uploaded files
        file_ids = [f['id'] for f in uploaded_files]
        file_descriptions = [f['emoji'] for f in uploaded_files]
        
        comment_content = f"""
        <p>📎 <strong>Multi-media comment</strong> with {len(uploaded_files)} attachments:</p>
        <ul>
            {"".join(f"<li>{desc}</li>" for desc in file_descriptions)}
        </ul>
        <p>Perfect for sharing different types of content! 🚀</p>
        """
        
        comment_response = client.post_comment(
            document_id=document_id,
            content=comment_content,
            file_ids=file_ids
        )
        
        comment = comment_response.comment
        print(f"\n💬 Multi-file comment created!")
        print(f"   - Comment ID: {comment.id}")
        print(f"   - Attached files: {len(comment.files)}")
        print(f"   - File IDs: {[f.id for f in comment.files]}")
        print(f"   - File names: {[f.original_name for f in comment.files]}")
        
        # Display file details
        print(f"\n📋 File details:")
        for i, file_info in enumerate(uploaded_files, 1):
            print(f"   {i}. {file_info['emoji']} {file_info['name']} ({file_info['size']} bytes)")
        
        return comment.id, file_ids
        
    except Exception as e:
        print(f"❌ Error: {e}")


def edit_comment_add_files():
    """Create a comment without files, then edit it to add files."""
    client = get_client()
    document_id = get_or_create_document_id()
    
    try:
        print("\n=== EDIT COMMENT: ADD FILES EXAMPLE ===")
        
        # 1. Create a comment without files
        original_response = client.post_comment(
            document_id=document_id,
            content="<p>📝 This comment will be <strong>enhanced</strong> with file attachments!</p>"
        )
        
        original_comment = original_response.comment
        print(f"📄 Original comment created (no files): {original_comment.id}")
        print(f"   Content: {original_comment.content}")
        print(f"   Files: {len(original_comment.files)}")
        
        # 2. Upload a file to add
        file_path = os.path.join("assets", "example.pdf")
        if not os.path.exists(file_path):
            print(f"❌ File not found: {file_path}")
            return
        
        print(f"\n📤 Uploading file to add: {file_path}")
        upload_response = client.upload_file(file_path)
        file_id = upload_response.file.id
        print(f"   ✅ File uploaded: {file_id}")
        print(f"   📝 Name: {upload_response.file.original_name}")
        
        # 3. Edit comment to add the file
        edit_response = client.edit_comment(
            comment_id=original_comment.id,
            content="<p>📝 <strong>UPDATED:</strong> This comment now has a file attachment! 📎</p>",
            add_file_ids=[file_id],
            order_file_ids=[file_id]
        )
        
        edited_comment = edit_response.comment
        print(f"\n✏️ Comment edited successfully!")
        print(f"   - Comment ID: {edited_comment.id}")
        print(f"   - New content: {edited_comment.content}")
        print(f"   - Files after edit: {len(edited_comment.files)}")
        print(f"   - File IDs: {[f.id for f in edited_comment.files]}")
        print(f"   - Edited at: {edited_comment.edited_at}")
        
        return edited_comment.id
        
    except Exception as e:
        print(f"❌ Error: {e}")


def edit_comment_manage_files():
    """Demonstrate complex file management: add, reorder, and remove files."""
    client = get_client()
    document_id = get_or_create_document_id()
    
    try:
        print("\n=== EDIT COMMENT: COMPLEX FILE MANAGEMENT ===")
        
        # 1. Upload initial files
        files_to_upload = ["assets/example.png", "assets/example.pdf"]
        initial_file_ids = []
        
        print("📤 Uploading initial files...")
        for file_path in files_to_upload:
            if os.path.exists(file_path):
                upload_response = client.upload_file(file_path)
                initial_file_ids.append(upload_response.file.id)
                print(f"   ✅ Uploaded: {upload_response.file.original_name} ({upload_response.file.id})")
        
        if len(initial_file_ids) < 2:
            print("❌ Need at least 2 files for this example")
            return
        
        # 2. Create comment with initial files
        comment_response = client.post_comment(
            document_id=document_id,
            content="<p>🗂️ File management demo with initial files</p>",
            file_ids=initial_file_ids
        )
        
        comment_id = comment_response.comment.id
        print(f"\n💬 Initial comment created: {comment_id}")
        print(f"   Initial files: {[f.id for f in comment_response.comment.files]}")
        print(f"   File names: {[f.original_name for f in comment_response.comment.files]}")
        
        # 3. Add a third file if available
        third_file_path = os.path.join("assets", "example.mp4")
        if os.path.exists(third_file_path):
            print(f"\n📤 Adding third file: {third_file_path}")
            upload_response = client.upload_file(third_file_path)
            third_file_id = upload_response.file.id
            print(f"   ✅ Uploaded: {third_file_id}")
            
            # Edit to add the third file
            edit_response = client.edit_comment(
                comment_id=comment_id,
                content="<p>🗂️ <strong>STEP 1:</strong> Added a third file (video)</p>",
                add_file_ids=[third_file_id],
                order_file_ids=initial_file_ids + [third_file_id]
            )
            print(f"   ✏️ Added third file: {[f.id for f in edit_response.comment.files]}")
            
            # 4. Reorder files (reverse order)
            all_files = edit_response.comment.files
            reversed_file_ids = [f.id for f in reversed(all_files)]
            
            edit_response = client.edit_comment(
                comment_id=comment_id,
                content="<p>🗂️ <strong>STEP 2:</strong> Reordered files (reversed)</p>",
                order_file_ids=reversed_file_ids
            )
            print(f"   🔄 Reordered files: {[f.id for f in edit_response.comment.files]}")
            
            # 5. Remove the middle file
            current_file_ids = [f.id for f in edit_response.comment.files]
            file_to_remove = current_file_ids[1]  # Middle file
            remaining_files = [f for f in current_file_ids if f != file_to_remove]
            
            edit_response = client.edit_comment(
                comment_id=comment_id,
                content="<p>🗂️ <strong>STEP 3:</strong> Removed middle file</p>",
                remove_file_ids=[file_to_remove],
                order_file_ids=remaining_files
            )
            print(f"   🗑️ Removed file: {file_to_remove}")
            print(f"   📁 Final files: {[f.id for f in edit_response.comment.files]}")
        
        print(f"\n🎉 File management demonstration completed!")
        
    except Exception as e:
        print(f"❌ Error: {e}")


def complete_file_workflow():
    """Demonstrate a complete workflow with files: upload -> comment -> react -> edit -> delete."""
    client = get_client()
    document_id = get_or_create_document_id()
    
    try:
        print("\n=== COMPLETE FILE WORKFLOW ===")
        
        # 1. Upload file
        file_path = os.path.join("assets", "example.png")
        if not os.path.exists(file_path):
            print(f"❌ File not found: {file_path}")
            return
        
        print("1️⃣ Uploading file...")
        upload_response = client.upload_file(file_path)
        file_id = upload_response.file.id
        print(f"   ✅ Uploaded: {upload_response.file.original_name}")
        
        # 2. Create comment with file
        print("2️⃣ Creating comment with file...")
        comment_response = client.post_comment(
            document_id=document_id,
            content="<p>📸 <strong>Workflow demo</strong> - beautiful image attached!</p>",
            file_ids=[file_id]
        )
        comment_id = comment_response.comment.id
        print(f"   💬 Comment created: {comment_id}")
        
        # 3. Add reaction to the comment
        print("3️⃣ Adding reaction...")
        reaction_response = client.add_reaction(
            comment_id=comment_id,
            reaction=CommentReactionType.HEART
        )
        print(f"   ❤️ Added heart reaction")
        
        # 4. Edit comment content (keep file)
        print("4️⃣ Editing comment content...")
        edit_response = client.edit_comment(
            comment_id=comment_id,
            content="<p>📸 <strong>UPDATED:</strong> Enhanced workflow demo with even better description!</p>",
            order_file_ids=[file_id]  # Keep the file
        )
        print(f"   ✏️ Content updated, file preserved")
        
        # 5. Verify in comments list
        print("5️⃣ Verifying in comments list...")
        comments_response = client.get_comments(document_id=document_id)
        
        our_comment = None
        for comment in comments_response.comments:
            if comment.id == comment_id:
                our_comment = comment
                break
        
        if our_comment:
            print(f"   📋 Found comment in list:")
            print(f"      - Files: {len(our_comment.files)}")
            print(f"      - Reactions: {len(our_comment.reactions)}")
            print(f"      - Edited: {our_comment.edited_at is not None}")
        
        # 6. Delete comment
        print("6️⃣ Deleting comment...")
        delete_response = client.delete_comment(comment_id=comment_id)
        print(f"   🗑️ Comment deleted at: {delete_response.comment.deleted_at}")
        print(f"   📝 Content cleared: '{delete_response.comment.content}'")
        
        print(f"\n🎉 Complete file workflow finished!")
        print("📊 Summary: Upload ✅ Comment ✅ React ✅ Edit ✅ Verify ✅ Delete ✅")
        
    except Exception as e:
        print(f"❌ Error: {e}")


def main():
    """Run all file-related comment examples."""
    print("🗃️ " + "="*60)
    print("FILE ATTACHMENT EXAMPLES FOR COMMENTS")
    print("="*60)
    
    upload_single_file_comment()
    upload_multiple_files_comment()
    edit_comment_add_files()
    edit_comment_manage_files()
    complete_file_workflow()
    
    print("\n🎉 All file examples completed!")


if __name__ == "__main__":
    main() 