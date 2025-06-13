"""
Module demonstrating how to get task information using the Vaiz SDK.
"""

from vaiz import VaizClient
from vaiz.api.base import VaizSDKError, VaizNotFoundError, VaizAuthError
from examples.config import get_client

def get_task(task_id: str) -> None:
    """Get task information using the Vaiz SDK."""
    client = get_client()
    client.verbose = True  # Enable debug output
    
    try:
        response = client.get_task(task_id)
        print("\n=== Task Retrieved Successfully ===")
        print(f"Response type: {response.type}")
        print(f"Task data: {response.payload}")
        print("================================\n")
        return response

    except VaizNotFoundError as e:
        print("\n=== Task Not Found ===")
        print(f"Error: {str(e)}")
        if e.api_error and e.api_error.meta:
            print(f"Details: {e.api_error.meta.description}")
        print("=====================\n")

    except VaizAuthError as e:
        print("\n=== Authentication Error ===")
        print(f"Error: {str(e)}")
        if e.api_error and e.api_error.meta:
            print(f"Details: {e.api_error.meta.description}")
        print("==========================\n")

    except VaizSDKError as e:
        print("\n=== SDK Error ===")
        print(f"Error: {str(e)}")
        if e.api_error:
            print(f"Error code: {e.api_error.code}")
            print(f"Original type: {e.api_error.original_type}")
        print("================\n")

    except Exception as e:
        print("\n=== Unexpected Error ===")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        print("======================\n")

def main():
    """Main function to demonstrate task retrieval."""
    task_id = "PRJ-21"  # Example task ID
    print(f"Getting information for task with ID: {task_id}")
    get_task(task_id)

if __name__ == "__main__":
    main() 