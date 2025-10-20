"""
Tests for custom field helper functions.

These tests verify that helper functions correctly create properly typed
request objects for all custom field types and option management.
"""

import pytest
from vaiz.helpers.custom_fields import (
    # Field creation helpers
    make_text_field,
    make_number_field,
    make_checkbox_field,
    make_date_field,
    make_member_field,
    make_task_relations_field,
    make_select_field,
    make_url_field,
    
    # Select field option helpers
    make_select_option,
    SelectOption,
    add_board_custom_field_select_option,
    remove_board_custom_field_select_option,
    edit_board_custom_field_select_field_option,
)
from vaiz.models import (
    CreateBoardCustomFieldRequest,
    EditBoardCustomFieldRequest,
    CustomFieldType
)
from vaiz.models.enums import Color, Icon


class TestFieldCreationHelpers:
    """Test all field creation helper functions."""
    
    def setup_method(self):
        """Set up test data."""
        self.board_id = "test_board_123"
        self.field_name = "Test Field"
        self.description = "Test description"
    
    def test_make_text_field(self):
        """Test text field creation."""
        request = make_text_field(
            name=self.field_name,
            board_id=self.board_id,
            description=self.description,
            hidden=True
        )
        
        assert isinstance(request, CreateBoardCustomFieldRequest)
        assert request.name == self.field_name
        assert request.type == CustomFieldType.TEXT
        assert request.board_id == self.board_id
        assert request.description == self.description
        assert request.hidden == True
        assert request.options is None
    
    def test_make_number_field(self):
        """Test number field creation."""
        request = make_number_field(
            name=self.field_name,
            board_id=self.board_id
        )
        
        assert isinstance(request, CreateBoardCustomFieldRequest)
        assert request.name == self.field_name
        assert request.type == CustomFieldType.NUMBER
        assert request.board_id == self.board_id
        assert request.description is None
        assert request.hidden == False
        assert request.options is None
    
    def test_make_checkbox_field(self):
        """Test checkbox field creation."""
        request = make_checkbox_field(
            name=self.field_name,
            board_id=self.board_id,
            description=self.description
        )
        
        assert isinstance(request, CreateBoardCustomFieldRequest)
        assert request.name == self.field_name
        assert request.type == CustomFieldType.CHECKBOX
        assert request.board_id == self.board_id
        assert request.description == self.description
        assert request.hidden == False
        assert request.options is None
    
    def test_make_date_field(self):
        """Test date field creation."""
        request = make_date_field(
            name=self.field_name,
            board_id=self.board_id
        )
        
        assert isinstance(request, CreateBoardCustomFieldRequest)
        assert request.name == self.field_name
        assert request.type == CustomFieldType.DATE
        assert request.board_id == self.board_id
        assert request.options is None
    
    def test_make_member_field(self):
        """Test member field creation."""
        request = make_member_field(
            name=self.field_name,
            board_id=self.board_id
        )
        
        assert isinstance(request, CreateBoardCustomFieldRequest)
        assert request.name == self.field_name
        assert request.type == CustomFieldType.MEMBER
        assert request.board_id == self.board_id
        assert request.options is None
    
    def test_make_task_relations_field(self):
        """Test task relations field creation."""
        request = make_task_relations_field(
            name=self.field_name,
            board_id=self.board_id
        )
        
        assert isinstance(request, CreateBoardCustomFieldRequest)
        assert request.name == self.field_name
        assert request.type == CustomFieldType.TASK_RELATIONS
        assert request.board_id == self.board_id
        assert request.options is None
    
    def test_make_url_field(self):
        """Test URL field creation."""
        request = make_url_field(
            name=self.field_name,
            board_id=self.board_id
        )
        
        assert isinstance(request, CreateBoardCustomFieldRequest)
        assert request.name == self.field_name
        assert request.type == CustomFieldType.URL
        assert request.board_id == self.board_id
        assert request.options is None


