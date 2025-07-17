import { AxiosInstance } from 'axios';
export interface VaizClientConfig {
    apiKey: string;
    spaceId: string;
    baseUrl?: string;
    timeout?: number;
}
export declare class BaseAPIClient {
    private config;
    protected http: AxiosInstance;
    constructor(config: VaizClientConfig);
}
