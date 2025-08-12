# vaiz/client.py
from vaiz.api.tasks import TasksAPIClient
from vaiz.api.boards import BoardsAPIClient
from vaiz.api.profile import ProfileAPIClient
from vaiz.api.projects import ProjectsAPIClient
from vaiz.api.milestones import MilestonesAPIClient
from vaiz.api.upload import UploadAPIClient
from vaiz.api.comments import CommentsAPIClient
from vaiz.api.documents import DocumentsAPIClient


class VaizClient(TasksAPIClient, BoardsAPIClient, ProfileAPIClient, ProjectsAPIClient, MilestonesAPIClient, UploadAPIClient, CommentsAPIClient, DocumentsAPIClient):
    """
    Main client for interacting with the Vaiz API.
    This class inherits all task-related operations from TasksAPIClient,
    board-related operations from BoardsAPIClient,
    profile-related operations from ProfileAPIClient,
    project-related operations from ProjectsAPIClient,
    milestone-related operations from MilestonesAPIClient,
    upload-related operations from UploadAPIClient,
    and comment-related operations from CommentsAPIClient.
    """
    pass