class TestSelectOptionHelpers:
    """Test select option creation and management."""
    
    def test_make_select_option_with_enums(self):
        """Test creating select option with enum values."""
        option = make_select_option(
            title="High Priority",
            color=Color.Red,
            icon=Icon.Flag
        )
        
        assert isinstance(option, SelectOption)
        assert option.title == "High Priority"
        assert option.color == Color.Red
        assert option.icon == Icon.Flag
        assert option.id is not None
        assert len(option.id) == 24  # MD5 hash truncated to 24 chars
        
        # Test dictionary format
        option_dict = option.to_dict()
        assert option_dict["_id"] == option.id
        assert option_dict["title"] == "High Priority"
        assert option_dict["color"] == Color.Red
        assert option_dict["icon"] == Icon.Flag
    
    def test_make_select_option_with_strings(self):
        """Test creating select option with string values."""
        option = make_select_option(
            title="Medium Priority",
            color=Color.Orange,
            icon="Circle"
        )
        
        assert isinstance(option, SelectOption)
        assert option.title == "Medium Priority"
        assert option.color == Color.Orange
        assert option.icon == Icon.Circle
    
    def test_make_select_option_with_custom_id(self):
        """Test creating select option with custom ID."""
        custom_id = "custom_option_id_123"
        option = make_select_option(
            title="Custom Option",
            color=Color.Blue,
            icon=Icon.User,
            option_id=custom_id
        )
        
        assert option.id == custom_id
        assert option.to_dict()["_id"] == custom_id
    
    def test_make_select_field_with_options(self):
        """Test creating select field with options."""
        options = [
            make_select_option("High", Color.Red, Icon.Flag),
            make_select_option("Medium", Color.Orange, Icon.Circle),
            make_select_option("Low", Color.Green, Icon.Target)
        ]
        
        request = make_select_field(
            name="Priority",
            board_id="board123",
            options=options,
            description="Task priority level"
        )
        
        assert isinstance(request, CreateBoardCustomFieldRequest)
        assert request.name == "Priority"
        assert request.type == CustomFieldType.SELECT
        assert request.board_id == "board123"
        assert request.description == "Task priority level"
        assert len(request.options) == 3
        
        # Check first option
        option_dict = request.options[0]
        assert option_dict["title"] == "High"
        assert option_dict["color"] == Color.Red
        assert option_dict["icon"] == Icon.Flag
        assert "_id" in option_dict
    
    def test_make_select_field_with_dict_options(self):
        """Test creating select field with dictionary options."""
        options = [
            {"_id": "opt1", "title": "Option 1", "color": Color.Red, "icon": Icon.Flag},
            {"_id": "opt2", "title": "Option 2", "color": Color.Blue, "icon": Icon.Circle}
        ]
        
        request = make_select_field(
            name="Test Select",
            board_id="board123",
            options=options
        )
        
        assert len(request.options) == 2
        assert request.options[0]["_id"] == "opt1"
        assert request.options[1]["_id"] == "opt2"
    
    def test_make_select_field_invalid_option_type(self):
        """Test error handling for invalid option types."""
        with pytest.raises(ValueError, match="Invalid option type"):
            make_select_field(
                name="Test",
                board_id="board123",
                options=["invalid_option"]  # String instead of SelectOption or dict
            )


