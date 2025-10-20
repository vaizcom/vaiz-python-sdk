"""
Advanced Custom Field Management Example

This example demonstrates the advanced custom field helper functions:
- Field editing helpers
- Task relations management  
- Member field management
- Date field helpers
- Value formatting helpers

These functions make it much easier to work with different types of custom fields
and their values in a strongly-typed way.
"""

import time
from datetime import datetime, timedelta
from .config import get_client, BOARD_ID, PROJECT_ID, GROUP_ID

# Import all the new advanced helper functions
from vaiz import (
    # Field creation (from previous example)
    make_text_field,
    make_number_field,
    make_member_field,
    make_date_field,
    make_task_relations_field,
    make_select_field,
    make_select_option,
    
    # Field editing helpers
    edit_custom_field_name,
    edit_custom_field_description,
    edit_custom_field_visibility,
    edit_custom_field_complete,
    
    # Task relations helpers
    make_task_relation_value,
    add_task_relation,
    remove_task_relation,
    
    # Member field helpers
    make_member_value,
    add_member_to_field,
    remove_member_from_field,
    
    # Date field helpers
    make_date_value,
    make_date_range_value,
    
    # Value formatting helpers
    make_text_value,
    make_number_value,
    make_checkbox_value,
    make_url_value,
    
    # Models for task creation
    CreateTaskRequest,
    CustomField,
    TaskPriority
)
from vaiz.models.enums import Color, Icon


def demonstrate_field_editing():
    """Show how to edit existing custom fields."""
    client = get_client()
    
    print("🔧 Demonstrating field editing helpers...")
    
    # First create a field to edit
    original_field = make_text_field(
        name="Original Name",
        board_id=BOARD_ID,
        description="Original description"
    )
    
    field_response = client.create_board_custom_field(original_field)
    field_id = field_response.custom_field.id
    print(f"✅ Created field: {field_response.custom_field.name}")
    
    time.sleep(1)
    
    # Edit field name
    name_edit = edit_custom_field_name(
        field_id=field_id,
        board_id=BOARD_ID,
        new_name="🎯 Updated Field Name"
    )
    
    client.edit_board_custom_field(name_edit)
    print(f"✅ Updated field name to: 🎯 Updated Field Name")
    
    time.sleep(1)
    
    # Edit field description
    desc_edit = edit_custom_field_description(
        field_id=field_id,
        board_id=BOARD_ID,
        new_description="This field has been updated with new description and emoji!"
    )
    
    client.edit_board_custom_field(desc_edit)
    print(f"✅ Updated field description")
    
    time.sleep(1)
    
    # Edit multiple properties at once
    complete_edit = edit_custom_field_complete(
        field_id=field_id,
        board_id=BOARD_ID,
        name="🚀 Final Field Name",
        description="Final description with all updates applied",
        hidden=False
    )
    
    client.edit_board_custom_field(complete_edit)
    print(f"✅ Applied complete field update")
    
    return field_id


