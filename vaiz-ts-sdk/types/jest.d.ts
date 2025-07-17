/// <reference types="jest" />

declare global {
  const jest: typeof import("jest");
  const test: typeof import("@jest/globals").test;
  const expect: typeof import("@jest/globals").expect;
  const describe: typeof import("@jest/globals").describe;
  const beforeEach: typeof import("@jest/globals").beforeEach;
  const afterEach: typeof import("@jest/globals").afterEach;

  namespace NodeJS {
    interface Global {
      fetch: jest.Mock;
    }
  }

  var global: NodeJS.Global & typeof globalThis;
}
