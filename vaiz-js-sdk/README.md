# Vaiz JavaScript SDK

Basic JavaScript/TypeScript SDK for the Vaiz API.

```ts
import { VaizClient } from './dist';

const client = new VaizClient({
  apiKey: 'your-api-key',
  spaceId: 'your-space-id',
});

async function main() {
  const boards = await client.boards.getBoards();
  console.log(boards);
}
main();
```