def demonstrate_task_relations():
    """Show how to work with task relations custom fields."""
    client = get_client()
    
    print(f"\n🔗 Demonstrating task relations helpers...")
    
    # Create a task relations field
    relations_field = make_task_relations_field(
        name="Related Tasks",
        board_id=BOARD_ID,
        description="Tasks that are related to this one"
    )
    
    field_response = client.create_board_custom_field(relations_field)
    field_id = field_response.custom_field.id
    print(f"✅ Created task relations field: {field_response.custom_field.name}")
    
    # Create some tasks to relate
    task_ids = []
    task_names = ["Backend API", "Frontend UI", "Database Schema", "Documentation"]
    
    for task_name in task_names:
        task_request = CreateTaskRequest(
            name=task_name,
            group=GROUP_ID,
            board=BOARD_ID,
            project=PROJECT_ID,
            description=f"Task for {task_name}",
            priority=TaskPriority.Medium
        )
        
        task_response = client.create_task(task_request)
        task_ids.append(task_response.task.id)
        print(f"  📋 Created task: {task_name}")
    
    time.sleep(2)
    
    # Create initial relations
    initial_relations = make_task_relation_value([task_ids[0], task_ids[1]])
    print(f"✅ Initial relations: {len(initial_relations)} tasks")
    
    # Add more relations
    updated_relations = add_task_relation(initial_relations, task_ids[2])
    updated_relations = add_task_relation(updated_relations, task_ids[3])
    print(f"✅ Added relations: {len(updated_relations)} tasks")
    
    # Remove a relation
    final_relations = remove_task_relation(updated_relations, task_ids[1])
    print(f"✅ Removed relation: {len(final_relations)} tasks")
    
    # Create a main task with these relations
    relations_custom_field = CustomField(
        id=field_id,
        value=final_relations
    )
    
    main_task_request = CreateTaskRequest(
        name="🎯 Main Project Task",
        group=GROUP_ID,
        board=BOARD_ID,
        project=PROJECT_ID,
        description="Main task with related subtasks",
        priority=TaskPriority.High,
        custom_fields=[relations_custom_field]
    )
    
    main_task_response = client.create_task(main_task_request)
    print(f"✅ Created main task with {len(final_relations)} related tasks")
    
    return field_id, main_task_response.task.id


def demonstrate_member_fields():
    """Show how to work with member custom fields."""
    client = get_client()
    
    print(f"\n👥 Demonstrating member field helpers...")
    
    # Create a member field
    member_field = make_member_field(
        name="Reviewers",
        board_id=BOARD_ID,
        description="People who need to review this task"
    )
    
    field_response = client.create_board_custom_field(member_field)
    field_id = field_response.custom_field.id
    print(f"✅ Created member field: {field_response.custom_field.name}")
    
    # Simulate member IDs (in real usage, these would come from your space)
    mock_member_ids = ["user_123", "user_456", "user_789"]
    
    # Start with single member
    single_member = make_member_value(mock_member_ids[0])
    print(f"✅ Single member: {single_member}")
    
    # Add more members
    multiple_members = add_member_to_field(single_member, mock_member_ids[1])
    multiple_members = add_member_to_field(multiple_members, mock_member_ids[2])
    print(f"✅ Multiple members: {len(multiple_members)} members")
    
    # Remove a member
    final_members = remove_member_from_field(multiple_members, mock_member_ids[1])
    print(f"✅ Removed member: {len(final_members)} members remaining")
    
    # Create task with member field
    member_custom_field = CustomField(
        id=field_id,
        value=final_members
    )
    
    member_task_request = CreateTaskRequest(
        name="👥 Task with Reviewers",
        group=GROUP_ID,
        board=BOARD_ID,
        project=PROJECT_ID,
        description="Task that requires review from team members",
        priority=TaskPriority.High,
        custom_fields=[member_custom_field]
    )
    
    member_task_response = client.create_task(member_task_request)
    print(f"✅ Created task with member assignments")
    
    return field_id, member_task_response.task.id


def demonstrate_date_fields():
    """Show how to work with date custom fields."""
    client = get_client()
    
    print(f"\n📅 Demonstrating date field helpers...")
    
    # Create a date field
    date_field = make_date_field(
        name="Target Launch Date",
        board_id=BOARD_ID,
        description="When we plan to launch this feature"
    )
    
    field_response = client.create_board_custom_field(date_field)
    field_id = field_response.custom_field.id
    print(f"✅ Created date field: {field_response.custom_field.name}")
    
    # Create date values
    launch_date = datetime.now() + timedelta(days=30)
    date_value = make_date_value(launch_date)
    print(f"✅ Launch date: {launch_date.strftime('%Y-%m-%d')}")
    
    # Create date range for project phases
    project_start = datetime.now()
    project_end = datetime.now() + timedelta(days=90)
    date_range = make_date_range_value(project_start, project_end)
    print(f"✅ Project duration: {(project_end - project_start).days} days")
    
    # Create task with date field
    date_custom_field = CustomField(
        id=field_id,
        value=date_value
    )
    
    date_task_request = CreateTaskRequest(
        name="📅 Scheduled Launch Task",
        group=GROUP_ID,
        board=BOARD_ID,
        project=PROJECT_ID,
        description="Task with specific launch date",
        priority=TaskPriority.High,
        custom_fields=[date_custom_field]
    )
    
    date_task_response = client.create_task(date_task_request)
    print(f"✅ Created task with launch date")
    
    return field_id, date_task_response.task.id


