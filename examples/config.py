"""
Configuration module for Vaiz SDK examples.
Handles environment variables and client initialization.
"""

import os
from dotenv import load_dotenv
from vaiz import VaizClient

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variable
API_KEY = os.getenv("VAIZ_API_KEY")
if not API_KEY:
    raise ValueError("Please set VAIZ_API_KEY environment variable or create a .env file with VAIZ_API_KEY=your_api_key")

SPACE_ID = os.getenv("VAIZ_SPACE_ID")
if not SPACE_ID:
    raise ValueError("Please set VAIZ_SPACE_ID environment variable or create a .env file with VAIZ_SPACE_ID=your_space_id")


# Configuration constants
PROJECT_ID = os.getenv("VAIZ_PROJECT_ID")
BOARD_ID = os.getenv("VAIZ_BOARD_ID")
GROUP_ID = os.getenv("VAIZ_GROUP_ID")
ASSIGNEE_ID = os.getenv("VAIZ_ASSIGNEE_ID")

def get_client():
    """Initialize and return a VaizClient instance."""
    return VaizClient(
        api_key=API_KEY,
        space_id=SPACE_ID,
        verify_ssl=False,
        base_url="https://api.vaiz.local:10000/v4"
    ) 