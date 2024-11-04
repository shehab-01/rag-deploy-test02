import { defineStore } from 'pinia';
import { ref, computed } from 'vue';

// 1) Options API
export const useCounterStore = defineStore('counter', {
  state: () => ({ count: 0, name: 'test-counter' }),
  getters: {
    doubleCount: state => state.count * 2
  },
  actions: {
    increment() {
      this.count++;
    }
  }
});

// 2) Setup API
// export const useCounterStore = defineStore('counter', () => {
//   const count = ref(0);
//   const name = ref('test-counter');
//   const doubleCount = computed(() => count.value * 2);
//   function increment() {
//     count.value++;
//   }
//   return { count, doubleCount, increment };
// });
