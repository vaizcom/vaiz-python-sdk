"""
Module demonstrating single project retrieval functionality.
"""

from .config import get_client

def get_project(project_id: str):
    """Get a single project using the Vaiz SDK."""
    client = get_client()
    
    try:
        response = client.get_project(project_id)
        project = response.project
        
        print("Project retrieved successfully!")
        print(f"\nProject: {project.name}")
        print(f"ID: {project.id}")
        print(f"Color: {project.color}")
        print(f"Slug: {project.slug}")
        print(f"Icon: {project.icon}")
        print(f"Creator: {project.creator}")
        print(f"Archiver: {project.archiver}")
        print(f"Archived At: {project.archived_at}")
        print(f"Space: {project.space}")
        print(f"Created At: {project.created_at}")
        print(f"Updated At: {project.updated_at}")
        
        return project.id
    except Exception as e:
        print(f"Error retrieving project: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response content: {e.response.text}")
        return None

if __name__ == "__main__":
    # Get a project ID from get_projects.py first
    from get_projects import get_projects
    project_ids = get_projects()
    if project_ids:
        get_project(project_ids[0]) 