import { BaseAPIClient } from './base';
import {
  MilestonesResponse,
  CreateMilestoneRequest,
  CreateMilestoneResponse,
  GetMilestoneResponse,
  EditMilestoneRequest,
  EditMilestoneResponse,
  ToggleMilestoneRequest,
  ToggleMilestoneResponse,
} from './types';

export class MilestonesAPIClient extends BaseAPIClient {
  
  async getMilestones(): Promise<MilestonesResponse> {
    /**
     * Get all milestones in the current space.
     * 
     * @returns The list of milestones
     */
    const responseData = await this.request<MilestonesResponse>('getMilestones', 'POST', {});
    return responseData;
  }

  async getMilestone(milestoneId: string): Promise<GetMilestoneResponse> {
    /**
     * Get a single milestone by its ID.
     * 
     * @param milestoneId The ID of the milestone to retrieve
     * @returns The milestone information
     */
    const responseData = await this.request<GetMilestoneResponse>(
      'getMilestone',
      'POST',
      { _id: milestoneId }
    );
    return responseData;
  }

  async createMilestone(request: CreateMilestoneRequest): Promise<CreateMilestoneResponse> {
    /**
     * Create a new milestone.
     * 
     * @param request The milestone creation request
     * @returns The created milestone information
     */
    const responseData = await this.request<CreateMilestoneResponse>(
      'createMilestone',
      'POST',
      request
    );
    return responseData;
  }

  async editMilestone(request: EditMilestoneRequest): Promise<EditMilestoneResponse> {
    /**
     * Edit an existing milestone.
     * 
     * @param request The milestone edit request
     * @returns The updated milestone information
     */
    const responseData = await this.request<EditMilestoneResponse>(
      'editMilestone',
      'POST',
      request
    );
    return responseData;
  }

  async toggleMilestone(request: ToggleMilestoneRequest): Promise<ToggleMilestoneResponse> {
    /**
     * Toggle milestone assignment for a task (attach/detach task to/from milestones).
     * 
     * @param request The milestone toggle request containing task ID and milestone IDs
     * @returns The updated task information with milestone assignments
     */
    const responseData = await this.request<ToggleMilestoneResponse>(
      'toggleMilestone',
      'POST',
      request
    );
    return responseData;
  }
}