import { BaseAPIClient } from './base';

export interface Project {
  id: string;
  name: string;
}

export interface ProjectsResponse {
  payload: { projects: Project[] };
  type: string;
}

export class ProjectsAPIClient extends BaseAPIClient {
  async getProjects(): Promise<ProjectsResponse> {
    return this.request<ProjectsResponse>('getProjects', {});
  }
}
