import { BaseAPIClient } from './base';
import { 
  CreateTaskRequest, 
  TaskResponse, 
  EditTaskRequest, 
  TaskFile, 
  TaskUploadFile,
  UploadFileResponse,
  EUploadFileType
} from './types';
import * as fs from 'fs';
import * as path from 'path';

export class TasksAPIClient extends BaseAPIClient {
  
  async createTask(
    task: CreateTaskRequest, 
    description?: string,
    file?: TaskUploadFile
  ): Promise<TaskResponse> {
    /**
     * Create a new task with optional description and file upload.
     * 
     * If description is provided, it will be set in the task.
     * If file is provided (with 'path' and 'type'), the file will be automatically uploaded
     * and added to the task.files list before creating the task.
     * 
     * @param task The task creation request containing all necessary task information
     * @param description Task description to set
     * @param file File info with 'path' and 'type' for auto-upload
     * 
     * @throws Error If file path is provided but file doesn't exist
     * @throws Error If file dict is provided but doesn't contain 'path'
     */
    
    // Set description if provided
    if (description) {
      task.description = description;
    }
    
    // Handle automatic file upload if file is provided
    if (file) {
      if (!file.path) {
        throw new Error("File object must contain 'path' property");
      }
      
      const filePath = file.path;
      const fileType = file.type;
      
      if (!fs.existsSync(filePath)) {
        throw new Error(`File not found: ${filePath}`);
      }
      
      // Upload the file
      const uploadResponse = await this.uploadFile(filePath, fileType);
      const uploadedFile = uploadResponse.file;
      
      if (this.verbose) {
        console.log('Uploaded file:', uploadedFile);
      }
      
      // Create TaskFile and add to task.files
      const taskFile: TaskFile = {
        id: uploadedFile.id,
        url: uploadedFile.url,
        name: uploadedFile.name,
        ext: uploadedFile.ext,
        type: uploadedFile.type,
        dimension: uploadedFile.dimension,
        size: uploadedFile.size,
      };
      
      if (!task.files) {
        task.files = [];
      }
      task.files.push(taskFile);
    }
    
    const responseData = await this.request<any>('createTask', 'POST', task);
    
    // Add convenience property
    if (responseData.payload?.task) {
      responseData.task = responseData.payload.task;
    }
    
    return responseData as TaskResponse;
  }

  async editTask(task: EditTaskRequest): Promise<TaskResponse> {
    /**
     * Edit an existing task.
     * 
     * @param task The task edit request containing the updated task information
     * @returns The updated task information
     */
    const responseData = await this.request<any>('editTask', 'POST', task);
    
    // Add convenience property
    if (responseData.payload?.task) {
      responseData.task = responseData.payload.task;
    }
    
    return responseData as TaskResponse;
  }

  async getTask(slug: string): Promise<TaskResponse> {
    /**
     * Get task information by its slug.
     * 
     * @param slug The task slug (e.g. "ABC-123")
     * @returns The task information
     */
    const responseData = await this.request<any>('getTask', 'POST', { slug });
    
    // Add convenience property
    if (responseData.payload?.task) {
      responseData.task = responseData.payload.task;
    }
    
    return responseData as TaskResponse;
  }

  // Upload file helper method (will be moved to UploadAPIClient later)
  private async uploadFile(filePath: string, fileType: EUploadFileType): Promise<UploadFileResponse> {
    const url = `${this.baseUrl}/UploadFile`;
    
    try {
      // Check if we're in Node.js environment
      if (typeof window === 'undefined') {
        // Node.js environment
        const FormData = require('form-data');
        const formData = new FormData();
        
        formData.append('file', fs.createReadStream(filePath), path.basename(filePath));
        formData.append('type', fileType);
        
        const response = await fetch(url, {
          method: 'POST',
          headers: {
            'Authorization': this.headers['Authorization'],
            'current-space-id': this.headers['current-space-id'],
            'app-version': this.headers['app-version'],
            ...formData.getHeaders()
          },
          body: formData
        });
        
        if (!response.ok) {
          throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        return await response.json();
      } else {
        // Browser environment
        const formData = new FormData();
        const fileInput = document.createElement('input');
        fileInput.type = 'file';
        
        // This is a simplified version for browser - in real usage, 
        // you'd get the file from a file input or drag & drop
        throw new Error('File upload in browser environment requires File object, not file path');
      }
    } catch (error) {
      throw new Error(`Failed to upload file: ${error}`);
    }
  }
}