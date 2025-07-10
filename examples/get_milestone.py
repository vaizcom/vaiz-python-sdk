"""
Module demonstrating single milestone retrieval functionality.
"""

from .config import get_client

def get_milestone(milestone_id: str = None):
    """Get a single milestone by ID using the Vaiz SDK."""
    client = get_client()
    
    # If no milestone_id provided, get one from the list
    if not milestone_id:
        print("No milestone ID provided, getting first available milestone...")
        milestones_response = client.get_milestones()
        if not milestones_response.milestones:
            print("No milestones available!")
            return None
        milestone_id = milestones_response.milestones[0].id
        print(f"Using milestone ID: {milestone_id}")
    
    try:
        response = client.get_milestone(milestone_id)
        milestone = response.milestone
        
        print("Milestone retrieved successfully!")
        print(f"Response type: {response.type}")
        print(f"\nMilestone Details:")
        print(f"ID: {milestone.id}")
        print(f"Name: {milestone.name}")
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
        print(f"Editor: {milestone.editor}")
        print(f"Archiver: {milestone.archiver}")
        print(f"Archived At: {milestone.archived_at}")
        print(f"Created At: {milestone.created_at}")
        print(f"Updated At: {milestone.updated_at}")
        print(f"Deleter: {milestone.deleter}")
        print(f"Deleted At: {milestone.deleted_at}")
        
        return milestone.id
    except Exception as e:
        print(f"Error retrieving milestone: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response content: {e.response.text}")
        return None

if __name__ == "__main__":
    get_milestone() 