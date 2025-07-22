import { BaseAPIClient } from '../client/BaseAPIClient';
import { z } from 'zod';

export const BoardSchema = z.object({
  _id: z.string(),
  name: z.string(),
});
export type Board = z.infer<typeof BoardSchema>;

export const BoardsResponseSchema = z.object({
  boards: z.array(BoardSchema),
});
export type BoardsResponse = z.infer<typeof BoardsResponseSchema>;

export class BoardsAPI extends BaseAPIClient {
  async getBoards(): Promise<BoardsResponse> {
    const res = await this.http.get('/boards');
    return BoardsResponseSchema.parse(res.data);
  }
}
