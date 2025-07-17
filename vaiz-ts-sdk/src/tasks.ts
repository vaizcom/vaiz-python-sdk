import { BaseAPIClient } from './base';

export interface CreateTaskRequest {
  name: string;
  group: string;
  board: string;
  project: string;
}

export interface Task {
  id: string;
  name: string;
}

export interface TaskResponse {
  payload: { task: Task };
  type: string;
}

export class TasksAPIClient extends BaseAPIClient {
  async createTask(task: CreateTaskRequest): Promise<TaskResponse> {
    return this.request<TaskResponse>('createTask', task);
  }

  async getTask(slug: string): Promise<TaskResponse> {
    return this.request<TaskResponse>('getTask', { slug });
  }
}
