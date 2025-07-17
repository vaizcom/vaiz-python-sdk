import { BaseAPIClient } from './base';
import { ProfileResponse } from './types';

export class ProfileAPIClient extends BaseAPIClient {
  
  async getProfile(): Promise<ProfileResponse> {
    /**
     * Get the current user's profile.
     * 
     * @returns The user's profile information
     */
    const responseData = await this.request<ProfileResponse>('getProfile', 'POST', {});
    return responseData;
  }
}