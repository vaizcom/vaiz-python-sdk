import { VaizClient, ProjectsResponse, ProjectResponse } from '../src';
import { getTestClient } from './test-config';

describe('Projects API', () => {
  let client: VaizClient;

  beforeAll(() => {
    client = getTestClient();
  });

  test('should get all projects', async () => {
    const response = await client.projects.getProjects();
    
    expect(response.type).toBe('GetProjects');
    expect(response.payload.projects).toBeDefined();
    expect(Array.isArray(response.payload.projects)).toBe(true);
    
    console.log(`✅ Retrieved ${response.payload.projects.length} projects`);
    
    if (response.payload.projects.length > 0) {
      const project = response.payload.projects[0];
      expect(project._id).toBeDefined();
      expect(project.name).toBeDefined();
      console.log(`   First project: ${project.name} (${project._id})`);
    }
  });

  test('should get a specific project', async () => {
    // First get all projects to get a valid project ID
    const projectsResponse = await client.projects.getProjects();
    
    if (projectsResponse.payload.projects.length === 0) {
      console.log('⚠️ No projects available to test getProject');
      return;
    }
    
    const projectId = projectsResponse.payload.projects[0]._id;
    
    const response = await client.projects.getProject(projectId);
    
    expect(response.type).toBe('GetProject');
    expect(response.payload.project).toBeDefined();
    expect(response.payload.project._id).toBe(projectId);
    expect(response.payload.project.name).toBeDefined();
    
    console.log(`✅ Retrieved project: ${response.payload.project.name}`);
  });
});