import { APIError } from './types';

export class VaizError extends Error {
  public apiError?: APIError;

  constructor(message: string, apiError?: APIError) {
    let formattedMessage = message;
    
    if (apiError) {
      const errorDetails: string[] = [];
      errorDetails.push(`Error code: ${apiError.code}`);
      
      if (apiError.originalType) {
        errorDetails.push(`Original type: ${apiError.originalType}`);
      }
      
      if (apiError.fields && apiError.fields.length > 0) {
        const fieldStrs = apiError.fields.map(f => 
          typeof f === 'object' && f.name ? f.name : String(f)
        );
        errorDetails.push(`Affected fields: ${fieldStrs.join(', ')}`);
      }
      
      if (apiError.meta?.description) {
        errorDetails.push(`Details: ${apiError.meta.description}`);
      }
      
      if (errorDetails.length > 0) {
        formattedMessage = `${message}\n\n${errorDetails.join('\n')}`;
      }
    }
    
    super(formattedMessage);
    this.name = this.constructor.name;
    this.apiError = apiError;
  }
}

export class VaizAuthError extends VaizError {
  constructor(message: string, apiError?: APIError) {
    super(message, apiError);
  }
}

export class VaizValidationError extends VaizError {
  constructor(message: string, apiError?: APIError) {
    super(message, apiError);
  }
}

export class VaizNotFoundError extends VaizError {
  constructor(message: string, apiError?: APIError) {
    super(message, apiError);
  }
}

export class VaizPermissionError extends VaizError {
  constructor(message: string, apiError?: APIError) {
    super(message, apiError);
  }
}

export class VaizRateLimitError extends VaizError {
  constructor(message: string, apiError?: APIError) {
    super(message, apiError);
  }
}

export class VaizNetworkError extends VaizError {
  public responseText?: string;

  constructor(message: string, responseText?: string) {
    super(message);
    this.responseText = responseText;
  }
}