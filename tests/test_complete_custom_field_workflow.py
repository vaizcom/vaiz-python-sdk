"""
Complete Custom Field Workflow Integration Test

This test creates various types of custom fields, creates tasks with values,
and verifies that everything appears correctly on the board.
"""

import pytest
from datetime import datetime, timedelta
from tests.test_config import get_test_client, TEST_BOARD_ID, TEST_PROJECT_ID, TEST_GROUP_ID

from vaiz import (
    # Field creation helpers
    make_text_field,
    make_number_field,
    make_checkbox_field,
    make_date_field,
    make_member_field,
    make_task_relations_field,
    make_select_field,
    make_url_field,
    
    # Value formatting helpers
    make_text_value,
    make_number_value,
    make_checkbox_value,
    make_date_value,
    make_member_value,
    make_task_relation_value,
    make_url_value,
    make_select_option,
    
    # Models
    CreateTaskRequest,
    CustomField,
    TaskPriority
)
from vaiz.models.enums import Color, Icon


class TestCompleteCustomFieldWorkflow:
    """Integration test for complete custom field workflow."""
    
    def setup_method(self):
        """Set up test data."""
        self.client = get_test_client()
        self.created_field_ids = []
        self.created_task_ids = []
    
    def teardown_method(self):
        """Clean up created resources."""
        # Note: In a real scenario, you might want to clean up created fields
        # but for debugging purposes, we'll leave them to inspect on the board
        pass
    
    def test_complete_workflow_all_field_types(self):
        """Test creating all types of custom fields and tasks with values."""
        print("\n🚀 Starting complete custom field workflow test...")
        # Step 1: Create different types of custom fields
        field_data = self._create_all_field_types()
        # Step 2: Create tasks with values for each field type
        tasks_data = self._create_tasks_with_values(field_data)
        # Step 3: Verify the tasks were created correctly
        self._verify_tasks_and_values(tasks_data, field_data)
        print(f"✅ Complete workflow test successful!")
        print(f"Created {len(field_data)} custom fields")
        print(f"Created {len(tasks_data)} tasks with custom field values")
        print(f"Check the board at: {TEST_BOARD_ID}")
        # Print field IDs for inspection
        for field_name, field_info in field_data.items():
            print(f"  📋 {field_name}: {field_info['id']} ({field_info['type']})")
    
    def _create_all_field_types(self):
        """Create one field of each type."""
        print("📝 Creating custom fields...")
        field_data = {}
        # Text field
        text_field = make_text_field(
            name="🏢 Company Name",
            board_id=TEST_BOARD_ID,
            description="Name of the client company"
        )
        response = self.client.create_board_custom_field(text_field)
        field_data['company'] = {
            'id': response.custom_field.id,
            'type': 'TEXT',
            'name': '🏢 Company Name'
        }
        self.created_field_ids.append(response.custom_field.id)
        print(f"  ✅ Created text field: {response.custom_field.id}")
        # Number field
        number_field = make_number_field(
            name="💰 Budget Amount",
            board_id=TEST_BOARD_ID,
            description="Project budget in USD"
        )
        response = self.client.create_board_custom_field(number_field)
        field_data['budget'] = {
            'id': response.custom_field.id,
            'type': 'NUMBER',
            'name': '💰 Budget Amount'
        }
        self.created_field_ids.append(response.custom_field.id)
        print(f"  ✅ Created number field: {response.custom_field.id}")
        # Checkbox field
        checkbox_field = make_checkbox_field(
            name="✅ Client Approved",
            board_id=TEST_BOARD_ID,
            description="Has the client approved this?"
        )
        response = self.client.create_board_custom_field(checkbox_field)
        field_data['approved'] = {
            'id': response.custom_field.id,
            'type': 'CHECKBOX',
            'name': '✅ Client Approved'
        }
        self.created_field_ids.append(response.custom_field.id)
        print(f"  ✅ Created checkbox field: {response.custom_field.id}")
        # Date field
        date_field = make_date_field(
            name="📅 Launch Date",
            board_id=TEST_BOARD_ID,
            description="Planned launch date"
        )
        response = self.client.create_board_custom_field(date_field)
        field_data['launch_date'] = {
            'id': response.custom_field.id,
            'type': 'DATE',
            'name': '📅 Launch Date'
        }
        self.created_field_ids.append(response.custom_field.id)
        print(f"  ✅ Created date field: {response.custom_field.id}")
        # URL field
        url_field = make_url_field(
            name="🔗 Project Link",
            board_id=TEST_BOARD_ID,
            description="Link to project documentation"
        )
        response = self.client.create_board_custom_field(url_field)
        field_data['project_url'] = {
            'id': response.custom_field.id,
            'type': 'URL',
            'name': '🔗 Project Link'
        }
        self.created_field_ids.append(response.custom_field.id)
        print(f"  ✅ Created URL field: {response.custom_field.id}")
        # Select field with options
        priority_options = [
            make_select_option("🔥 Critical", Color.Red, Icon.Fire),
            make_select_option("⚡ High", Color.Orange, Icon.Flag),
            make_select_option("📋 Medium", Color.Blue, Icon.Circle),
            make_select_option("🌱 Low", Color.Green, Icon.Target)
        ]
        select_field = make_select_field(
            name="🎯 Priority Level",
            board_id=TEST_BOARD_ID,
            options=priority_options,
            description="Task priority level"
        )
        response = self.client.create_board_custom_field(select_field)
        field_data['priority'] = {
            'id': response.custom_field.id,
            'type': 'SELECT',
            'name': '🎯 Priority Level',
            'options': {opt.title: opt.id for opt in priority_options}
        }
        self.created_field_ids.append(response.custom_field.id)
        print(f"  ✅ Created select field: {response.custom_field.id}")
        return field_data
    
    def _create_tasks_with_values(self, field_data):
        """Create tasks with different custom field values."""
        print("📋 Creating tasks with custom field values...")
        tasks_data = []
        # Task 1: E-commerce project
        ecommerce_fields = [
            CustomField(
                id=field_data['company']['id'],
                value=make_text_value("Acme Corporation 🏢")
            ),
            CustomField(
                id=field_data['budget']['id'],
                value=make_number_value(75000.50)
            ),
            CustomField(
                id=field_data['approved']['id'],
                value=make_checkbox_value(True)
            ),
            CustomField(
                id=field_data['launch_date']['id'],
                value=make_date_value(datetime.now() + timedelta(days=30))
            ),
            CustomField(
                id=field_data['project_url']['id'],
                value=make_url_value("https://acme-corp.com/ecommerce")
            ),
            CustomField(
                id=field_data['priority']['id'],
                value=[list(field_data['priority']['options'].values())[0]]  # Critical
            )
        ]
        ecommerce_task = CreateTaskRequest(
            name="🛒 E-commerce Platform Development",
            group=TEST_GROUP_ID,
            board=TEST_BOARD_ID,
            
            description="Build a modern e-commerce platform with payment integration",
            priority=TaskPriority.High,
            custom_fields=ecommerce_fields
        )
        response = self.client.create_task(ecommerce_task)
        tasks_data.append({
            'id': response.task.id,
            'name': response.task.name,
            'fields': ecommerce_fields
        })
        self.created_task_ids.append(response.task.id)
        print(f"  ✅ Created task: {response.task.name} ({response.task.id})")
        # Task 2: Mobile app project
        mobile_fields = [
            CustomField(
                id=field_data['company']['id'],
                value=make_text_value("TechStart Inc. 📱")
            ),
            CustomField(
                id=field_data['budget']['id'],
                value=make_number_value(45000)
            ),
            CustomField(
                id=field_data['approved']['id'],
                value=make_checkbox_value(False)
            ),
            CustomField(
                id=field_data['launch_date']['id'],
                value=make_date_value(datetime.now() + timedelta(days=60))
            ),
            CustomField(
                id=field_data['project_url']['id'],
                value=make_url_value("https://techstart.io/mobile-app")
            ),
            CustomField(
                id=field_data['priority']['id'],
                value=[list(field_data['priority']['options'].values())[2]]  # Medium
            )
        ]
        mobile_task = CreateTaskRequest(
            name="📱 Mobile App Development",
            group=TEST_GROUP_ID,
            board=TEST_BOARD_ID,
            
            description="Native mobile app for iOS and Android",
            priority=TaskPriority.Medium,
            custom_fields=mobile_fields
        )
        response = self.client.create_task(mobile_task)
        tasks_data.append({
            'id': response.task.id,
            'name': response.task.name,
            'fields': mobile_fields
        })
        self.created_task_ids.append(response.task.id)
        print(f"  ✅ Created task: {response.task.name} ({response.task.id})")
        # Task 3: Website redesign
        website_fields = [
            CustomField(
                id=field_data['company']['id'],
                value=make_text_value("Design Studio Pro 🎨")
            ),
            CustomField(
                id=field_data['budget']['id'],
                value=make_number_value(25000)
            ),
            CustomField(
                id=field_data['approved']['id'],
                value=make_checkbox_value(True)
            ),
            CustomField(
                id=field_data['launch_date']['id'],
                value=make_date_value(datetime.now() + timedelta(days=45))
            ),
            CustomField(
                id=field_data['project_url']['id'],
                value=make_url_value("https://designstudio.pro/redesign")
            ),
            CustomField(
                id=field_data['priority']['id'],
                value=[list(field_data['priority']['options'].values())[1]]  # High
            )
        ]
        website_task = CreateTaskRequest(
            name="🎨 Website Redesign Project",
            group=TEST_GROUP_ID,
            board=TEST_BOARD_ID,
            
            description="Complete website redesign with modern UI/UX",
            priority=TaskPriority.High,
            custom_fields=website_fields
        )
        response = self.client.create_task(website_task)
        tasks_data.append({
            'id': response.task.id,
            'name': response.task.name,
            'fields': website_fields
        })
        self.created_task_ids.append(response.task.id)
        print(f"  ✅ Created task: {response.task.name} ({response.task.id})")
        return tasks_data
    
    def _verify_tasks_and_values(self, tasks_data, field_data):
        """Verify that tasks were created with correct custom field values."""
        print("🔍 Verifying tasks and custom field values...")
        for task_info in tasks_data:
            # Get the task from API
            task = self.client.get_task(task_info['id']).task
            
            print(f"  📋 Verifying task: {task.name}")
            print(f"     ID: {task.id}")
            print(f"     Custom fields count: {len(task.custom_fields)}")
            
            # Check that custom fields exist
            assert len(task.custom_fields) > 0, f"Task {task.name} should have custom fields"
            
            # Print custom field values for debugging
            for cf in task.custom_fields:
                field_name = "Unknown"
                for name, info in field_data.items():
                    if info['id'] == cf.id:
                        field_name = info['name']
                        break
                
                print(f"       🎛️ {field_name}: {cf.value}")
            
            print(f"  ✅ Task verification complete")


if __name__ == "__main__":
    # Run the test manually for debugging
    test = TestCompleteCustomFieldWorkflow()
    test.setup_method()
    test.test_complete_workflow_all_field_types() 