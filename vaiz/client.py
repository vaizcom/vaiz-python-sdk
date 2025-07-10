# vaiz/client.py
from vaiz.api.tasks import TasksAPIClient
from vaiz.api.boards import BoardsAPIClient
from vaiz.api.profile import ProfileAPIClient
from vaiz.api.projects import ProjectsAPIClient
from vaiz.api.milestones import MilestonesAPIClient
from vaiz.api.upload import UploadAPIClient


class VaizClient(TasksAPIClient, BoardsAPIClient, ProfileAPIClient, ProjectsAPIClient, MilestonesAPIClient, UploadAPIClient):
    """
    Main client for interacting with the Vaiz API.
    This class inherits all task-related operations from TasksAPIClient,
    board-related operations from BoardsAPIClient,
    profile-related operations from ProfileAPIClient,
    project-related operations from ProjectsAPIClient,
    and milestone-related operations from MilestonesAPIClient.
    """
    pass