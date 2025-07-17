"""
Main example demonstrating the complete workflow of creating and editing tasks.
"""

from .create_task import create_task
from .edit_task import edit_task
from .get_profile import get_profile
from .get_projects import get_projects
from .get_boards import main as get_boards
from .get_milestones import get_milestones
from .create_task_with_description_and_files import (
    create_task_with_description_and_files,
    create_task_with_multiple_files,
    create_task_with_description_only
)
from .edit_task_with_files import (
    edit_task_with_files,
    edit_task_add_multiple_files,
    edit_task_update_description_only
)
from .post_comment import post_comment_with_html, post_simple_text_comment, post_comment_reply, react_to_comment, add_popular_reactions, get_comments_example, edit_comment_example, edit_comment_with_files_example

def main():
    """Run the complete example workflow."""
    print("="*60)
    print("VAIZ SDK EXAMPLES")
    print("="*60)
    
    print("\n1. Basic data retrieval...")
    print("-" * 40)
    print("Getting profile...")
    get_profile()
    
    print("\nGetting projects...")
    get_projects()
    
    print("\nGetting boards...")
    get_boards()
    
    print("\nGetting milestones...")
    get_milestones()
    
    print("\n" + "="*60)
    print("2. Basic task creation and editing...")
    print("-" * 40)
    task_id = create_task()
    
    if task_id:
        edit_task(task_id)
    
    print("\n" + "="*60)
    print("3. Creating tasks with description and files...")
    print("-" * 40)
    create_task_with_description_and_files()
    
    print("\n" + "="*60)
    print("4. Creating tasks with multiple files...")
    print("-" * 40)
    create_task_with_multiple_files()
    
    print("\n" + "="*60)
    print("5. Creating tasks with description only...")
    print("-" * 40)
    create_task_with_description_only()
    
    print("\n" + "="*60)
    print("6. Editing tasks to add files and description...")
    print("-" * 40)
    edit_task_with_files()
    
    print("\n" + "="*60)
    print("7. Editing tasks to add multiple files...")
    print("-" * 40)
    edit_task_add_multiple_files()
    
    print("\n" + "="*60)
    print("8. Editing tasks to update description only...")
    print("-" * 40)
    edit_task_update_description_only()
    
    print("\n" + "="*60)
    print("9. Posting comments...")
    print("-" * 40)
    post_comment_with_html()
    post_simple_text_comment()
    
    print("\n" + "="*60)
    print("10. Posting comment replies...")
    print("-" * 40)
    post_comment_reply()
    
    print("\n" + "="*60)
    print("11. Adding reactions to comments...")
    print("-" * 40)
    react_to_comment()
    
    print("\n" + "="*60)
    print("12. Adding all popular reactions (simplified API)...")
    print("-" * 40)
    add_popular_reactions()
    
    print("\n" + "="*60)
    print("13. Getting all comments...")
    print("-" * 40)
    get_comments_example()
    
    print("\n" + "="*60)
    print("14. Editing a comment...")
    print("-" * 40)
    edit_comment_example()
    
    print("\n" + "="*60)
    print("15. Editing comment with file operations...")
    print("-" * 40)
    edit_comment_with_files_example()
    
    print("\n" + "="*60)
    print("All examples completed!")
    print("="*60)

if __name__ == "__main__":
    main() 