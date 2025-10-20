"""
Custom Field Helpers Usage Example

This example demonstrates how to use the new helper functions for creating
and managing custom fields with the Vaiz SDK. These helpers provide strongly 
typed and simplified APIs for working with custom fields.
"""

import time
from .config import get_client, BOARD_ID, PROJECT_ID, GROUP_ID

# Import the new helper functions
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
    
    # Select field option helpers
    make_select_option,
    SelectOption,
    add_board_custom_field_select_option,
    remove_board_custom_field_select_option,
    edit_board_custom_field_select_field_option,
    
    # Models needed for task creation
    CreateTaskRequest,
    CustomField,
    TaskPriority
)
from vaiz.models.enums import EColor, EIcon


def demonstrate_field_creation_helpers():
    """Show how to create different types of custom fields using helpers."""
    client = get_client()
    
    print("🚀 Creating custom fields using helper functions...")
    
    # 1. Text field - simple and clean
    text_field_request = make_text_field(
        name="Customer Name",
        board_id=BOARD_ID,
        description="Name of the customer for this project",
        hidden=False
    )
    text_field_response = client.create_board_custom_field(text_field_request)
    print(f"✅ Created text field: {text_field_response.custom_field.name}")
    
    # 2. Number field - for numeric values
    number_field_request = make_number_field(
        name="Budget (USD)",
        board_id=BOARD_ID,
        description="Project budget in US dollars"
    )
    number_field_response = client.create_board_custom_field(number_field_request)
    print(f"✅ Created number field: {number_field_response.custom_field.name}")
    
    # 3. Checkbox field - for boolean values
    checkbox_field_request = make_checkbox_field(
        name="Approved",
        board_id=BOARD_ID,
        description="Whether this task has been approved"
    )
    checkbox_field_response = client.create_board_custom_field(checkbox_field_request)
    print(f"✅ Created checkbox field: {checkbox_field_response.custom_field.name}")
    
    # 4. Date field - for date selection
    date_field_request = make_date_field(
        name="Launch Date",
        board_id=BOARD_ID,
        description="Planned launch date for this feature"
    )
    date_field_response = client.create_board_custom_field(date_field_request)
    print(f"✅ Created date field: {date_field_response.custom_field.name}")
    
    # 5. Member field - for team member assignment
    member_field_request = make_member_field(
        name="Tech Lead",
        board_id=BOARD_ID,
        description="Technical lead responsible for this task"
    )
    member_field_response = client.create_board_custom_field(member_field_request)
    print(f"✅ Created member field: {member_field_response.custom_field.name}")
    
    # 6. URL field - for links
    url_field_request = make_url_field(
        name="Design Mockup",
        board_id=BOARD_ID,
        description="Link to the design mockup or prototype"
    )
    url_field_response = client.create_board_custom_field(url_field_request)
    print(f"✅ Created URL field: {url_field_response.custom_field.name}")
    
    # 7. Select field with options - the most complex but now simplified
    priority_options = [
        make_select_option("🔥 Critical", EColor.Red, EIcon.Fire),
        make_select_option("⚡ High", EColor.Orange, EIcon.Flag),
        make_select_option("📋 Medium", EColor.Blue, EIcon.Circle),
        make_select_option("🌱 Low", EColor.Green, EIcon.Target),
        make_select_option("💤 Someday", EColor.Violet, EIcon.Moon)
    ]
    
    select_field_request = make_select_field(
        name="Task Priority",
        board_id=BOARD_ID,
        options=priority_options,
        description="Priority level for this task"
    )
    select_field_response = client.create_board_custom_field(select_field_request)
    print(f"✅ Created select field: {select_field_response.custom_field.name} with {len(priority_options)} options")
    
    return {
        'text_field': text_field_response.custom_field,
        'number_field': number_field_response.custom_field,
        'checkbox_field': checkbox_field_response.custom_field,
        'date_field': date_field_response.custom_field,
        'member_field': member_field_response.custom_field,
        'url_field': url_field_response.custom_field,
        'select_field': select_field_response.custom_field,
        'priority_options': priority_options
    }


