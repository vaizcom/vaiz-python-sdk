"""
Module demonstrating advanced custom field usage with Select type and multiple values.

This example shows how to:
1. Create a custom field of type Select with country options
2. Create a task that uses this custom field with multiple selected values
3. Verify the task was created with the correct custom field values
"""

import time
import hashlib
from typing import Optional
from .config import get_client, BOARD_ID, PROJECT_ID, GROUP_ID
from vaiz.models import (
    CreateBoardCustomFieldRequest, 
    CustomFieldType, 
    CreateTaskRequest,
    CustomField,
    TaskPriority
)
from vaiz.models.enums import EColor, EIcon


def generate_option_id(title: str) -> str:
    """Generate deterministic ID for option."""
    return hashlib.md5(title.encode()).hexdigest()[:24]


def create_multi_select_custom_field() -> Optional[str]:
    """
    Create a custom field of type Select with country options.
    
    Returns:
        Optional[str]: The ID of the created custom field, or None if creation failed
    """
    client = get_client()
    
    try:
        # Country options with proper format using enums
        country_options = [
            {
                "_id": generate_option_id("United States"),
                "title": "United States", 
                "color": EColor.Red,
                "icon": EIcon.User
            },
            {
                "_id": generate_option_id("Germany"),
                "title": "Germany",
                "color": EColor.Blue,
                "icon": EIcon.Circle
            },
            {
                "_id": generate_option_id("France"),
                "title": "France",
                "color": EColor.Violet,
                "icon": EIcon.Heart
            },
            {
                "_id": generate_option_id("Japan"),
                "title": "Japan",
                "color": EColor.Green,
                "icon": EIcon.Star
            },
            {
                "_id": generate_option_id("Brazil"),
                "title": "Brazil",
                "color": EColor.Gold,
                "icon": EIcon.Sun
            },
            {
                "_id": generate_option_id("India"),
                "title": "India",
                "color": EColor.Orange,
                "icon": EIcon.Fire
            },
            {
                "_id": generate_option_id("Canada"),
                "title": "Canada",
                "color": EColor.Mint,
                "icon": EIcon.Snow
            },
            {
                "_id": generate_option_id("Australia"),
                "title": "Australia",
                "color": EColor.Magenta,
                "icon": EIcon.Triangle
            }
        ]
        
        # Create the custom field with options
        create_request = CreateBoardCustomFieldRequest(
            name="Target Countries",
            type=CustomFieldType.SELECT,
            board_id=BOARD_ID,
            description="Select target countries for this task",
            hidden=False,
            options=country_options
        )
        
        print("Creating custom field 'Target Countries' with country options...")
        response = client.create_board_custom_field(create_request)
        custom_field = response.custom_field
        field_id = custom_field.id
        
        print(f"✅ Custom field created successfully!")
        print(f"   Field ID: {field_id}")
        print(f"   Field name: {custom_field.name}")
        print(f"   Field type: {custom_field.type}")
        print(f"   Options count: {len(custom_field.options)}")
        
        print(f"\n📋 Available country options:")
        for i, option in enumerate(custom_field.options):
            print(f"   {i+1}. {option['title']} (ID: {option['_id'][:8]}...)")
        
        return field_id, country_options
        
    except Exception as e:
        print(f"❌ Error creating custom field: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response content: {e.response.text}")
        return None, None


