import { ZodSchema } from 'zod';
export declare function validate<T>(schema: ZodSchema<T>, data: unknown): T;
