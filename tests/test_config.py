"""
Test configuration module for Vaiz SDK tests.
Contains test credentials and helper functions for testing.
"""

import os
from dotenv import load_dotenv
from vaiz import VaizClient

# Load environment variables from .env file
load_dotenv()

# Test credentials
TEST_API_KEY = os.getenv("VAIZ_API_KEY")
if not TEST_API_KEY:
    raise ValueError("Please set VAIZ_API_KEY environment variable or create a .env file with VAIZ_API_KEY=your_api_key")

TEST_SPACE_ID = os.getenv("VAIZ_SPACE_ID")
if not TEST_SPACE_ID:
    raise ValueError("Please set VAIZ_SPACE_ID environment variable or create a .env file with VAIZ_SPACE_ID=your_space_id")

# Test configuration constants
TEST_PROJECT_ID = os.getenv("VAIZ_PROJECT_ID")
TEST_BOARD_ID = os.getenv("VAIZ_BOARD_ID")
TEST_GROUP_ID = os.getenv("VAIZ_GROUP_ID")
TEST_ASSIGNEE_ID = os.getenv("VAIZ_ASSIGNEE_ID")

def get_test_client():
    """Initialize and return a VaizClient instance for testing."""
    return VaizClient(
        api_key=TEST_API_KEY,
        space_id=TEST_SPACE_ID,
        verify_ssl=False,
        base_url="https://api.vaiz.local:10000/v4",
    ) 