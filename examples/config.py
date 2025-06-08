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

# Configuration constants
SPACE_ID = os.getenv("VAIZ_SPACE_ID")
BOARD_ID = "68455de3e48da05d905c51e1"
GROUP_ID = "68455de3e48da05d905c51e2"
PROJECT_ID = "676d6758c6ea65cbc1f06d81"
ASSIGNEE_ID = "676d6758c6ea65cbc1f06d70"

def get_client():
    """Initialize and return a VaizClient instance."""
    return VaizClient(
        api_key=API_KEY,
        space_id=SPACE_ID,
        verify_ssl=False,
        base_url="https://api.vaiz.local:10000/v4"
    ) 