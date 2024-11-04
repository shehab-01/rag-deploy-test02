<template>
  <h2>Fetch Test..</h2>
  <div class="d-flex">
    <v-btn variant="outlined" class="ma-5" @click="page.test">TEST</v-btn>
    <v-btn variant="outlined" class="ma-5" @click="page.test1">TEST1</v-btn>
    <v-btn variant="outlined" class="ma-5" @click="page.test2">TEST2</v-btn>
    <v-btn variant="outlined" class="ma-5" @click="page.test3">TEST3</v-btn>
    <v-btn variant="outlined" class="ma-5" @click="page.test4">TEST4</v-btn>
  </div>
  <div>
    <v-btn variant="outlined" class="ma-5" @click="$router.back()">Back</v-btn>
  </div>
</template>

<script setup lang="ts">
onMounted(() => {
  max.ui.init({
    page: page
  });
});

// TEST:
let url = '/health';
let url_0 = '/api/hello';
let url_1 = 'https://jsonplaceholder.typicode.com/photos';
let url_2 = 'https://www.ag-grid.com/example-assets/row-data.json';
let url_3 = 'https://www.ag-grid.com/example-assets/small-row-data.json';

const page = {
  init() {
    // const axios = useNuxtApp().$axios;
    // axios.get('/api/hello').then(response => {
    //   console.log('response:', response);
    // });
  },
  test() {
    useApi()
      .request({
        method: 'get',
        url: url,
        data: {}
      })
      .then(result => {
        console.log('result:', result);
      })
      .catch(ex => {
        console.error('ex:', ex);
      });
  },
  async test1() {
    let res = await useApi().request({
      method: 'get',
      url: url,
      data: {}
    });
    console.log('res:', res);
  },
  async test2() {
    const list = await $fetch(url_1, {
      credentials: 'include'
    });
    console.log('list:', list);
  },
  async test3() {
    const { data: list, refresh } = await useFetch(url_3, {});
    console.log('list:', list);
  },
  async test4() {
    const { data: list, refresh } = await useAsyncData('get', () => {
      return $fetch(url_3);
    });
    console.log('list:', list);
  }
};
</script>
