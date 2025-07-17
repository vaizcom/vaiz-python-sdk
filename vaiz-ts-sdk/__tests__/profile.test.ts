import { VaizClient, ProfileResponse } from '../src';
import { getTestClient } from './test-config';

describe('Profile API', () => {
  let client: VaizClient;

  beforeAll(() => {
    client = getTestClient();
  });

  test('should get user profile', async () => {
    const response = await client.profile.getProfile();
    
    expect(response.type).toBe('GetProfile');
    expect(response.payload.profile).toBeDefined();
    expect(response.payload.profile._id).toBeDefined();
    expect(response.payload.profile.name).toBeDefined();
    expect(response.payload.profile.email).toBeDefined();
    
    console.log(`✅ Retrieved profile for: ${response.payload.profile.name} (${response.payload.profile.email})`);
  });

  test('should have valid profile fields', async () => {
    const response = await client.profile.getProfile();
    const profile = response.payload.profile;
    
    // Test field types
    expect(typeof profile._id).toBe('string');
    expect(typeof profile.name).toBe('string');
    expect(typeof profile.email).toBe('string');
    
    // Email should be valid format
    expect(profile.email).toMatch(/^[^\s@]+@[^\s@]+\.[^\s@]+$/);
    
    console.log(`✅ Profile validation passed`);
    console.log(`   ID: ${profile._id}`);
    console.log(`   Name: ${profile.name}`);
    console.log(`   Email: ${profile.email}`);
    console.log(`   Role: ${profile.role || 'not specified'}`);
    console.log(`   Avatar: ${profile.avatar || 'not specified'}`);
  });
});