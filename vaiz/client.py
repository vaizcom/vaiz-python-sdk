# vaiz/client.py
from vaiz.api.tasks import TasksAPIClient
from vaiz.api.boards import BoardsAPIClient


class VaizClient(TasksAPIClient, BoardsAPIClient):
    """
    Main client for interacting with the Vaiz API.
    This class inherits all task-related operations from TasksAPIClient
    and board-related operations from BoardsAPIClient.
    """
    pass