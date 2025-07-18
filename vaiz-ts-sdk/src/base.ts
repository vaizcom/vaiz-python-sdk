export interface APIError {
  code: string;
  message?: string;
}

export class VaizError extends Error {
  constructor(message: string, public info?: APIError) {
    super(message);
  }
}

export interface ClientOptions {
  apiKey: string;
  spaceId: string;
  baseUrl?: string;
  verifySsl?: boolean;
}

export class BaseAPIClient {
  private baseUrl: string;
  private headers: Record<string, string>;
  constructor(private options: ClientOptions) {
    this.baseUrl = options.baseUrl || 'https://api.vaiz.com/v4';
    this.headers = {
      'Authorization': `Bearer ${options.apiKey}`,
      'current-space-id': options.spaceId,
      'Content-Type': 'application/json'
    };
  }

  protected async request<T>(endpoint: string, body: any = {}): Promise<T> {
    const res = await fetch(`${this.baseUrl}/${endpoint}`, {
      method: 'POST',
      headers: this.headers,
      body: JSON.stringify(body)
    });
    const data: any = await res.json();
    if (!res.ok) {
      throw new VaizError('API error', data.error);
    }
    return data as T;
  }
}
