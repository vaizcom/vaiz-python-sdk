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
)
from typing import Optional, Dict, Tuple
from datetime import datetime, timedelta
import os
import hashlib
import json


class TasksAPIClient(BaseAPIClient):
    def __init__(self, *args, **kwargs):
        """Initialize TasksAPIClient with caching support."""
        super().__init__(*args, **kwargs)
        self._tasks_cache: Dict[str, Tuple[GetTasksResponse, datetime]] = {}
        self._cache_ttl = timedelta(minutes=5)  # 5 minutes cache TTL
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

    def _get_cache_key(self, request: GetTasksRequest) -> str:
        """Generate a unique cache key for the request."""
        # Create a deterministic string from request parameters
        request_dict = request.model_dump(by_alias=True)
        request_str = json.dumps(request_dict, sort_keys=True)
        # Add space_id to make cache unique per space
        cache_str = f"{self.space_id}:{request_str}"
        # Create a hash for the cache key
        return hashlib.md5(cache_str.encode()).hexdigest()
    
    def _is_cache_valid(self, cached_time: datetime) -> bool:
        """Check if cached data is still valid (within TTL)."""
        return datetime.now() - cached_time < self._cache_ttl
    
    def clear_tasks_cache(self):
        """Clear all cached tasks data."""
        self._tasks_cache.clear()
        if self.verbose:
            print("Tasks cache cleared")
    
    def get_tasks(self, request: GetTasksRequest) -> GetTasksResponse:
        """
        Get tasks with optional filtering by assignees and pagination.
        Maximum 50 tasks per page. Results are automatically cached for 5 minutes for API protection.

        Args:
            request (GetTasksRequest): The request containing filter and pagination parameters

        Returns:
            GetTasksResponse: The response containing the list of tasks (max 50)
            
        Note:
            Caching is mandatory for API protection. The same request will return cached
            results for 5 minutes to prevent excessive API calls.
        """
        # Generate cache key
        cache_key = self._get_cache_key(request)
        
        # Check cache (mandatory for API protection)
        if cache_key in self._tasks_cache:
            cached_response, cached_time = self._tasks_cache[cache_key]
            if self._is_cache_valid(cached_time):
                if self.verbose:
                    print(f"Cache hit for getTasks (key: {cache_key[:8]}...)")
                return cached_response
            else:
                # Remove expired cache entry
                del self._tasks_cache[cache_key]
                if self.verbose:
                    print(f"Cache expired for getTasks (key: {cache_key[:8]}...)")
        
        # Make API request
        if self.verbose:
            print(f"Cache miss for getTasks (key: {cache_key[:8]}...)")
        
        response_data = self._make_request(
            "getTasks", json_data=request.model_dump(by_alias=True)
        )
        response = GetTasksResponse(**response_data)
        
        # Store in cache (mandatory for API protection)
        self._tasks_cache[cache_key] = (response, datetime.now())
        if self.verbose:
            print(f"Cached getTasks response (key: {cache_key[:8]}...)")
        
        return response

