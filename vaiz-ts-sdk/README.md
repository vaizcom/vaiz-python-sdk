# Vaiz SDK for TypeScript

A minimal TypeScript port of the Python SDK. It exposes `VaizClient` for interacting with the Vaiz API. This package is intended for demonstration and does not implement the complete Python SDK.

## Installation

```bash
npm install vaiz-ts-sdk
```

## Usage

```ts
import { VaizClient } from 'vaiz-ts-sdk';

const client = new VaizClient({ apiKey: 'YOUR_KEY', spaceId: 'SPACE_ID' });
const res = await client.createTask({ name: 'Task', group: 'g', board: 'b', project: 'p' });
console.log(res.payload.task);
```

## Running tests

```bash
npm test
```

## Building

```bash
npm run build
```
