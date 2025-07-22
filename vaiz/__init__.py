from importlib import metadata

try:
    __version__ = metadata.version("vaiz-sdk")
except metadata.PackageNotFoundError:
    __version__ = "0.0.0"

from .client import VaizClient
from .models import (
    TaskFollower,
    TaskPriority,
    CustomField,
    CreateTaskRequest,
    EditTaskRequest,
    Task,
    TaskResponse,
    BoardResponse,
    BoardsResponse,
    CreateBoardTypeRequest,
    CreateBoardTypeResponse,
    EditBoardTypeRequest,
    EditBoardTypeResponse,
    Profile,
    ProfileResponse,
    Project,
    ProjectsResponse,
    ProjectResponse,
    Milestone,
    MilestonesResponse,
    CreateMilestoneRequest,
    CreateMilestoneResponse,
    GetMilestoneResponse,
    EditMilestoneRequest,
    EditMilestoneResponse,
    ToggleMilestoneRequest,
    ToggleMilestoneResponse,
    UploadedFile,
    UploadFileResponse,
    Comment,
    CommentReaction,
    PostCommentRequest,
    PostCommentResponse,
    ReactToCommentRequest,
    ReactToCommentResponse,
    GetCommentsRequest,
    GetCommentsResponse,
    EditCommentRequest,
    EditCommentResponse,
    DeleteCommentRequest,
    DeleteCommentResponse,
    CommentReactionType,
    COMMENT_REACTION_METADATA,
)

# Import helper functions for convenient usage
from .helpers import (
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
    add_board_custom_field_select_option,
    remove_board_custom_field_select_option,
    edit_board_custom_field_select_field_option,
    SelectOption,
    
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
)

__all__ = [
    'VaizClient',
    'TaskFollower',
    'TaskPriority',
    'CustomField',
    'CreateTaskRequest',
    'EditTaskRequest',
    'Task',
    'TaskResponse',
    'BoardResponse',
    'BoardsResponse',
    'CreateBoardTypeRequest',
    'CreateBoardTypeResponse',
    'EditBoardTypeRequest',
    'EditBoardTypeResponse',
    'ProfileResponse',
    'Project',
    'ProjectsResponse',
    'ProjectResponse',
    'Milestone',
    'MilestonesResponse',
    'CreateMilestoneRequest',
    'CreateMilestoneResponse',
    'GetMilestoneResponse',
    'EditMilestoneRequest',
    'EditMilestoneResponse',
    'ToggleMilestoneRequest',
    'ToggleMilestoneResponse',
    'UploadedFile',
    'UploadFileResponse',
    'Comment',
    'CommentReaction',
    'PostCommentRequest',
    'PostCommentResponse',
    'ReactToCommentRequest',
    'ReactToCommentResponse',
    'GetCommentsRequest',
    'GetCommentsResponse',
    'EditCommentRequest',
    'EditCommentResponse',
    'DeleteCommentRequest',
    'DeleteCommentResponse',
    'CommentReactionType',
    'COMMENT_REACTION_METADATA',
    
    # Helper functions for custom fields
    'make_text_field',
    'make_number_field',
    'make_checkbox_field',
    'make_date_field',
    'make_member_field',
    'make_task_relations_field',
    'make_select_field',
    'make_url_field',
    'make_select_option',
    'add_board_custom_field_select_option',
    'remove_board_custom_field_select_option',
    'edit_board_custom_field_select_field_option',
    'SelectOption',
    
    # Field editing helpers
    'edit_custom_field_name',
    'edit_custom_field_description',
    'edit_custom_field_visibility',
    'edit_custom_field_complete',
    
    # Task relations helpers
    'make_task_relation_value',
    'add_task_relation',
    'remove_task_relation',
    
    # Member field helpers
    'make_member_value',
    'add_member_to_field',
    'remove_member_from_field',
    
    # Date field helpers
    'make_date_value',
    'make_date_range_value',
    
    # Value formatting helpers
    'make_text_value',
    'make_number_value',
    'make_checkbox_value',
    'make_url_value',
]