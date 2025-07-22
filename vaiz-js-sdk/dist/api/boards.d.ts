import { BaseAPIClient } from '../client/BaseAPIClient';
import { z } from 'zod';
export declare const BoardSchema: z.ZodObject<{
    _id: z.ZodString;
    name: z.ZodString;
}, "strip", z.ZodTypeAny, {
    _id: string;
    name: string;
}, {
    _id: string;
    name: string;
}>;
export type Board = z.infer<typeof BoardSchema>;
export declare const BoardsResponseSchema: z.ZodObject<{
    boards: z.ZodArray<z.ZodObject<{
        _id: z.ZodString;
        name: z.ZodString;
    }, "strip", z.ZodTypeAny, {
        _id: string;
        name: string;
    }, {
        _id: string;
        name: string;
    }>, "many">;
}, "strip", z.ZodTypeAny, {
    boards: {
        _id: string;
        name: string;
    }[];
}, {
    boards: {
        _id: string;
        name: string;
    }[];
}>;
export type BoardsResponse = z.infer<typeof BoardsResponseSchema>;
export declare class BoardsAPI extends BaseAPIClient {
    getBoards(): Promise<BoardsResponse>;
}