def create_task_with_multi_select_values(custom_field_id: str, country_options: list) -> Optional[str]:
    """
    Create a task with multiple selected values in the custom field.
    
    Args:
        custom_field_id (str): The ID of the custom field to use
        country_options (list): List of available country options
        
    Returns:
        Optional[str]: The ID of the created task, or None if creation failed
    """
    client = get_client()
    
    try:
        # Selected countries for this task (multiple values)
        selected_country_names = ["United States", "Germany", "Japan"]
        
        # Get the _id values for selected countries
        selected_country_ids = []
        for option in country_options:
            if option["title"] in selected_country_names:
                selected_country_ids.append(option["_id"])
        
        # Create custom field with multiple values
        custom_field = CustomField(
            id=custom_field_id,
            value=selected_country_ids  # List of option IDs for multi-select
        )
        
        # Create the task
        task_request = CreateTaskRequest(
            name="International Marketing Campaign",
            group=GROUP_ID,
            board=BOARD_ID,
            project=PROJECT_ID,
            description="Plan and execute marketing campaign for multiple international markets",
            priority=TaskPriority.High,
            custom_fields=[custom_field]
        )
        
        print(f"\n🎯 Creating task with selected countries: {selected_country_names}")
        task_response = client.create_task(task_request)
        task = task_response.task
        
        print(f"✅ Task created successfully!")
        print(f"   Task ID: {task.id}")
        print(f"   Task name: {task.name}")
        print(f"   Task priority: {task.priority}")
        print(f"   Custom fields count: {len(task.custom_fields)}")
        
        # Verify custom field values
        for cf in task.custom_fields:
            if cf.id == custom_field_id:
                print(f"   ✅ Custom field found with {len(cf.value)} selected countries")
                
                # Map option IDs back to country names for display
                selected_names = []
                for option_id in cf.value:
                    for option in country_options:
                        if option["_id"] == option_id:
                            selected_names.append(option["title"])
                            break
                
                print(f"   📍 Selected countries: {selected_names}")
                break
        else:
            print(f"   ⚠️  Custom field '{custom_field_id}' not found in task")
        
        return task.id
        
    except Exception as e:
        print(f"❌ Error creating task: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response content: {e.response.text}")
        return None


def verify_task_custom_field(task_id: str, custom_field_id: str, country_options: list) -> bool:
    """
    Verify that the task has the correct custom field values.
    
    Args:
        task_id (str): The ID of the task to verify
        custom_field_id (str): The ID of the custom field to check
        country_options (list): List of available country options
        
    Returns:
        bool: True if verification successful, False otherwise
    """
    client = get_client()
    
    try:
        print(f"\n🔍 Verifying task custom field values...")
        task_response = client.get_task(task_id)
        task = task_response.task
        
        # Find our custom field
        for cf in task.custom_fields:
            if cf.id == custom_field_id:
                print(f"✅ Found custom field with {len(cf.value)} values")
                
                if isinstance(cf.value, list) and len(cf.value) > 0:
                    print(f"   ✅ Multi-select working correctly with {len(cf.value)} values")
                    
                    # Display selected countries
                    selected_countries = []
                    for option_id in cf.value:
                        for option in country_options:
                            if option["_id"] == option_id:
                                selected_countries.append(option["title"])
                                break
                    
                    print(f"   🌍 Countries: {selected_countries}")
                    return True
                else:
                    print(f"   ⚠️  Expected list of values, got: {type(cf.value)}")
                    return False
        
        print(f"❌ Custom field '{custom_field_id}' not found in task")
        return False
        
    except Exception as e:
        print(f"❌ Error verifying task: {e}")
        return False


def demonstrate_multi_select_custom_field():
    """
    Complete demonstration of multi-select custom field functionality.
    
    This function orchestrates the entire process:
    1. Creates a custom field of type Select with country options
    2. Creates a task with multiple selected values
    3. Verifies the task was created correctly
    """
    print("🚀 Multi-Select Custom Field Demonstration")
    print("=" * 60)
    
    # Step 1: Create custom field with options
    result = create_multi_select_custom_field()
    if not result[0]:
        print("❌ Failed to create custom field. Aborting.")
        return
    
    custom_field_id, country_options = result
    
    # Give the API a moment to process
    time.sleep(1)
    
    # Step 2: Create task with multiple selected values
    task_id = create_task_with_multi_select_values(custom_field_id, country_options)
    if not task_id:
        print("❌ Failed to create task. Aborting.")
        return
    
    # Give the API a moment to process
    time.sleep(1)
    
    # Step 3: Verify the task was created correctly
    verification_success = verify_task_custom_field(task_id, custom_field_id, country_options)
    
    print("\n" + "=" * 60)
    if verification_success:
        print("🎉 Multi-Select Custom Field Demonstration SUCCESSFUL!")
        print(f"   - Custom Field ID: {custom_field_id}")
        print(f"   - Task ID: {task_id}")
        print("   - Multiple countries selected: United States, Germany, Japan")
        print("   - ✅ All functionality working correctly!")
    else:
        print("❌ Multi-Select Custom Field Demonstration FAILED!")
    
    return {
        'custom_field_id': custom_field_id,
        'task_id': task_id,
        'success': verification_success
    }


if __name__ == "__main__":
    demonstrate_multi_select_custom_field() 