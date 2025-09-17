from vaiz.api.base import BaseAPIClient
from vaiz.models import (
    CreateTaskRequest,
    TaskResponse,
    EditTaskRequest,
    TaskFile,
    TaskUploadFile,
    GetHistoryRequest,
    GetHistoryResponse,
    GetTasksRequest,
    GetTasksResponse,
    Task,
)
from typing import Optional, List
import os


class TasksAPIClient(BaseAPIClient):
    def create_task(
        self,
        task: CreateTaskRequest,
        description: Optional[str] = None,
        file: Optional[TaskUploadFile] = None,
    ) -> TaskResponse:
        """
        Create a new task with optional description and strongly-typed file parameter.
        If a file is provided, it must include path and type (both required).

        If description is provided, it will be set in the task.
        If file is provided (with 'path' and optionally 'type'), the file will be automatically uploaded
        and added to the task.files list before creating the task.

        Args:
            task (CreateTaskRequest): The task creation request containing all necessary task information
            description (Optional[str]): Task description to set
            file (Optional[TaskUploadFile]): File info with 'path' and optional 'type' (auto-detected if not provided)

        Returns:
            TaskResponse: The created task information

        Raises:
            FileNotFoundError: If file path is provided but file doesn't exist
            ValueError: If file dict is provided but doesn't contain 'path'
        """
        # Set description if provided
        if description:
            task.description = description

        # Handle automatic file upload if file is provided
        if file:
            if file.path is None:
                raise ValueError("File dict must contain 'path' key")

            file_path = file.path
            file_type = file.type

            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")

            # Upload the file
            upload_response = self.upload_file(file_path, file_type)
            uploaded_file = upload_response.file

            print(uploaded_file)

            # Create TaskFile and add to task.files
            task_file = TaskFile(
                url=uploaded_file.url,
                name=uploaded_file.name,
                ext=uploaded_file.ext,
                id=uploaded_file.id,
                type=uploaded_file.type,
                # Pass all available fields from UploadedFile
                dimension=uploaded_file.dimension,
                size=uploaded_file.size,
            )
            task.files.append(task_file)

        response_data = self._make_request(
            "createTask", json_data=task.model_dump(by_alias=True)
        )
        return TaskResponse(**response_data)

    def edit_task(self, task: EditTaskRequest) -> TaskResponse:
        """
        Edit an existing task.

        Args:
            task (EditTaskRequest): The task edit request containing the updated task information

        Returns:
            TaskResponse: The updated task information
        """
        response_data = self._make_request(
            "editTask", json_data=task.model_dump(by_alias=True)
        )
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

    def get_history(self, request: GetHistoryRequest) -> GetHistoryResponse:
        """
        Get the history for a task or other kind.
        Args:
            request (GetHistoryRequest): The request model for history retrieval.
        Returns:
            GetHistoryResponse: The response containing histories.
        """
        response_data = self._make_request(
            "getHistory", json_data=request.model_dump(by_alias=True)
        )
        return GetHistoryResponse(**response_data)

    def get_tasks(self, request: GetTasksRequest) -> GetTasksResponse:
        """
        Get tasks with optional filtering by assignees and pagination.
        Maximum 50 tasks per page.

        Args:
            request (GetTasksRequest): The request containing filter and pagination parameters

        Returns:
            GetTasksResponse: The response containing the list of tasks (max 50)
        """
        response_data = self._make_request(
            "getTasks", json_data=request.model_dump(by_alias=True)
        )
        return GetTasksResponse(**response_data)

    def get_all_tasks(
        self, request: Optional[GetTasksRequest] = None, max_tasks: int = 500
    ) -> List[Task]:
        """
        Get all tasks matching the filters, automatically handling pagination.

        This is a convenience method that automatically fetches multiple pages of tasks.
        Use with caution on large datasets as it may take time and resources.

        Args:
            request (Optional[GetTasksRequest]): The request with filters (limit and skip will be managed automatically)
            max_tasks (int): Maximum number of tasks to fetch (default 500, max 10000)

        Returns:
            List[Task]: A list of all tasks matching the filters

        Example:
            # Get all completed tasks
            request = GetTasksRequest(completed=True)
            all_completed_tasks = client.get_all_tasks(request)

            # Get all tasks with default filters
            all_tasks = client.get_all_tasks()
        """
        if max_tasks > 10000:
            raise ValueError("max_tasks cannot exceed 10000 for safety reasons")

        # Create base request if not provided
        if request is None:
            request = GetTasksRequest()

        all_tasks = []
        page = 0

        while len(all_tasks) < max_tasks:
            # Create a copy of the request with pagination
            paginated_request = GetTasksRequest(
                ids=request.ids,
                board=request.board,
                project=request.project,
                assignees=request.assignees,
                parent_task=request.parent_task,
                milestones=request.milestones,
                completed=request.completed,
                archived=request.archived,
                limit=50,  # Always use max limit per page
                skip=page * 50,
            )

            response = self.get_tasks(paginated_request)
            tasks = response.payload.tasks

            if not tasks:
                break  # No more tasks

            all_tasks.extend(tasks)

            if len(tasks) < 50:
                break  # Last page had fewer than 50 tasks

            page += 1

            # Respect max_tasks limit
            if len(all_tasks) >= max_tasks:
                all_tasks = all_tasks[:max_tasks]
                break

        return all_tasks
