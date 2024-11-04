<template>
  <div class="" v-if="option.type == 'select'">
    <v-select
      :color="props.color"
      :id="props.name"
      :name="props.name"
      :class="props.class"
      :style="props.style"
      :disabled="option.disabled"
      :items="data.codes"
      item-title="val"
      item-value="key"
      label="선택"
      v-model="value"
      single-line
      @change="$emit('change', $event, $event.target.value)"
    ></v-select>
  </div>

  <div class="" v-else-if="option.type == 'radio'">
    <v-radio-group v-model="value" :inline="true">
      <template v-for="(code, idx) in data.codes" :key="idx">
        <v-radio
          :color="props.color"
          :id="props.name + '-' + idx"
          :name="props.name"
          :label="code.val"
          :value="code.key"
          v-model="value"
          @change="$emit('change', $event, $event.target.value)"
        ></v-radio>
      </template>
    </v-radio-group>
  </div>

  <div class="" v-else-if="option.type == 'checkbox'">
    <v-row class="">
      <template v-for="(code, idx) in data.codes" :key="idx">
        <v-checkbox
          :color="props.color"
          :id="props.name + '-' + idx"
          :name="props.name"
          :label="code.val"
          :value="code.key"
          v-model="value"
          multiple
          @change="comp.change($event, $event.target.value)"
        ></v-checkbox>
      </template>
    </v-row>
  </div>
</template>

<script setup lang="ts">
const data = reactive({
  codes: []
});

// MEMO: 상위 컴포넌트에서 설정한 v-model은 modelValue 로 설정된다.
const props = defineProps({
  idx: {
    type: Number,
    required: false
  },
  name: {
    type: String,
    required: true
  },
  color: {
    type: String,
    required: false
  },
  class: {
    type: String,
    required: false
  },
  style: {
    type: Object,
    required: false
  },
  option: {
    type: Object,
    required: true
  },
  modelValue: null
});
const emit = defineEmits(['load', 'change', 'update:modelValue']);

/**
 * 변경값 감지
 * @input="$emit('update:modelValue', $event.target.value)"
 * @input="$emit('update:modelValue', $event.target.checked)"
 */
const value = computed({
  get() {
    return props.modelValue;
  },
  set(value) {
    // console.log('computed.value:', value);
    emit('update:modelValue', value);
  }
});

const option = props.option;

// 파라미터 변경시 재검색
watch(
  () => props.option.param,
  (newVal, oldVal) => {
    if (!newVal.compare(oldVal)) {
      comp.search();
    }
  }
);

const comp = {
  init: function () {
    this.search();
  },
  search: function () {
    // 목록초기화
    data.codes = [];

    // 코드목록
    let first = {};
    if (option.all) {
      first = { key: '', val: option.all };
      data.codes.push(first);
    }

    // 코드필터
    let filter = [];
    if (option.filter) {
      filter = option.filter;
    }

    // 공통코드
    if (option.code) {
      let codeInfo = max.storage.session.get('codeInfo');
      if (codeInfo != null) {
        let code = codeInfo[option.code];
        for (let key in code) {
          if (filter.length > 0) {
            if (!filter.contain(key)) {
              continue;
            }
          }
          data.codes.push({ key: key, val: code[key] });
        }
        // console.log(data.codes);
      }
    }
    // 업무코드
    else if (option.biz) {
      // console.log(option.biz);
      let param = Object.assign({ code_biz: option.biz }, props.option.param);

      useApi()
        .request({
          method: 'post',
          url: '/api/code/biz',
          data: param
        })
        .then((result: ApiResponse) => {
          let list: Array<{ key: string; val: string }> = result.data || [];
          list.forEach(code => {
            if (filter.length > 0) {
              if (!filter.contain(code.key)) {
                return true;
              }
            }
            data.codes.push(code);
          });
        });
    }
    // 입력데이터
    else if (option.data) {
      for (let key in option.data) {
        data.codes.push({ key: key, val: option.data[key] });
      }
    }

    // load data
    emit('load', toRaw(data.codes));
  },
  change: function (evt: Event, val: string) {
    // 체크박스인 경우
    if (option.type == 'checkbox') {
      if (option.all) {
        // 전체선택 체크시
        if (val == '' && evt.target instanceof HTMLInputElement) {
          let checked = evt.target.checked;
          let checkEl = document.querySelectorAll('input[type=checkbox][name=' + evt.target.name + ']');
          checkEl.forEach(function (el: Element, idx) {
            if (idx > 0) {
              if (el instanceof HTMLInputElement) {
                el.disabled = checked;
                el.checked = false;
              }
            }
            if (checked) {
              value.value = [''];
            }
          });
        }
      }
    }

    // change data
    emit('change', evt, val);
  }
};

onMounted(() => {
  comp.init();
});
</script>
