import { ClientOptions, APIError } from './types';
import { 
  VaizError, 
  VaizAuthError, 
  VaizValidationError, 
  VaizNotFoundError, 
  VaizPermissionError, 
  VaizRateLimitError,
  VaizNetworkError
} from './errors';

// Simplified fetch wrapper that works in both Node.js and browser
const fetchWrapper = typeof fetch !== 'undefined' ? fetch : require('node-fetch');

export class BaseAPIClient {
  protected baseUrl: string;
  protected headers: Record<string, string>;
  protected verifySsl: boolean;
  protected verbose: boolean;

  constructor(options: ClientOptions) {
    this.baseUrl = options.baseUrl || 'https://api.vaiz.com/v4';
    this.verifySsl = options.verifySsl !== false; // default to true
    this.verbose = options.verbose || false;
    
    this.headers = {
      'Authorization': `Bearer ${options.apiKey}`,
      'current-space-id': options.spaceId,
      'Content-Type': 'application/json',
      'app-version': 'typescript-sdk-1.0.0'
    };
  }

  private parseError(responseData: any): APIError {
    const errorData = responseData.error || {};
    const metaData = errorData.meta || {};
    
    return {
      code: errorData.code || 'UnknownError',
      fields: errorData.fields || [],
      originalType: errorData.originalType || '',
      meta: {
        description: metaData.description,
        token: metaData.token
      }
    };
  }

  private handleApiError(apiError: APIError): never {
    const errorMap: Record<string, typeof VaizError> = {
      'JwtIncorrect': VaizAuthError,
      'JwtExpired': VaizAuthError,
      'ValidationError': VaizValidationError,
      'NotFound': VaizNotFoundError,
      'PermissionDenied': VaizPermissionError,
      'RateLimitExceeded': VaizRateLimitError,
    };
    
    const ErrorClass = errorMap[apiError.code] || VaizError;
    const message = apiError.meta?.description || apiError.code;
    throw new ErrorClass(message, apiError);
  }

  // Convert ISO date strings to Date objects recursively
  private parseDates(obj: any): any {
    if (obj === null || obj === undefined) {
      return obj;
    }
    
    if (typeof obj === 'string') {
      // Check if it's an ISO date string
      const isoDateRegex = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{3})?Z?$/;
      if (isoDateRegex.test(obj)) {
        return new Date(obj);
      }
      return obj;
    }
    
    if (Array.isArray(obj)) {
      return obj.map(item => this.parseDates(item));
    }
    
    if (typeof obj === 'object') {
      const parsed: any = {};
      for (const [key, value] of Object.entries(obj)) {
        parsed[key] = this.parseDates(value);
      }
      return parsed;
    }
    
    return obj;
  }

  // Convert Date objects to ISO strings recursively for API
  private serializeDates(obj: any): any {
    if (obj === null || obj === undefined) {
      return obj;
    }
    
    if (obj instanceof Date) {
      return obj.toISOString();
    }
    
    if (Array.isArray(obj)) {
      return obj.map(item => this.serializeDates(item));
    }
    
    if (typeof obj === 'object') {
      const serialized: any = {};
      for (const [key, value] of Object.entries(obj)) {
        serialized[key] = this.serializeDates(value);
      }
      return serialized;
    }
    
    return obj;
  }

  protected async request<T>(endpoint: string, method: string = 'POST', jsonData?: any): Promise<T> {
    const url = `${this.baseUrl}/${endpoint}`;
    
    // Serialize dates in request data
    const serializedData = jsonData ? this.serializeDates(jsonData) : undefined;
    
    if (this.verbose) {
      console.log('Request payload:', serializedData);
    }
    
    try {
      const response = await fetchWrapper(url, {
        method,
        headers: this.headers,
        body: serializedData ? JSON.stringify(serializedData) : undefined,
        // In Node.js environments, we might need to handle SSL verification
        ...(process?.env && !this.verifySsl ? { rejectUnauthorized: false } : {})
      });

      if (!response.ok) {
        throw new VaizNetworkError(`HTTP ${response.status}: ${response.statusText}`);
      }

      const responseData = await response.json();
      
      if (this.verbose) {
        console.log('Response data:', responseData);
      }

      // Check for error in response
      if (responseData.error) {
        const apiError = this.parseError(responseData);
        this.handleApiError(apiError);
      }
      
      // Parse dates in response data
      return this.parseDates(responseData) as T;

    } catch (error) {
      if (error instanceof VaizError) {
        throw error;
      }
      throw new VaizNetworkError(`Network error for ${url}: ${error}`, String(error));
    }
  }
}