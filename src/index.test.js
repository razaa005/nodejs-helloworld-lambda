const { handler } = require('./index');

test('should return Hello, World', async() => {
  const result = await handler();
  expect(result).toBe('Hello World!');
});
