"""
Module demonstrating milestone retrieval functionality.
"""

from .config import get_client

def get_milestones():
    """Get all milestones using the Vaiz SDK."""
    client = get_client()
    
    try:
        response = client.get_milestones()
        milestones = response.milestones
        
        print("Milestones retrieved successfully!")
        print(f"Found {len(milestones)} milestones:")
        
        for milestone in milestones:
            print(f"\nMilestone: {milestone.name}")
            print(f"ID: {milestone.id}")
            print(f"Description: {milestone.description}")
            print(f"Due Start: {milestone.due_start}")
            print(f"Due End: {milestone.due_end}")
            print(f"Project: {milestone.project}")
            print(f"Board: {milestone.board}")
            print(f"Document: {milestone.document}")
            print(f"Total Tasks: {milestone.total}")
            print(f"Completed Tasks: {milestone.completed}")
            print(f"Progress: {milestone.completed}/{milestone.total} ({(milestone.completed/milestone.total*100):.1f}%)" if milestone.total > 0 else "Progress: 0/0 (0%)")
            print(f"Followers: {milestone.followers}")
            print(f"Creator: {milestone.creator}")
            print(f"Archiver: {milestone.archiver}")
            print(f"Archived At: {milestone.archived_at}")
            print(f"Created At: {milestone.created_at}")
            print(f"Updated At: {milestone.updated_at}")
            print(f"Deleter: {milestone.deleter}")
            print(f"Deleted At: {milestone.deleted_at}")
        
        return [milestone.id for milestone in milestones]
    except Exception as e:
        print(f"Error retrieving milestones: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response content: {e.response.text}")
        return None

if __name__ == "__main__":
    get_milestones() 