import { VaizClient } from "../src";

// Setup fetch mock
const mockFetch = jest.fn();
global.fetch = mockFetch;

describe("TypeScript SDK Tests", () => {
  let client: VaizClient;

  beforeEach(() => {
    mockFetch.mockClear();
    client = new VaizClient({
      apiKey: "test-api-key",
      spaceId: "test-space-id",
    });
  });

  test("should create client with TypeScript types", () => {
    expect(client).toBeInstanceOf(VaizClient);
    expect(client.projects).toBeDefined();
  });

  test("should handle createTask with proper typing", async () => {
    const mockResponse = {
      payload: { task: { id: "123", name: "Test Task" } },
      type: "ok",
    };

    mockFetch.mockResolvedValue({
      ok: true,
      json: async () => mockResponse,
    });

    const result = await client.createTask({
      name: "TypeScript Test Task",
      group: "group-id",
      board: "board-id",
      project: "project-id",
    });

    expect(result.payload.task.name).toBe("Test Task");
    expect(mockFetch).toHaveBeenCalledWith(
      "https://api.vaiz.com/v4/createTask",
      expect.objectContaining({
        method: "POST",
        headers: expect.objectContaining({
          Authorization: "Bearer test-api-key",
          "current-space-id": "test-space-id",
        }),
      })
    );
  });
});
