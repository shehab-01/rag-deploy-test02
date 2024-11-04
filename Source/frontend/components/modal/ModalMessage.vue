<template>
  <!-- Modal: alert/confirm/valid -->
  <v-dialog v-model="data.message.show" max-width="400" @keydown.esc="modal.hide()" persistent scrollable>
    <!-- <v-card :prepend-icon="data.message.opts.icon"> -->
    <v-card>
      <template v-slot:prepend v-if="data.message.opts.icon">
        <v-icon :class="classObject" style="display: inline-table">{{ data.message.opts.icon }}</v-icon>
      </template>
      <template v-slot:title>
        <div :class="classObject" v-html="data.message.opts.title"></div>
      </template>
      <template v-slot:text>
        <div v-html="data.message.opts.content"></div>
      </template>
      <v-divider v-if="false"></v-divider>
      <template v-slot:actions>
        <v-spacer></v-spacer>
        <v-btn @click="modal.cancel()" v-if="data.message.opts.buttons.cancel">{{ data.message.opts.buttons.cancel.text }}</v-btn>
        <v-btn @click="modal.ok()" v-if="data.message.opts.buttons.ok">{{ data.message.opts.buttons.ok.text }}</v-btn>
      </template>
    </v-card>
  </v-dialog>
</template>

<script setup>
const props = defineProps({
  option: {
    type: Object,
    required: false,
    default: {}
  },
  modelValue: null
});
const option = props.option;
// const emit = defineEmits(['update:modelValue']);

const env = import.meta.env;
const data = reactive({
  message: store.page().message
});
const classObject = computed(() => {
  return {
    'text-info': data.message.opts.type == 'info',
    'text-valid': data.message.opts.type == 'valid',
    'text-error': data.message.opts.type == 'error'
  };
});

onMounted(() => {
  modal.init();
});

// 모달 변경값 감시
// watch(
//   () => data.message.show,
//   (newVal, oldVal) => {
//     // console.log('watch:', newVal, oldVal);
//     if (newVal === true) {
//       modal.show();
//     } else {
//       modal.hide();
//     }
//   }
// );

const modal = {
  // _this: null,
  // 모달설정
  init: function () {
    // TODO:
    this.hide();
  },
  // 모달열기
  show: function () {
    data.message.show = true;
  },
  // 모달닫기
  hide: function () {
    data.message.show = false;
  },
  // 모달토글
  toggle: function () {
    data.message.show = !data.message.show;
  },
  /**
   * 취소
   */
  cancel: function () {
    if (isFunction(data.message.opts.buttons.cancel.action)) {
      data.message.opts.buttons.cancel.action();
    }
    this.hide();
  },
  /**
   * 확인
   */
  ok: function () {
    if (isFunction(data.message.opts.buttons.ok.action)) {
      data.message.opts.buttons.ok.action();
    }
    this.hide();
  }
};
</script>
