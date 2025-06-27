from vaiz.api.base import BaseAPIClient
from vaiz.models import CreateTaskRequest, TaskResponse, EditTaskRequest, TaskFile, TaskUploadFile
from vaiz.models.enums import EUploadFileType
from typing import Optional, Dict, Any
import os


class TasksAPIClient(BaseAPIClient):
    def create_task(
        self, 
        task: CreateTaskRequest, 
        description: Optional[str] = None,
        file: Optional[TaskUploadFile] = None
    ) -> TaskResponse:
        """
        Create a new task с опциональным description и строго типизированным file.
        Если file передан, он должен содержать path и type (оба обязательны).
        
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