def demonstrate_select_option_management(select_field, priority_options):
    """Show how to manage select field options using helper functions."""
    client = get_client()
    
    print(f"\n🔧 Managing options for select field: {select_field.name}")
    
    field_id = select_field.id
    existing_options = select_field.options
    
    # 1. Add a new option
    new_option = make_select_option("🚨 Emergency", EColor.Magenta, EIcon.Crown)
    add_request = add_board_custom_field_select_option(
        field_id=field_id,
        board_id=BOARD_ID,
        new_option=new_option,
        existing_options=existing_options
    )
    
    add_response = client.edit_board_custom_field(add_request)
    print(f"✅ Added new option: {new_option.title}")
    
    # Update existing_options for next operations
    existing_options = add_response.custom_field.options
    
    # 2. Edit an existing option (change the "Low" priority option)
    # Find the "Low" option ID
    low_option_id = None
    for option in existing_options:
        if "Low" in option.get("title", ""):
            low_option_id = option["_id"]
            break
    
    if low_option_id:
        updated_option = make_select_option("🐌 Low Priority", EColor.Mint, EIcon.Target)
        edit_request = edit_board_custom_field_select_field_option(
            field_id=field_id,
            board_id=BOARD_ID,
            option_id=low_option_id,
            updated_option=updated_option,
            existing_options=existing_options
        )
        
        edit_response = client.edit_board_custom_field(edit_request)
        print(f"✅ Updated option: {updated_option.title}")
        
        # Update existing_options for next operation
        existing_options = edit_response.custom_field.options
    
    # 3. Remove an option (remove "Someday" option)
    someday_option_id = None
    for option in existing_options:
        if "Someday" in option.get("title", ""):
            someday_option_id = option["_id"]
            break
    
    if someday_option_id:
        remove_request = remove_board_custom_field_select_option(
            field_id=field_id,
            board_id=BOARD_ID,
            option_id=someday_option_id,
            existing_options=existing_options
        )
        
        remove_response = client.edit_board_custom_field(remove_request)
        print(f"✅ Removed 'Someday' option")
        
        return remove_response.custom_field
    
    return add_response.custom_field


def create_task_with_custom_fields(custom_fields):
    """Create a task using the custom fields we created."""
    client = get_client()
    
    print(f"\n📋 Creating a task with custom field values...")
    
    # Find a priority option to use
    select_field = custom_fields['select_field']
    priority_option_id = None
    if select_field.options:
        # Use the first option (Critical)
        priority_option_id = select_field.options[0]["_id"]
    
    # Create custom field values for the task
    task_custom_fields = []
    
    # Text field value
    task_custom_fields.append(CustomField(
        id=custom_fields['text_field'].id,
        value="Acme Corporation"
    ))
    
    # Number field value
    task_custom_fields.append(CustomField(
        id=custom_fields['number_field'].id,
        value="50000"
    ))
    
    # Checkbox field value
    task_custom_fields.append(CustomField(
        id=custom_fields['checkbox_field'].id,
        value="true"
    ))
    
    # URL field value
    task_custom_fields.append(CustomField(
        id=custom_fields['url_field'].id,
        value="https://figma.com/mockup-example"
    ))
    
    # Select field value
    if priority_option_id:
        task_custom_fields.append(CustomField(
            id=custom_fields['select_field'].id,
            value=[priority_option_id]  # List for multi-select support
        ))
    
    # Create the task
    task_request = CreateTaskRequest(
        name="E-commerce Platform Redesign",
        group=GROUP_ID,
        board=BOARD_ID,
        project=PROJECT_ID,
        description="Complete redesign of the e-commerce platform with modern UI/UX",
        priority=TaskPriority.High,
        custom_fields=task_custom_fields
    )
    
    task_response = client.create_task(task_request)
    print(f"✅ Created task: {task_response.task.name} with {len(task_custom_fields)} custom field values")
    
    return task_response.task


def verify_custom_fields_on_task(task):
    """Verify that custom fields are properly set on the task."""
    client = get_client()
    
    print(f"\n🔍 Verifying custom fields on task: {task.name}")
    
    # Get the task to see custom field values
    task_response = client.get_task(task.hrid)
    task_with_fields = task_response.task
    
    print(f"Task has {len(task_with_fields.custom_fields)} custom field values:")
    
    for custom_field in task_with_fields.custom_fields:
        print(f"  - Field ID: {custom_field.id}, Value: {custom_field.value}")
    
    return task_with_fields


def main():
    """Main demonstration function."""
    print("🎯 Custom Field Helpers Usage Example")
    print("=" * 50)
    
    try:
        # Step 1: Create various types of custom fields
        custom_fields = demonstrate_field_creation_helpers()
        time.sleep(2)  # Give API time to process
        
        # Step 2: Demonstrate select option management
        updated_select_field = demonstrate_select_option_management(
            custom_fields['select_field'], 
            custom_fields['priority_options']
        )
        custom_fields['select_field'] = updated_select_field
        time.sleep(2)  # Give API time to process
        
        # Step 3: Create a task with custom field values
        task = create_task_with_custom_fields(custom_fields)
        time.sleep(2)  # Give API time to process
        
        # Step 4: Verify the custom fields on the task
        verify_custom_fields_on_task(task)
        
        print(f"\n🎉 Example completed successfully!")
        print(f"Created {len(custom_fields)} different types of custom fields")
        print(f"Demonstrated option management (add, edit, remove)")
        print(f"Created a task with custom field values")
        
    except Exception as e:
        print(f"❌ Error during demonstration: {e}")
        raise


if __name__ == "__main__":
    main() 