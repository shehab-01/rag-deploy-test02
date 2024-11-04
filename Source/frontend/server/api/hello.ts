export default defineEventHandler(event => {
  console.log('server.api.hello..');
  return {
    api: 'this works !'
  };
});
