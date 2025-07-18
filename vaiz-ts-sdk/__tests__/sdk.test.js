const { VaizClient } = require("../dist/index.js");

// Mock fetch globally
global.fetch = jest.fn();

describe("Vaiz TypeScript SDK", () => {
  let client;

  beforeEach(() => {
    // Reset fetch mock
    fetch.mockClear();

    // Create client
    client = new VaizClient({
      apiKey: "test-api-key",
      spaceId: "test-space-id",
    });
  });

  describe("createTask", () => {
    test("should send correct request and return task", async () => {
      const mockResponse = {
        payload: { task: { id: "123", name: "Test Task" } },
        type: "ok",
      };

      fetch.mockResolvedValue({
        ok: true,
        json: async () => mockResponse,
      });

      const taskData = {
        name: "Test Task",
        group: "group-id",
        board: "board-id",
        project: "project-id",
      };

      const result = await client.createTask(taskData);

      // Verify fetch was called correctly
      expect(fetch).toHaveBeenCalledWith(
        "https://api.vaiz.com/v4/createTask",
        expect.objectContaining({
          method: "POST",
          headers: expect.objectContaining({
            Authorization: "Bearer test-api-key",
            "current-space-id": "test-space-id",
            "Content-Type": "application/json",
          }),
          body: JSON.stringify(taskData),
        })
      );

      // Verify response
      expect(result).toEqual(mockResponse);
      expect(result.payload.task.name).toBe("Test Task");
    });

    test("should handle API errors", async () => {
      const errorResponse = {
        error: { code: "TaskCreationFailed", message: "Failed to create task" },
      };

      fetch.mockResolvedValue({
        ok: false,
        json: async () => errorResponse,
      });

      const taskData = {
        name: "Test Task",
        group: "group-id",
        board: "board-id",
        project: "project-id",
      };

      await expect(client.createTask(taskData)).rejects.toThrow("API error");
    });
  });

  describe("getTask", () => {
    test("should fetch task by slug", async () => {
      const mockResponse = {
        payload: { task: { id: "123", name: "Retrieved Task" } },
        type: "ok",
      };

      fetch.mockResolvedValue({
        ok: true,
        json: async () => mockResponse,
      });

      const result = await client.getTask("task-slug");

      expect(fetch).toHaveBeenCalledWith(
        "https://api.vaiz.com/v4/getTask",
        expect.objectContaining({
          method: "POST",
          body: JSON.stringify({ slug: "task-slug" }),
        })
      );

      expect(result.payload.task.name).toBe("Retrieved Task");
    });
  });

  describe("projects", () => {
    test("should have projects client instance", () => {
      expect(client.projects).toBeDefined();
      expect(typeof client.projects.getProjects).toBe("function");
    });
  });

  describe("client configuration", () => {
    test("should use custom baseUrl when provided", () => {
      const customClient = new VaizClient({
        apiKey: "test-key",
        spaceId: "test-space",
        baseUrl: "https://custom.api.url/v4",
      });

      fetch.mockResolvedValue({
        ok: true,
        json: async () => ({ payload: { task: {} }, type: "ok" }),
      });

      return customClient
        .createTask({
          name: "Test",
          group: "g",
          board: "b",
          project: "p",
        })
        .then(() => {
          expect(fetch).toHaveBeenCalledWith(
            "https://custom.api.url/v4/createTask",
            expect.any(Object)
          );
        });
    });

    test("should set correct headers", async () => {
      fetch.mockResolvedValue({
        ok: true,
        json: async () => ({ payload: { task: {} }, type: "ok" }),
      });

      await client.createTask({
        name: "Test",
        group: "g",
        board: "b",
        project: "p",
      });

      const [, options] = fetch.mock.calls[0];
      expect(options.headers).toEqual({
        Authorization: "Bearer test-api-key",
        "current-space-id": "test-space-id",
        "Content-Type": "application/json",
      });
    });
  });
});
