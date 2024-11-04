export default defineNuxtPlugin(nuxtApp => {
  // console.log('common.nuxtApp:', nuxtApp);
  // console.log('common.globalThis:', globalThis);

  return {
    provide: {
      test: () => {}
    }
  };
});
