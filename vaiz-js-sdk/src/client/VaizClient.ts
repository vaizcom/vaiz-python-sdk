import { VaizClientConfig, BaseAPIClient } from './BaseAPIClient';
import { BoardsAPI } from '../api/boards';

export class VaizClient extends BaseAPIClient {
  boards: BoardsAPI;

  constructor(config: VaizClientConfig) {
    super(config);
    this.boards = new BoardsAPI(config);
  }
}
export { VaizClientConfig } from './BaseAPIClient';
