import axios, { AxiosInstance, AxiosRequestConfig } from 'axios';

export interface VaizClientConfig {
  apiKey: string;
  spaceId: string;
  baseUrl?: string;
  timeout?: number;
}

export class BaseAPIClient {
  protected http: AxiosInstance;
  constructor(private config: VaizClientConfig) {
    this.http = axios.create({
      baseURL: config.baseUrl || 'https://api.vaiz.app/v4',
      timeout: config.timeout || 10000,
    });

    this.http.interceptors.request.use((req) => {
      req.headers = req.headers || {};
      req.headers['Authorization'] = `Bearer ${this.config.apiKey}`;
      req.headers['X-Space-Id'] = this.config.spaceId;
      return req;
    });
  }
}