class TestSelectOptionManagement:
    """Test functions for managing select field options."""
    
    def setup_method(self):
        """Set up test data."""
        self.field_id = "field_123"
        self.board_id = "board_123"
        self.existing_options = [
            {"_id": "opt1", "title": "Option 1", "color": Color.Red, "icon": Icon.Flag},
            {"_id": "opt2", "title": "Option 2", "color": Color.Blue, "icon": Icon.Circle}
        ]
    
    def test_add_board_custom_field_select_option(self):
        """Test adding a new option to select field."""
        new_option = make_select_option("Option 3", Color.Green, Icon.Target)
        
        request = add_board_custom_field_select_option(
            field_id=self.field_id,
            board_id=self.board_id,
            new_option=new_option,
            existing_options=self.existing_options
        )
        
        assert isinstance(request, EditBoardCustomFieldRequest)
        assert request.field_id == self.field_id
        assert request.board_id == self.board_id
        assert len(request.options) == 3
        
        # Check that new option was added
        new_option_dict = request.options[2]
        assert new_option_dict["title"] == "Option 3"
        assert new_option_dict["color"] == Color.Green
        assert new_option_dict["icon"] == Icon.Target
    
    def test_add_board_custom_field_select_option_with_dict(self):
        """Test adding a new option using dictionary format."""
        new_option = {"_id": "opt3", "title": "Option 3", "color": Color.Green, "icon": Icon.Target}
        
        request = add_board_custom_field_select_option(
            field_id=self.field_id,
            board_id=self.board_id,
            new_option=new_option,
            existing_options=self.existing_options
        )
        
        assert len(request.options) == 3
        assert request.options[2]["_id"] == "opt3"
    
    def test_remove_board_custom_field_select_option(self):
        """Test removing an option from select field."""
        request = remove_board_custom_field_select_option(
            field_id=self.field_id,
            board_id=self.board_id,
            option_id="opt1",
            existing_options=self.existing_options
        )
        
        assert isinstance(request, EditBoardCustomFieldRequest)
        assert request.field_id == self.field_id
        assert request.board_id == self.board_id
        assert len(request.options) == 1
        assert request.options[0]["_id"] == "opt2"
    
    def test_remove_board_custom_field_select_option_not_found(self):
        """Test error when trying to remove non-existent option."""
        with pytest.raises(ValueError, match="Option with ID 'nonexistent' not found"):
            remove_board_custom_field_select_option(
                field_id=self.field_id,
                board_id=self.board_id,
                option_id="nonexistent",
                existing_options=self.existing_options
            )
    
    def test_edit_board_custom_field_select_field_option(self):
        """Test editing an existing option in select field."""
        updated_option = make_select_option("Updated Option 1", Color.Magenta, Icon.Crown)
        
        request = edit_board_custom_field_select_field_option(
            field_id=self.field_id,
            board_id=self.board_id,
            option_id="opt1",
            updated_option=updated_option,
            existing_options=self.existing_options
        )
        
        assert isinstance(request, EditBoardCustomFieldRequest)
        assert request.field_id == self.field_id
        assert request.board_id == self.board_id
        assert len(request.options) == 2
        
        # Check that option was updated
        updated_option_dict = request.options[0]
        assert updated_option_dict["_id"] == "opt1"  # ID preserved
        assert updated_option_dict["title"] == "Updated Option 1"
        assert updated_option_dict["color"] == Color.Magenta
        assert updated_option_dict["icon"] == Icon.Crown
        
        # Check that other option remained unchanged
        assert request.options[1]["_id"] == "opt2"
        assert request.options[1]["title"] == "Option 2"
    
    def test_edit_board_custom_field_select_field_option_with_dict(self):
        """Test editing an option using dictionary format."""
        updated_option = {"title": "Updated Option 1", "color": Color.Magenta, "icon": Icon.Crown}
        
        request = edit_board_custom_field_select_field_option(
            field_id=self.field_id,
            board_id=self.board_id,
            option_id="opt1",
            updated_option=updated_option,
            existing_options=self.existing_options
        )
        
        # Check that ID was preserved
        updated_option_dict = request.options[0]
        assert updated_option_dict["_id"] == "opt1"
        assert updated_option_dict["title"] == "Updated Option 1"
    
    def test_edit_board_custom_field_select_field_option_not_found(self):
        """Test error when trying to edit non-existent option."""
        updated_option = make_select_option("New Title", Color.Red, Icon.Flag)
        
        with pytest.raises(ValueError, match="Option with ID 'nonexistent' not found"):
            edit_board_custom_field_select_field_option(
                field_id=self.field_id,
                board_id=self.board_id,
                option_id="nonexistent",
                updated_option=updated_option,
                existing_options=self.existing_options
            )


