import { BaseAPIClient } from './base';
import {
  BoardsResponse,
  BoardResponse,
  CreateBoardTypeRequest,
  CreateBoardTypeResponse,
  EditBoardTypeRequest,
  EditBoardTypeResponse,
  CreateBoardCustomFieldRequest,
  CreateBoardCustomFieldResponse,
  EditBoardCustomFieldRequest,
  EditBoardCustomFieldResponse,
  CreateBoardGroupRequest,
  CreateBoardGroupResponse,
  EditBoardGroupRequest,
  EditBoardGroupResponse,
} from './types';

export class BoardsAPIClient extends BaseAPIClient {
  
  async getBoards(): Promise<BoardsResponse> {
    /**
     * Get all boards in the current space.
     * 
     * @returns The list of boards
     */
    const responseData = await this.request<BoardsResponse>('getBoards', 'POST', {});
    return responseData;
  }

  async getBoard(boardId: string): Promise<BoardResponse> {
    /**
     * Get a single board by its ID.
     * 
     * @param boardId The ID of the board to retrieve
     * @returns The board information
     */
    const responseData = await this.request<BoardResponse>(
      'getBoard',
      'POST',
      { boardId }
    );
    return responseData;
  }

  async createBoardType(request: CreateBoardTypeRequest): Promise<CreateBoardTypeResponse> {
    /**
     * Create a new board type.
     * 
     * @param request The board type creation request
     * @returns The created board type information
     */
    const responseData = await this.request<CreateBoardTypeResponse>(
      'createBoardType',
      'POST',
      request
    );
    return responseData;
  }

  async editBoardType(request: EditBoardTypeRequest): Promise<EditBoardTypeResponse> {
    /**
     * Edit an existing board type.
     * 
     * @param request The board type edit request
     * @returns The updated board type information
     */
    const responseData = await this.request<EditBoardTypeResponse>(
      'editBoardType',
      'POST',
      request
    );
    return responseData;
  }

  async createBoardCustomField(request: CreateBoardCustomFieldRequest): Promise<CreateBoardCustomFieldResponse> {
    /**
     * Create a new custom field in a board.
     * 
     * @param request The custom field creation request
     * @returns The created custom field information
     */
    const responseData = await this.request<CreateBoardCustomFieldResponse>(
      'createBoardCustomField',
      'POST',
      request
    );
    return responseData;
  }

  async editBoardCustomField(request: EditBoardCustomFieldRequest): Promise<EditBoardCustomFieldResponse> {
    /**
     * Edit an existing custom field in a board.
     * 
     * @param request The custom field edit request
     * @returns The updated custom field information
     */
    const responseData = await this.request<EditBoardCustomFieldResponse>(
      'editBoardCustomField',
      'POST',
      request
    );
    return responseData;
  }

  async createBoardGroup(request: CreateBoardGroupRequest): Promise<CreateBoardGroupResponse> {
    /**
     * Create a new group in a board.
     * 
     * @param request The group creation request
     * @returns The created group information
     */
    const responseData = await this.request<CreateBoardGroupResponse>(
      'createBoardGroup',
      'POST',
      request
    );
    return responseData;
  }

  async editBoardGroup(request: EditBoardGroupRequest): Promise<EditBoardGroupResponse> {
    /**
     * Edit an existing group in a board.
     * 
     * @param request The group edit request
     * @returns The updated group information
     */
    const responseData = await this.request<EditBoardGroupResponse>(
      'editBoardGroup',
      'POST',
      request
    );
    return responseData;
  }
}