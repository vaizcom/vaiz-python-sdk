"""
Module demonstrating project retrieval functionality.
"""

from .config import get_client

def get_projects():
    """Get all projects using the Vaiz SDK."""
    client = get_client()
    
    try:
        response = client.get_projects()
        projects = response.projects
        
        print("Projects retrieved successfully!")
        print(f"Found {len(projects)} projects:")
        
        for project in projects:
            print(f"\nProject: {project.name}")
            print(f"ID: {project._id}")
            print(f"Color: {project.color}")
            print(f"Slug: {project.slug}")
            print(f"Icon: {project.icon}")
            print(f"Creator: {project.creator}")
            print(f"Archiver: {project.archiver}")
            print(f"Archived At: {project.archived_at}")
            print(f"Space: {project.space}")
            print(f"Created At: {project.created_at}")
            print(f"Updated At: {project.updated_at}")
        
        return [project._id for project in projects]
    except Exception as e:
        print(f"Error retrieving projects: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response content: {e.response.text}")
        return None

if __name__ == "__main__":
    get_projects() 