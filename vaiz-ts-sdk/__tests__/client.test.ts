import { VaizClient } from '../src';

const fetchMock = jest.fn();
(global as any).fetch = fetchMock;

test('createTask sends request', async () => {
  fetchMock.mockResolvedValue({ ok: true, json: async () => ({payload:{task:{id:'1',name:'test'}},type:'ok'}) });
  const client = new VaizClient({apiKey:'key',spaceId:'space'});
  const res = await client.createTask({name:'test',group:'g',board:'b',project:'p'});
  expect(fetchMock).toHaveBeenCalledWith('https://api.vaiz.com/v4/createTask', expect.objectContaining({method:'POST'}));
  expect(res.payload.task.name).toBe('test');
});
