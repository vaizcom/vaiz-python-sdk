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
TEST_API_KEY = 'pat_07691ae71a23c07ef7683aaa69e899b66b68e0d452663dd12cf943ca529a0608'
if not TEST_API_KEY:
    raise ValueError("Please set VAIZ_API_KEY environment variable or create a .env file with VAIZ_API_KEY=your_api_key")

TEST_SPACE_ID = '67443596293eac9ce307e4fc'
if not TEST_SPACE_ID:
    raise ValueError("Please set VAIZ_SPACE_ID environment variable or create a .env file with VAIZ_SPACE_ID=your_space_id")

# Test configuration constants
TEST_PROJECT_ID = '67443596293eac9ce307e50f'
TEST_BOARD_ID = '67443596293eac9ce307e522'
TEST_GROUP_ID = "67443596293eac9ce307e523"
TEST_ASSIGNEE_ID = "67443596293eac9ce307e4fe"

def get_test_client():
    """Initialize and return a VaizClient instance for testing."""
    return VaizClient(
        api_key=TEST_API_KEY,
        space_id=TEST_SPACE_ID,
        verify_ssl=False,
        base_url="https://api.vaiz.local:10000/v4",
    ) 