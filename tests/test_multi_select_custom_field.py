"""
Test module for multi-select custom field functionality.

This module tests the complete workflow of:
1. Creating a custom field of type Select
2. Adding multiple options to the field
3. Creating a task with multiple selected values
4. Verifying the task contains the correct custom field values
"""

import pytest
import time
from typing import List
from tests.test_config import get_test_client, TEST_BOARD_ID, TEST_PROJECT_ID, TEST_GROUP_ID
from vaiz.models import (
    CreateBoardCustomFieldRequest,
    EditBoardCustomFieldRequest, 
    CustomFieldType,
    CreateTaskRequest,
    CustomField,
    TaskPriority
)
from vaiz.models.enums import Color, Icon


class TestMultiSelectCustomField:
    """Test class for multi-select custom field functionality."""
    
    @pytest.fixture
    def country_options(self):
        """Fixture providing test country options."""
        import hashlib
        
        def generate_option_id(title):
            """Generate deterministic ID for option."""
            return hashlib.md5(title.encode()).hexdigest()[:24]
        
        return [
            {"_id": generate_option_id("United States"), "title": "United States", "color": Color.Red, "icon": Icon.User},
            {"_id": generate_option_id("Germany"), "title": "Germany", "color": Color.Blue, "icon": Icon.Circle},
            {"_id": generate_option_id("France"), "title": "France", "color": Color.Violet, "icon": Icon.Heart},
            {"_id": generate_option_id("Japan"), "title": "Japan", "color": Color.Green, "icon": Icon.Star},
            {"_id": generate_option_id("Brazil"), "title": "Brazil", "color": Color.Gold, "icon": Icon.Sun},
            {"_id": generate_option_id("India"), "title": "India", "color": Color.Orange, "icon": Icon.Fire},
            {"_id": generate_option_id("Canada"), "title": "Canada", "color": Color.Mint, "icon": Icon.Snow},
            {"_id": generate_option_id("Australia"), "title": "Australia", "color": Color.Magenta, "icon": Icon.Triangle}
        ]
    
    def test_create_select_custom_field_with_options(self, country_options):
        """Test creating a custom field of type Select and adding options."""
        client = get_test_client()
        board_id = TEST_BOARD_ID
        
        # Step 1: Create the custom field
        create_request = CreateBoardCustomFieldRequest(
            name="Test Countries Field",
            type=CustomFieldType.SELECT,
            board_id=board_id,
            description="Test field for country selection",
            hidden=False,
            options=[]
        )
        
        response = client.create_board_custom_field(create_request)
        assert response is not None
        assert response.custom_field is not None
        
        custom_field = response.custom_field
        assert custom_field.name == "Test Countries Field"
        assert custom_field.type == CustomFieldType.SELECT
        assert custom_field.description == "Test field for country selection"
        assert custom_field.hidden is False
        
        field_id = custom_field.id
        assert field_id is not None
        
        # Step 2: Add options to the custom field
        edit_request = EditBoardCustomFieldRequest(
            field_id=field_id,
            board_id=board_id,
            options=country_options
        )
        
        edit_response = client.edit_board_custom_field(edit_request)
        assert edit_response is not None
        assert edit_response.custom_field is not None
        
        updated_field = edit_response.custom_field
        assert updated_field.options is not None
        assert len(updated_field.options) == len(country_options)
        
        # Verify options were added correctly
        for i, option in enumerate(updated_field.options):
            expected_option = country_options[i]
            assert option["title"] == expected_option["title"]
            assert option["_id"] == expected_option["_id"]
            assert option["color"] == expected_option["color"]
            assert option["icon"] == expected_option["icon"]
        assert field_id is not None
    
    def test_create_task_with_single_select_value(self):
        """Test creating a task with a single selected value in custom field."""
        client = get_test_client()
        board_id = TEST_BOARD_ID
        project_id = TEST_PROJECT_ID
        group_id = TEST_GROUP_ID
        
        # First create a custom field
        import hashlib
        
        def generate_option_id(title):
            return hashlib.md5(title.encode()).hexdigest()[:24]
        
        # Create select field using helper functions
        from vaiz.helpers import make_select_field, make_select_option
        
        test_option = make_select_option("Test Country", Color.Red, Icon.User)
        select_field_request = make_select_field(
            name="Test Countries Single",
            board_id=board_id,
            options=[test_option],
            description="Test select field for single selection"
        )
        
        field_response = client.create_board_custom_field(select_field_request)
        field_id = field_response.custom_field.id
        
        # Create custom field with single value
        custom_field = CustomField(
            id=field_id,
            value=test_option.id  # Single value as string (option ID)
        )
        
        # Create the task
        task_request = CreateTaskRequest(
            name="Single Select Test Task",
            group=group_id,
            board=board_id,
            project=project_id,
            description="Test task with single select custom field",
            priority=TaskPriority.Medium,
            custom_fields=[custom_field]
        )
        
        task_response = client.create_task(task_request)
        assert task_response is not None
        assert task_response.task is not None
        
        task = task_response.task
        assert task.name == "Single Select Test Task"
        assert len(task.custom_fields) >= 1
        
        # Find our custom field in the task
        found_field = None
        for cf in task.custom_fields:
            if cf.id == field_id:
                found_field = cf
                break
        
        assert found_field is not None, f"Custom field {field_id} not found in task"
        assert found_field.value == test_option.id
        assert task.id is not None
    
    def test_create_task_with_multi_select_values(self, country_options):
        """Test creating a task with multiple selected values in custom field."""
        client = get_test_client()
        board_id = TEST_BOARD_ID
        project_id = TEST_PROJECT_ID
        group_id = TEST_GROUP_ID
        
        # First create a custom field with country options using helper functions
        from vaiz.helpers import make_select_field
        
        select_field_request = make_select_field(
            name="Test Countries Multi",
            board_id=board_id,
            options=country_options,
            description="Test select field for multi selection"
        )
        
        field_response = client.create_board_custom_field(select_field_request)
        field_id = field_response.custom_field.id
        
        # Selected countries (multiple values) - using option IDs
        selected_country_names = ["United States", "Germany", "Japan"]
        
        # Get the _id values for selected countries
        selected_country_ids = []
        for option in country_options:
            if option["title"] in selected_country_names:
                selected_country_ids.append(option["_id"])
        
        # Create custom field with multiple values
        custom_field = CustomField(
            id=field_id,
            value=selected_country_ids  # List of option IDs for multi-select
        )
        
        # Create the task
        task_request = CreateTaskRequest(
            name="Multi Select Test Task",
            group=group_id,
            board=board_id,
            project=project_id,
            description="Test task with multi-select custom field",
            priority=TaskPriority.High,
            custom_fields=[custom_field]
        )
        
        task_response = client.create_task(task_request)
        assert task_response is not None
        assert task_response.task is not None
        
        task = task_response.task
        assert task.name == "Multi Select Test Task"
        assert task.priority == TaskPriority.High
        assert len(task.custom_fields) >= 1
        
        # Find our custom field in the task
        found_field = None
        for cf in task.custom_fields:
            if cf.id == field_id:
                found_field = cf
                break
        
        assert found_field is not None, f"Custom field {field_id} not found in task"
        assert isinstance(found_field.value, list), f"Expected list, got {type(found_field.value)}"
        assert len(found_field.value) == 3
        assert set(found_field.value) == set(selected_country_ids)
        assert task.id is not None
        assert field_id is not None
    
    def test_retrieve_task_with_multi_select_values(self, country_options):
        """Test retrieving a task and verifying multi-select custom field values."""
        from vaiz.helpers import make_select_field
        
        client = get_test_client()
        board_id = TEST_BOARD_ID
        project_id = TEST_PROJECT_ID
        group_id = TEST_GROUP_ID
        
        # Create select field with country options
        select_field_request = make_select_field(
            name="Test Countries Retrieve",
            board_id=board_id,
            options=country_options,
            description="Test select field for retrieval test"
        )
        
        field_response = client.create_board_custom_field(select_field_request)
        field_id = field_response.custom_field.id
        
        # Create task with multi-select values
        selected_country_names = ["United States", "Germany", "Japan"]
        selected_country_ids = []
        for option in country_options:
            if option["title"] in selected_country_names:
                selected_country_ids.append(option["_id"])
        
        custom_field = CustomField(
            id=field_id,
            value=selected_country_ids
        )
        
        task_request = CreateTaskRequest(
            name="Multi Select Retrieve Test Task",
            group=group_id,
            board=board_id,
            project=project_id,
            description="Test task for retrieval with multi-select custom field",
            priority=TaskPriority.Medium,
            custom_fields=[custom_field]
        )
        
        task_response = client.create_task(task_request)
        task_id = task_response.task.hrid  # Use hrid for get_task
        
        # Retrieve the task
        task_response = client.get_task(task_id)
        assert task_response is not None
        assert task_response.task is not None
        
        task = task_response.task
        assert task.hrid == task_id
        assert task.name == "Multi Select Retrieve Test Task"
        
        # Find our custom field
        found_field = None
        for cf in task.custom_fields:
            if cf.id == field_id:
                found_field = cf
                break
        
        assert found_field is not None
        assert isinstance(found_field.value, list)
        assert len(found_field.value) == 3
        
        # Check that the values match our expected option IDs
        expected_country_names = ["United States", "Germany", "Japan"]
        expected_ids = []
        for option in country_options:
            if option["title"] in expected_country_names:
                expected_ids.append(option["_id"])
        
        for expected_id in expected_ids:
            assert expected_id in found_field.value
    
    def test_complete_workflow_multi_select_custom_field(self):
        """Test the complete workflow from field creation to task verification."""
        client = get_test_client()
        board_id = TEST_BOARD_ID
        project_id = TEST_PROJECT_ID
        group_id = TEST_GROUP_ID
        
        # Step 1: Create custom field
        create_request = CreateBoardCustomFieldRequest(
            name="Test Complete Workflow",
            type=CustomFieldType.SELECT,
            board_id=board_id,
            description="Complete workflow test field",
            hidden=False,
            options=[]
        )
        
        response = client.create_board_custom_field(create_request)
        field_id = response.custom_field.id
        
        # Step 2: Add options
        import hashlib
        
        def generate_option_id(title):
            return hashlib.md5(title.encode()).hexdigest()[:24]
        
        options = [
            {"_id": generate_option_id("Option A"), "title": "Option A", "color": Color.Red, "icon": Icon.Checkbox},
            {"_id": generate_option_id("Option B"), "title": "Option B", "color": Color.Green, "icon": Icon.Circle},
            {"_id": generate_option_id("Option C"), "title": "Option C", "color": Color.Blue, "icon": Icon.Square}
        ]
        
        edit_request = EditBoardCustomFieldRequest(
            field_id=field_id,
            board_id=board_id,
            options=options
        )
        
        client.edit_board_custom_field(edit_request)
        
        # Step 3: Create task with multiple values
        selected_option_ids = [options[0]["_id"], options[2]["_id"]]  # Select options A and C
        custom_field = CustomField(
            id=field_id,
            value=selected_option_ids  # List of option IDs
        )
        
        task_request = CreateTaskRequest(
            name="Complete Workflow Test",
            group=group_id,
            board=board_id,
            project=project_id,
            custom_fields=[custom_field]
        )
        
        task_response = client.create_task(task_request)
        task_id = task_response.task.id
        
        # Step 4: Verify task has correct values
        retrieved_task_response = client.get_task(task_id)
        task = retrieved_task_response.task
        
        # Find the custom field
        custom_field_found = None
        for cf in task.custom_fields:
            if cf.id == field_id:
                custom_field_found = cf
                break
        
        assert custom_field_found is not None
        assert isinstance(custom_field_found.value, list)
        assert set(custom_field_found.value) == set(selected_option_ids)
        
        print(f"✅ Complete workflow test successful:")
        print(f"   - Custom field ID: {field_id}")
        print(f"   - Task ID: {task_id}")
        print(f"   - Selected values: {custom_field_found.value}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 