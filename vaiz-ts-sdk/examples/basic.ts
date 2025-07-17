import { VaizClient } from '../dist';

async function main() {
  const client = new VaizClient({ apiKey: 'your-key', spaceId: 'space' });
  const task = await client.createTask({ name: 'Demo', group: 'g', board: 'b', project: 'p' });
  console.log(task);
}

main();
