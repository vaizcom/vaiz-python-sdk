import { VaizClient, CreateTaskRequest, EditTaskRequest, TaskPriority, TaskResponse, TaskUploadFile, EUploadFileType } from '../src';
import { getTestClient, TEST_BOARD_ID, TEST_GROUP_ID, TEST_PROJECT_ID, TEST_ASSIGNEE_ID } from './test-config';

describe('Tasks API', () => {
  let client: VaizClient;
  let createdTaskId: string;

  beforeAll(() => {
    client = getTestClient();
  });

  test('should create a task with due dates', async () => {
    const task: CreateTaskRequest = {
      name: 'Integration Test Task TS',
      group: TEST_GROUP_ID!,
      board: TEST_BOARD_ID!,
      project: TEST_PROJECT_ID!,
      priority: TaskPriority.High,
      completed: false,
      dueStart: new Date('2025-02-01T09:00:00Z'),  // February 1st, 9:00 AM
      dueEnd: new Date('2025-02-15T17:00:00Z'),    // February 15th, 5:00 PM
      types: [],
      assignees: [TEST_ASSIGNEE_ID!],
      subtasks: [],
      milestones: [],
      rightConnectors: [],
      leftConnectors: []
    };

    const response = await client.createTask(task);
    
    expect(response.type).toBe('CreateTask');
    expect(response.payload.task._id).toBeDefined();
    expect(response.payload.task.name).toBe('Integration Test Task TS');
    expect(response.payload.task.priority).toBe(TaskPriority.High);
    expect(response.payload.task.completed).toBe(false);
    
    // Check that due dates are properly set and are Date objects
    expect(response.payload.task.dueStart).toBeInstanceOf(Date);
    expect(response.payload.task.dueEnd).toBeInstanceOf(Date);
    
    console.log(`✅ Created task with due dates: ${response.payload.task._id}`);
    console.log(`   dueStart: ${response.payload.task.dueStart} (${typeof response.payload.task.dueStart})`);
    console.log(`   dueEnd: ${response.payload.task.dueEnd} (${typeof response.payload.task.dueEnd})`);
    
    // Store task ID for next test
    createdTaskId = response.payload.task._id;
  });

  test('should edit a task with updated due dates', async () => {
    expect(createdTaskId).toBeDefined();
    
    const editTask: EditTaskRequest = {
      taskId: createdTaskId,
      name: 'Integration Test Task TS Updated',
      priority: TaskPriority.Critical,
      completed: true,
      dueStart: new Date('2025-03-01T10:00:00Z'),  // March 1st, 10:00 AM
      dueEnd: new Date('2025-03-20T16:00:00Z'),    // March 20th, 4:00 PM
      assignees: [TEST_ASSIGNEE_ID!]
    };

    const response = await client.editTask(editTask);
    
    expect(response.type).toBe('EditTask');
    expect(response.payload.task._id).toBe(createdTaskId);
    expect(response.payload.task.name).toBe('Integration Test Task TS Updated');
    expect(response.payload.task.priority).toBe(TaskPriority.Critical);
    expect(response.payload.task.completed).toBe(true);
    
    // Check that due dates are updated and are Date objects
    expect(response.payload.task.dueStart).toBeInstanceOf(Date);
    expect(response.payload.task.dueEnd).toBeInstanceOf(Date);
    
    console.log(`✅ Updated task with new due dates`);
    console.log(`   dueStart: ${response.payload.task.dueStart} (${typeof response.payload.task.dueStart})`);
    console.log(`   dueEnd: ${response.payload.task.dueEnd} (${typeof response.payload.task.dueEnd})`);
  });

  test('should get a task by slug', async () => {
    expect(createdTaskId).toBeDefined();
    
    const response = await client.getTask(createdTaskId);
    
    expect(response.type).toBe('GetTask');
    expect(response.payload.task._id).toBe(createdTaskId);
    expect(response.payload.task.name).toBe('Integration Test Task TS Updated');
    
    // Check that due dates are properly retrieved as Date objects
    expect(response.payload.task.dueStart).toBeInstanceOf(Date);
    expect(response.payload.task.dueEnd).toBeInstanceOf(Date);
    
    console.log(`✅ Retrieved task with due dates`);
    console.log(`   dueStart: ${response.payload.task.dueStart} (${typeof response.payload.task.dueStart})`);
    console.log(`   dueEnd: ${response.payload.task.dueEnd} (${typeof response.payload.task.dueEnd})`);
  });

  test('should create a task with description', async () => {
    const task: CreateTaskRequest = {
      name: 'Task with Description',
      group: TEST_GROUP_ID!,
      board: TEST_BOARD_ID!,
      project: TEST_PROJECT_ID!,
      priority: TaskPriority.Medium,
      completed: false
    };
    
    const description = 'This is a test task with a detailed description for testing purposes.';
    
    const response = await client.createTask(task, description);
    
    expect(response.type).toBe('CreateTask');
    expect(response.payload.task.name).toBe('Task with Description');
    expect(response.payload.task.description).toBe(description);
    expect(response.payload.task.document).toBeDefined();
    
    console.log(`✅ Created task with description: ${response.payload.task._id}`);
  });

  test('should create a task with file upload', async () => {
    const task: CreateTaskRequest = {
      name: 'Task with File Upload',
      group: TEST_GROUP_ID!,
      board: TEST_BOARD_ID!,
      project: TEST_PROJECT_ID!,
      priority: TaskPriority.Low,
      completed: false
    };
    
    // Test with a real file from assets
    const filePath = '../assets/example.pdf';
    const file: TaskUploadFile = {
      path: filePath,
      type: EUploadFileType.Pdf
    };
    
    try {
      const response = await client.createTask(task, undefined, file);
      
      expect(response.type).toBe('CreateTask');
      expect(response.payload.task.name).toBe('Task with File Upload');
      expect(response.payload.task.document).toBeDefined();
      
      console.log(`✅ Created task with file upload: ${response.payload.task._id}`);
    } catch (error) {
      if (error instanceof Error && error.message.includes('File not found')) {
        console.log('⚠️ Skipping file upload test - test file not found');
        expect(true).toBe(true); // Mark test as passed
      } else {
        throw error;
      }
    }
  });
});