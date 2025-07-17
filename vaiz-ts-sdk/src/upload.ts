import { BaseAPIClient } from './base';
import { UploadFileResponse, EUploadFileType } from './types';
import * as fs from 'fs';
import * as path from 'path';

export class UploadAPIClient extends BaseAPIClient {
  
  async uploadFile(filePath: string, fileType: EUploadFileType): Promise<UploadFileResponse> {
    /**
     * Upload a file to the Vaiz platform.
     *
     * @param filePath Path to the file to upload.
     * @param fileType Type of the file (Image, Video, Pdf, or File).
     *                 - Image: Will display as image preview in interface
     *                 - Video: Will display as video player in interface  
     *                 - Pdf: Will display as PDF viewer in interface
     *                 - File: Will display as downloadable file attachment
     *
     * @returns The uploaded file information.
     */
    const url = `${this.baseUrl}/UploadFile`;
    
    try {
      // Check if we're in Node.js environment
      if (typeof window === 'undefined') {
        // Node.js environment
        const FormData = require('form-data');
        const formData = new FormData();
        
        formData.append('file', fs.createReadStream(filePath), path.basename(filePath));
        formData.append('type', fileType);
        
        const response = await fetch(url, {
          method: 'POST',
          headers: {
            'Authorization': this.headers['Authorization'],
            'current-space-id': this.headers['current-space-id'],
            'app-version': this.headers['app-version'],
            ...formData.getHeaders()
          },
          body: formData
        });
        
        if (!response.ok) {
          throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        const responseData = await response.json();
        return responseData as UploadFileResponse;
        
      } else {
        // Browser environment
        throw new Error('File upload in browser environment requires File object, not file path. Use uploadFileFromFile() method instead.');
      }
    } catch (error) {
      if (error instanceof Error) {
        throw error;
      }
      throw new Error(`Failed to upload file: ${error}`);
    }
  }

  async uploadFileFromFile(file: File, fileType: EUploadFileType): Promise<UploadFileResponse> {
    /**
     * Upload a file to the Vaiz platform from a File object (browser environment).
     *
     * @param file The File object to upload.
     * @param fileType Type of the file (Image, Video, Pdf, or File).
     *
     * @returns The uploaded file information.
     */
    const url = `${this.baseUrl}/UploadFile`;
    
    try {
      const formData = new FormData();
      formData.append('file', file, file.name);
      formData.append('type', fileType);
      
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Authorization': this.headers['Authorization'],
          'current-space-id': this.headers['current-space-id'],
          'app-version': this.headers['app-version']
          // Don't set Content-Type - let browser set it with boundary for FormData
        },
        body: formData
      });
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
      
      const responseData = await response.json();
      return responseData as UploadFileResponse;
      
    } catch (error) {
      if (error instanceof Error) {
        throw error;
      }
      throw new Error(`Failed to upload file: ${error}`);
    }
  }
}