/**
 * Test configuration module for Vaiz TypeScript SDK tests.
 * Contains test credentials and helper functions for testing.
 */

import * as dotenv from 'dotenv';
import { VaizClient, ClientOptions } from '../src';

// Load environment variables from .env file
dotenv.config({ path: '../.env' });

// Test credentials
export const TEST_API_KEY = process.env.VAIZ_API_KEY;
if (!TEST_API_KEY) {
  throw new Error('Please set VAIZ_API_KEY environment variable or create a .env file with VAIZ_API_KEY=your_api_key');
}

export const TEST_SPACE_ID = process.env.VAIZ_SPACE_ID;
if (!TEST_SPACE_ID) {
  throw new Error('Please set VAIZ_SPACE_ID environment variable or create a .env file with VAIZ_SPACE_ID=your_space_id');
}

// Test configuration constants
export const TEST_PROJECT_ID = process.env.VAIZ_PROJECT_ID;
export const TEST_BOARD_ID = process.env.VAIZ_BOARD_ID;
export const TEST_GROUP_ID = process.env.VAIZ_GROUP_ID;
export const TEST_ASSIGNEE_ID = process.env.VAIZ_ASSIGNEE_ID;

export function getTestClient(): VaizClient {
  /**
   * Initialize and return a VaizClient instance for testing.
   */
  const options: ClientOptions = {
    apiKey: TEST_API_KEY,
    spaceId: TEST_SPACE_ID,
    verifySsl: false,
    baseUrl: 'https://api.vaiz.local:10000/v4',
    verbose: false // Set to true for debugging
  };
  
  return new VaizClient(options);
}