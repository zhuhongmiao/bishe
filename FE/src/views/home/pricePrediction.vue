<template>
  <div class="w-screen h-full flex justify-center items-start pt-16 pb-12 px-4 md:px-10 bg-gray-50">
    <div class="w-full md:w-3/4 lg:w-3/4 max-w-5xl bg-white rounded-2xl shadow p-8 md:p-10">
      <h1 class="text-2xl font-bold mb-4">布料价格预测</h1>

      <p class="text-gray-600 mb-8 leading-relaxed text-sm md:text-base">
        根据已有数据中的面料特征（种类、国家、图案、克重），使用训练好的模型预测布料价格。
        下拉选项均来自历史数据，可以减少输入错误，让预测更加可靠。
      </p>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
        <div>
          <div class="mb-2 font-medium">面料种类</div>
          <a-select
            v-model:value="form.category_name"
            :options="categoryOptions"
            show-search
            allow-clear
            :filter-option="filterOption"
            placeholder="请选择面料种类"
            :dropdown-style="{ maxHeight: '400px', overflow: 'auto' }"
            :virtual="false"
          />
        </div>

        <div>
          <div class="mb-2 font-medium">所属国家</div>
          <a-select
            v-model:value="form.country"
            :options="countryOptions"
            show-search
            allow-clear
            :filter-option="filterOption"
            placeholder="请选择国家"
            :dropdown-style="{ maxHeight: '400px', overflow: 'auto' }"
            :virtual="false"
          />
        </div>

        <div>
          <div class="mb-2 font-medium">图案类型</div>
          <a-select
            v-model:value="form.pattern"
            :options="patternOptions"
            show-search
            allow-clear
            :filter-option="filterOption"
            placeholder="请选择图案类型"
            :dropdown-style="{ maxHeight: '400px', overflow: 'auto' }"
            :virtual="false"
          />
        </div>

        <div>
          <div class="mb-2 font-medium">克重（g/m²）</div>
          <div class="flex items-center gap-3">
            <a-input-number
              v-model:value="form.weight"
              :min="weightRange.min"
              :max="weightRange.max"
              class="w-full"
              :step="1"
              placeholder="请选择或输入克重"
            />
          </div>
          <div v-if="weightRange.min !== null" class="mt-1 text-xs text-gray-500">
            数据范围：{{ weightRange.min.toFixed(0) }} ~ {{ weightRange.max.toFixed(0) }} g/m²，
            建议值：约 {{ weightRange.median.toFixed(0) }} g/m²
          </div>
        </div>
      </div>

      <div class="flex flex-col md:flex-row md:items-center gap-4 mb-4">
        <a-button type="primary" :loading="loading" :disabled="loading || loadingOptions" @click="onPredict">
          {{ loading ? '预测中...' : '开始预测' }}
        </a-button>
        <span v-if="result !== null" class="text-lg">
          预测价格：
          <span class="text-blue-500 font-bold text-2xl">{{ formattedResult }}</span>
        </span>
        <span v-if="loading" class="text-sm text-gray-500">
          正在预测，请稍候...
        </span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, inject, computed, onMounted } from 'vue'
import api from '@/api'

const info = inject('info')

const form = reactive({
  category_name: '',
  country: '',
  pattern: '',
  weight: null,
})

const options = reactive({
  categories: [],
  countries: [],
  patterns: [],
})

const weightRange = reactive({
  min: null,
  max: null,
  median: null,
})

const loading = ref(false)
const loadingOptions = ref(false)
const result = ref(null)

const formattedResult = computed(() => {
  if (result.value === null) return ''
  return `￥${Number(result.value).toFixed(2)}`
})

const categoryOptions = computed(() =>
  options.categories.map((v) => ({
    label: v,
    value: v,
  })),
)

const countryOptions = computed(() =>
  options.countries.map((v) => ({
    label: v,
    value: v,
  })),
)

const patternOptions = computed(() =>
  options.patterns.map((v) => ({
    label: v,
    value: v,
  })),
)

const filterOption = (input, option) =>
  (option?.label ?? '').toLowerCase().includes(input.toLowerCase())

const loadOptions = () => {
  loadingOptions.value = true
  api
    .getPricePredictOptions()
    .then((res) => {
      if (res.data.code === 200) {
        const d = res.data.data || {}
        options.categories = d.category_names || []
        options.countries = d.countries || []
        options.patterns = d.patterns || []
        weightRange.min = typeof d.weight_min === 'number' ? d.weight_min : null
        weightRange.max = typeof d.weight_max === 'number' ? d.weight_max : null
        weightRange.median = typeof d.weight_median === 'number' ? d.weight_median : null

        if (form.weight === null && weightRange.median !== null) {
          form.weight = Number(weightRange.median.toFixed(0))
        }
      } else {
        info(res.data.msg || '加载选项失败', 'error')
      }
    })
    .catch(() => {
      info('加载选项失败，请稍后重试', 'error')
    })
    .finally(() => {
      loadingOptions.value = false
    })
}

const onPredict = () => {
  if (!form.category_name || !form.country || !form.pattern || form.weight === null) {
    info('请完整填写所有字段', 'warning')
    return
  }

  loading.value = true
  result.value = null

  api
    .predictPrice({
      category_name: form.category_name,
      country: form.country,
      pattern: form.pattern,
      weight: form.weight,
    })
    .then((res) => {
      if (res.data.code === 200) {
        result.value = res.data.data.price
      } else {
        info(res.data.msg || '预测失败', 'error')
      }
    })
    .catch(() => {
      info('预测请求失败，请稍后重试', 'error')
    })
    .finally(() => {
      loading.value = false
    })
}

onMounted(() => {
  loadOptions()
})
</script>
