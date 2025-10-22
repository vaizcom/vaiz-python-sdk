"""
Test for missing field types: Member and TaskRelations

This test specifically creates and tests Member and TaskRelations fields
which weren't included in our main workflow test.
"""

import pytest
from datetime import datetime
from tests.test_config import get_test_client, TEST_BOARD_ID, TEST_PROJECT_ID, TEST_GROUP_ID

from vaiz import (
    make_member_field,
    make_task_relations_field,
    make_member_value,
    make_task_relation_value,
    CreateTaskRequest,
    CustomField,
    TaskPriority
)


class TestMissingFieldTypes:
    """Test Member and TaskRelations field types."""
    
    def setup_method(self):
        """Set up test data."""
        self.client = get_test_client()
    
    def test_member_field_creation_and_usage(self):
        """Test Member field creation and usage in tasks."""
        print("\n👥 Testing Member field...")
        # Create member field
        member_field = make_member_field(
            name="👥 Assigned Reviewers",
            board_id=TEST_BOARD_ID,
            description="Team members assigned to review this task"
        )
        response = self.client.create_board_custom_field(member_field)
        field_id = response.custom_field.id
        print(f"  ✅ Created member field: {field_id}")
        assert response.custom_field.id is not None
        assert response.custom_field.type.value == "Member"
        # Create task with member field value
        # Note: In real usage, these would be actual user IDs from the space
        mock_user_ids = ["user_123", "user_456", "user_789"]
        member_value = make_member_value(mock_user_ids)  # Multiple members
        member_custom_field = CustomField(
            id=field_id,
            value=member_value
        )
        task_request = CreateTaskRequest(
            name="👥 Task with Member Assignments",
            group=TEST_GROUP_ID,
            board=TEST_BOARD_ID,
            
            description="Task that requires review from specific team members",
            priority=TaskPriority.High,
            custom_fields=[member_custom_field]
        )
        task_response = self.client.create_task(task_request)
        task_id = task_response.task.id
        print(f"  ✅ Created task with member field: {task_id}")
        # Verify the task has the member field value
        created_task = self.client.get_task(task_id).task
        assert len(created_task.custom_fields) > 0
        member_field_on_task = next(
            cf for cf in created_task.custom_fields 
            if cf.id == field_id
        )
        print(f"  ✅ Member field value: {member_field_on_task.value}")
        assert member_field_on_task.value == mock_user_ids
    
    def test_task_relations_field_creation_and_usage(self):
        """Test TaskRelations field creation and usage in tasks."""
        print("\n🔗 Testing TaskRelations field...")
        # Create task relations field
        relations_field = make_task_relations_field(
            name="🔗 Related Tasks",
            board_id=TEST_BOARD_ID,
            description="Tasks that are dependencies or related to this task"
        )
        response = self.client.create_board_custom_field(relations_field)
        field_id = response.custom_field.id
        print(f"  ✅ Created task relations field: {field_id}")
        assert response.custom_field.id is not None
        assert response.custom_field.type.value == "TaskRelations"
        # First, create some tasks to relate to
        related_task_ids = []
        task_names = ["🔧 Backend Development", "🎨 UI Design", "📱 Mobile Testing"]
        for task_name in task_names:
            related_task_request = CreateTaskRequest(
                name=task_name,
                group=TEST_GROUP_ID,
                board=TEST_BOARD_ID,
                
                description=f"Related task: {task_name}",
                priority=TaskPriority.Medium
            )
            
            related_response = self.client.create_task(related_task_request)
            related_task_ids.append(related_response.task.id)
            print(f"    📋 Created related task: {task_name} ({related_response.task.id})")
        # Create main task with relations
        relations_value = make_task_relation_value(related_task_ids)
        relations_custom_field = CustomField(
            id=field_id,
            value=relations_value
        )
        main_task_request = CreateTaskRequest(
            name="🎯 Main Project Coordination",
            group=TEST_GROUP_ID,
            board=TEST_BOARD_ID,
            
            description="Main task that coordinates other related tasks",
            priority=TaskPriority.High,
            custom_fields=[relations_custom_field]
        )
        main_task_response = self.client.create_task(main_task_request)
        main_task_id = main_task_response.task.id
        print(f"  ✅ Created main task with relations: {main_task_id}")
        # Verify the task has the relations field value
        created_task = self.client.get_task(main_task_id).task
        assert len(created_task.custom_fields) > 0
        relations_field_on_task = next(
            cf for cf in created_task.custom_fields 
            if cf.id == field_id
        )
        print(f"  ✅ Task relations value: {relations_field_on_task.value}")
        print(f"  ✅ Number of related tasks: {len(relations_field_on_task.value)}")
        assert isinstance(relations_field_on_task.value, list)
        assert len(relations_field_on_task.value) == len(related_task_ids)
        # Verify all task IDs are in the relations
        for task_id in related_task_ids:
            assert task_id in relations_field_on_task.value
    
    def test_complete_member_and_relations_workflow(self):
        """Test both Member and TaskRelations fields in a single workflow."""
        print("\n🔄 Testing complete Member + TaskRelations workflow...")
        # Create member field
        member_field = make_member_field(
            name="👥 Workflow Reviewers",
            board_id=TEST_BOARD_ID,
            description="Team members for workflow testing"
        )
        member_response = self.client.create_board_custom_field(member_field)
        member_field_id = member_response.custom_field.id
        print(f"  ✅ Created member field: {member_field_id}")
        # Create task relations field
        relations_field = make_task_relations_field(
            name="🔗 Workflow Relations",
            board_id=TEST_BOARD_ID,
            description="Task dependencies for workflow testing"
        )
        relations_response = self.client.create_board_custom_field(relations_field)
        relations_field_id = relations_response.custom_field.id
        print(f"  ✅ Created relations field: {relations_field_id}")
        # Create some related tasks
        related_task_ids = []
        for i, task_name in enumerate(["🔧 Backend API", "🎨 Frontend UI"]):
            related_task_request = CreateTaskRequest(
                name=task_name,
                group=TEST_GROUP_ID,
                board=TEST_BOARD_ID,
                
                description=f"Workflow related task {i+1}",
                priority=TaskPriority.Medium
            )
            related_response = self.client.create_task(related_task_request)
            related_task_ids.append(related_response.task.id)
            print(f"    📋 Created related task: {task_name}")
        # Create a task that uses both field types
        mock_reviewers = ["reviewer_001", "reviewer_002"]
        combined_fields = [
            CustomField(
                id=member_field_id,
                value=make_member_value(mock_reviewers)
            ),
            CustomField(
                id=relations_field_id,
                value=make_task_relation_value(related_task_ids)
            )
        ]
        combined_task_request = CreateTaskRequest(
            name="🚀 Combined Member + Relations Task",
            group=TEST_GROUP_ID,
            board=TEST_BOARD_ID,
            
            description="Task that combines both member assignments and task relations",
            priority=TaskPriority.High,
            custom_fields=combined_fields
        )
        combined_response = self.client.create_task(combined_task_request)
        combined_task_id = combined_response.task.id
        print(f"  ✅ Created combined task: {combined_task_id}")
        # Verify both field types work correctly
        combined_task = self.client.get_task(combined_task_id).task
        assert len(combined_task.custom_fields) == 2
        member_field = next(cf for cf in combined_task.custom_fields if cf.id == member_field_id)
        relations_field = next(cf for cf in combined_task.custom_fields if cf.id == relations_field_id)
        print(f"  ✅ Member field value: {member_field.value}")
        print(f"  ✅ Relations field value: {relations_field.value}")
        assert member_field.value == mock_reviewers
        assert relations_field.value == related_task_ids
        print(f"✅ Complete Member + TaskRelations workflow successful!")


if __name__ == "__main__":
    # Run the test manually for debugging
    test = TestMissingFieldTypes()
    test.setup_method()
    test.test_complete_member_and_relations_workflow() 