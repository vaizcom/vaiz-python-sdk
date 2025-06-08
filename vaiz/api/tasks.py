from vaiz.api.base import BaseAPIClient
from vaiz.models import CreateTaskRequest, TaskResponse, EditTaskRequest


class TasksAPIClient(BaseAPIClient):
    def create_task(self, task: CreateTaskRequest) -> TaskResponse:
        """
        Create a new task.
        
        Args:
            task (CreateTaskRequest): The task creation request containing all necessary task information
            
        Returns:
            TaskResponse: The created task information
        """
        response_data = self._make_request("createTask", json_data=task.model_dump(by_alias=True))
        return TaskResponse(**response_data)

    def edit_task(self, task: EditTaskRequest) -> TaskResponse:
        """
        Edit an existing task.
        
        Args:
            task (EditTaskRequest): The task edit request containing the updated task information
            
        Returns:
            TaskResponse: The updated task information
        """
        response_data = self._make_request("editTask", json_data=task.model_dump(by_alias=True))
        return TaskResponse(**response_data)

    def get_task(self, slug: str) -> TaskResponse:
        """
        Get task information by its slug.
        
        Args:
            slug (str): The task slug (e.g. "ABC-123")
            
        Returns:
            TaskResponse: The task information
        """
        response_data = self._make_request("getTask", json_data={"slug": slug})
        return TaskResponse(**response_data) 