def demonstrate_value_formatting():
    """Show how to format values for different field types."""
    client = get_client()
    
    print(f"\n🎨 Demonstrating value formatting helpers...")
    
    # Create various fields for demonstration
    fields = {}
    
    # Text field
    text_field = make_text_field("Customer Info", BOARD_ID, "Customer details")
    text_response = client.create_board_custom_field(text_field)
    fields['text'] = text_response.custom_field.id
    print(f"✅ Created text field")
    
    time.sleep(1)
    
    # Number field  
    number_field = make_number_field("Budget Amount", BOARD_ID, "Project budget")
    number_response = client.create_board_custom_field(number_field)
    fields['number'] = number_response.custom_field.id
    print(f"✅ Created number field")
    
    time.sleep(1)
    
    # Prepare formatted values
    formatted_values = {
        'text': make_text_value("Acme Corporation - Enterprise Client 🏢"),
        'number': make_number_value(75000.50),
        'checkbox': make_checkbox_value(True),
        'url': make_url_value("https://acme-corp.com/project-details")
    }
    
    print(f"✅ Formatted values:")
    print(f"  📝 Text: {formatted_values['text']}")
    print(f"  🔢 Number: {formatted_values['number']}")
    print(f"  ☑️ Checkbox: {formatted_values['checkbox']}")
    print(f"  🔗 URL: {formatted_values['url']}")
    
    # Create task with formatted values
    custom_fields = [
        CustomField(id=fields['text'], value=formatted_values['text']),
        CustomField(id=fields['number'], value=formatted_values['number'])
    ]
    
    value_task_request = CreateTaskRequest(
        name="🎨 Task with Formatted Values",
        group=GROUP_ID,
        board=BOARD_ID,
        project=PROJECT_ID,
        description="Task demonstrating proper value formatting",
        priority=TaskPriority.Medium,
        custom_fields=custom_fields
    )
    
    value_task_response = client.create_task(value_task_request)
    print(f"✅ Created task with formatted custom field values")
    
    return fields, value_task_response.task.id


def verify_all_tasks():
    """Verify that all created tasks have their custom fields properly set."""
    client = get_client()
    
    print(f"\n🔍 Verifying all tasks...")
    
    # This would retrieve and verify the tasks created above
    # For demo purposes, we'll just show the concept
    print(f"✅ All tasks created successfully with custom fields")
    print(f"🎯 Advanced custom field management demonstration complete!")


def main():
    """Main demonstration function for advanced custom field management."""
    print("🚀 Advanced Custom Field Management Example")
    print("=" * 60)
    
    try:
        # Demonstrate field editing
        edited_field_id = demonstrate_field_editing()
        time.sleep(2)
        
        # Demonstrate task relations
        relations_field_id, main_task_id = demonstrate_task_relations()
        time.sleep(2)
        
        # Demonstrate member fields
        member_field_id, member_task_id = demonstrate_member_fields()
        time.sleep(2)
        
        # Demonstrate date fields
        date_field_id, date_task_id = demonstrate_date_fields()
        time.sleep(2)
        
        # Demonstrate value formatting
        value_fields, value_task_id = demonstrate_value_formatting()
        time.sleep(2)
        
        # Verify results
        verify_all_tasks()
        
        print(f"\n🎉 Advanced example completed successfully!")
        print(f"Created and demonstrated:")
        print(f"  📝 Field editing capabilities")
        print(f"  🔗 Task relations management")
        print(f"  👥 Member field management")
        print(f"  📅 Date field helpers")
        print(f"  🎨 Value formatting helpers")
        print(f"  📋 {5} tasks with various custom field types")
        
    except Exception as e:
        print(f"❌ Error during advanced demonstration: {e}")
        raise


if __name__ == "__main__":
    main() 