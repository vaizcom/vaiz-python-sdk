import { ZodSchema } from 'zod';

export function validate<T>(schema: ZodSchema<T>, data: unknown): T {
  return schema.parse(data);
}
