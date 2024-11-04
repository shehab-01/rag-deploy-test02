<template>
  <h2>CRUD Test..</h2>
  <div class="d-flex">
    <v-btn variant="outlined" class="ma-5" @click="page.test_search">Search</v-btn>
    <v-btn variant="outlined" class="ma-5" @click="page.test_insert">Insert</v-btn>
    <v-btn variant="outlined" class="ma-5" @click="page.test_update">Update</v-btn>
    <v-btn variant="outlined" class="ma-5" @click="page.test_delete">Delete</v-btn>
  </div>
</template>

<script setup lang="ts">
onMounted(() => {
  max.ui.init({
    page: page
  });
});

const page = {
  init() {
    // console.log('page.init..');
  },
  // TEST:
  test_search() {
    useApi()
      .request({
        method: 'get',
        url: '/api/org/list',
        data: { search_text: '테스트' }
        // params: { search: '테스트' }
      })
      .then(result => {
        console.log('result:', result);
      })
      .catch(ex => {
        console.error('ex:', ex);
      });
  },
  test_insert() {
    useApi()
      .request({
        method: 'post',
        url: '/api/org/create',
        data: { org_id: 'test2', org_nm: '테스트기관', org_div: 'DC', org_type: '01' }
      })
      .then(result => {
        console.log('result:', result);
      })
      .catch(ex => {
        console.error('ex:', ex);
      });
  },
  test_update() {
    useApi()
      .request({
        method: 'post',
        url: '/api/org/update',
        data: { org_id: 'test2', org_nm: '테스트기관22' }
      })
      .then(result => {
        console.log('result:', result);
      })
      .catch(ex => {
        console.error('ex:', ex);
      });
  },
  test_delete() {
    useApi()
      .request({
        method: 'post',
        url: '/api/org/delete',
        data: { org_id: 'test2' }
      })
      .then(result => {
        console.log('result:', result);
      })
      .catch(ex => {
        console.error('ex:', ex);
      });
  }
};
</script>