class TestFieldEditingHelpers:
    """Test field editing helper functions."""
    
    def setup_method(self):
        """Set up test data."""
        self.field_id = "field_123"
        self.board_id = "board_123"
    
    def test_edit_custom_field_name(self):
        """Test editing field name."""
        from vaiz.helpers import edit_custom_field_name
        
        request = edit_custom_field_name(
            field_id=self.field_id,
            board_id=self.board_id,
            new_name="Updated Field Name"
        )
        
        assert isinstance(request, EditBoardCustomFieldRequest)
        assert request.field_id == self.field_id
        assert request.board_id == self.board_id
        assert request.name == "Updated Field Name"
        assert request.description is None
        assert request.hidden is None
    
    def test_edit_custom_field_description(self):
        """Test editing field description."""
        from vaiz.helpers import edit_custom_field_description
        
        request = edit_custom_field_description(
            field_id=self.field_id,
            board_id=self.board_id,
            new_description="Updated description"
        )
        
        assert isinstance(request, EditBoardCustomFieldRequest)
        assert request.field_id == self.field_id
        assert request.board_id == self.board_id
        assert request.description == "Updated description"
        assert request.name is None
        assert request.hidden is None
    
    def test_edit_custom_field_visibility(self):
        """Test editing field visibility."""
        from vaiz.helpers import edit_custom_field_visibility
        
        request = edit_custom_field_visibility(
            field_id=self.field_id,
            board_id=self.board_id,
            hidden=True
        )
        
        assert isinstance(request, EditBoardCustomFieldRequest)
        assert request.field_id == self.field_id
        assert request.board_id == self.board_id
        assert request.hidden == True
        assert request.name is None
        assert request.description is None
    
    def test_edit_custom_field_complete(self):
        """Test editing multiple field properties at once."""
        from vaiz.helpers import edit_custom_field_complete
        
        request = edit_custom_field_complete(
            field_id=self.field_id,
            board_id=self.board_id,
            name="Complete Update",
            description="Complete description",
            hidden=False
        )
        
        assert isinstance(request, EditBoardCustomFieldRequest)
        assert request.field_id == self.field_id
        assert request.board_id == self.board_id
        assert request.name == "Complete Update"
        assert request.description == "Complete description"
        assert request.hidden == False


class TestTaskRelationsHelpers:
    """Test task relations helper functions."""
    
    def test_make_task_relation_value(self):
        """Test creating task relation values."""
        from vaiz.helpers import make_task_relation_value
        
        relations = make_task_relation_value(["task1", "task2", "task3"])
        
        assert isinstance(relations, list)
        assert len(relations) == 3
        assert "task1" in relations
        assert "task2" in relations
        assert "task3" in relations
    
    def test_add_task_relation(self):
        """Test adding task relations."""
        from vaiz.helpers import add_task_relation
        
        current_relations = ["task1", "task2"]
        updated_relations = add_task_relation(current_relations, "task3")
        
        assert len(updated_relations) == 3
        assert "task3" in updated_relations
        assert "task1" in updated_relations
        assert "task2" in updated_relations
        
        # Test adding duplicate (should not add)
        duplicate_relations = add_task_relation(updated_relations, "task1")
        assert len(duplicate_relations) == 3  # Should remain the same
    
    def test_remove_task_relation(self):
        """Test removing task relations."""
        from vaiz.helpers import remove_task_relation
        
        current_relations = ["task1", "task2", "task3"]
        updated_relations = remove_task_relation(current_relations, "task2")
        
        assert len(updated_relations) == 2
        assert "task2" not in updated_relations
        assert "task1" in updated_relations
        assert "task3" in updated_relations


class TestMemberFieldHelpers:
    """Test member field helper functions."""
    
    def test_make_member_value_single(self):
        """Test creating single member value."""
        from vaiz.helpers import make_member_value
        
        single_member = make_member_value("user123")
        assert single_member == "user123"
    
    def test_make_member_value_multiple(self):
        """Test creating multiple member values."""
        from vaiz.helpers import make_member_value
        
        multiple_members = make_member_value(["user123", "user456"])
        assert isinstance(multiple_members, list)
        assert len(multiple_members) == 2
        assert "user123" in multiple_members
        assert "user456" in multiple_members
    
    def test_add_member_to_field_single_to_multiple(self):
        """Test adding member to single member field."""
        from vaiz.helpers import add_member_to_field
        
        current_members = "user123"
        updated_members = add_member_to_field(current_members, "user456")
        
        assert isinstance(updated_members, list)
        assert len(updated_members) == 2
        assert "user123" in updated_members
        assert "user456" in updated_members
    
    def test_add_member_to_field_multiple(self):
        """Test adding member to multiple member field."""
        from vaiz.helpers import add_member_to_field
        
        current_members = ["user123", "user456"]
        updated_members = add_member_to_field(current_members, "user789")
        
        assert isinstance(updated_members, list)
        assert len(updated_members) == 3
        assert "user789" in updated_members
        
        # Test adding duplicate (should not add)
        duplicate_members = add_member_to_field(updated_members, "user123")
        assert len(duplicate_members) == 3  # Should remain the same
    
    def test_remove_member_from_field_single(self):
        """Test removing member from single member field."""
        from vaiz.helpers import remove_member_from_field
        
        current_members = "user123"
        updated_members = remove_member_from_field(current_members, "user123")
        
        assert updated_members == []
        
        # Test removing non-existent member
        unchanged_members = remove_member_from_field("user123", "user456")
        assert unchanged_members == "user123"
    
    def test_remove_member_from_field_multiple(self):
        """Test removing member from multiple member field."""
        from vaiz.helpers import remove_member_from_field
        
        current_members = ["user123", "user456", "user789"]
        updated_members = remove_member_from_field(current_members, "user456")
        
        assert isinstance(updated_members, list)
        assert len(updated_members) == 2
        assert "user456" not in updated_members
        assert "user123" in updated_members
        assert "user789" in updated_members


