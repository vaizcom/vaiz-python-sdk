import { VaizClientConfig, BaseAPIClient } from './BaseAPIClient';
import { BoardsAPI } from '../api/boards';
export declare class VaizClient extends BaseAPIClient {
    boards: BoardsAPI;
    constructor(config: VaizClientConfig);
}
export { VaizClientConfig } from './BaseAPIClient';
