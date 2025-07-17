import { BaseAPIClient } from './base';
import { ProjectsResponse, ProjectResponse } from './types';

export class ProjectsAPIClient extends BaseAPIClient {
  
  async getProjects(): Promise<ProjectsResponse> {
    /**
     * Get all projects in the current space.
     * 
     * @returns The list of projects
     */
    const responseData = await this.request<ProjectsResponse>('getProjects', 'POST', {});
    return responseData;
  }

  async getProject(projectId: string): Promise<ProjectResponse> {
    /**
     * Get a single project by its ID.
     * 
     * @param projectId The ID of the project to retrieve
     * @returns The project information
     */
    const responseData = await this.request<ProjectResponse>(
      'getProject', 
      'POST', 
      { projectId }
    );
    return responseData;
  }
}