class TestDateFieldHelpers:
    """Test date field helper functions."""
    
    def test_make_date_value_datetime(self):
        """Test creating date value from datetime object."""
        from vaiz.helpers import make_date_value
        from datetime import datetime
        
        date_obj = datetime(2025, 12, 31, 15, 30, 45)
        date_value = make_date_value(date_obj)
        
        assert isinstance(date_value, str)
        assert "2025-12-31T15:30:45" in date_value
    
    def test_make_date_value_string(self):
        """Test creating date value from string."""
        from vaiz.helpers import make_date_value
        
        date_string = "2025-12-31T00:00:00"
        date_value = make_date_value(date_string)
        
        assert date_value == date_string
    
    def test_make_date_range_value(self):
        """Test creating date range value."""
        from vaiz.helpers import make_date_range_value
        from datetime import datetime
        
        start_date = datetime(2025, 1, 1)
        end_date = datetime(2025, 12, 31)
        
        date_range = make_date_range_value(start_date, end_date)
        
        assert isinstance(date_range, dict)
        assert "start" in date_range
        assert "end" in date_range
        assert "2025-01-01T00:00:00" in date_range["start"]
        assert "2025-12-31T00:00:00" in date_range["end"]


class TestValueFormattingHelpers:
    """Test value formatting helper functions."""
    
    def test_make_text_value(self):
        """Test text value formatting."""
        from vaiz.helpers import make_text_value
        
        text_value = make_text_value("Hello World")
        assert text_value == "Hello World"
        
        # Test with special characters
        special_text = make_text_value("Special: @#$%^&*()")
        assert special_text == "Special: @#$%^&*()"
    
    def test_make_number_value(self):
        """Test number value formatting."""
        from vaiz.helpers import make_number_value
        
        # Test integer
        int_value = make_number_value(42)
        assert int_value == "42"
        
        # Test float
        float_value = make_number_value(99.99)
        assert float_value == "99.99"
        
        # Test string
        string_value = make_number_value("12345")
        assert string_value == "12345"
    
    def test_make_checkbox_value(self):
        """Test checkbox value formatting."""
        from vaiz.helpers import make_checkbox_value
        
        true_value = make_checkbox_value(True)
        assert true_value == "true"
        
        false_value = make_checkbox_value(False)
        assert false_value == "false"
    
    def test_make_url_value(self):
        """Test URL value formatting."""
        from vaiz.helpers import make_url_value
        
        url_value = make_url_value("https://example.com/path")
        assert url_value == "https://example.com/path"


class TestEdgeCases:
    """Test edge cases and error handling."""
    
    def test_invalid_option_types_in_management_functions(self):
        """Test error handling for invalid option types in management functions."""
        with pytest.raises(ValueError, match="Invalid option type"):
            add_board_custom_field_select_option(
                field_id="field1",
                board_id="board1",
                new_option="invalid",  # String instead of SelectOption or dict
                existing_options=[]
            )
        
        with pytest.raises(ValueError, match="Invalid option type"):
            edit_board_custom_field_select_field_option(
                field_id="field1",
                board_id="board1",
                option_id="opt1",
                updated_option=123,  # Number instead of SelectOption or dict
                existing_options=[{"_id": "opt1", "title": "Test"}]
            ) 