<template>
  <div class="px-10 pb-10">
    <div class="flex items-center gap-5">
      <div class="text-4xl font-bold text-slate-900">种类 / Category</div>
      <a-popover placement="right" :arrow="false">
        <template #content>
          <div class="w-200 grid grid-cols-6 gap-2">
            <div
              v-for="(item, index) in categories"
              :key="index"
              class="rounded-xl px-3 py-2 text-sm text-slate-600 transition hover:bg-slate-100 hover:text-slate-900 cursor-pointer"
              @click="choseCategory(item.value)"
            >
              {{ item.label }}
            </div>
          </div>
        </template>
        <button
          class="flex items-center gap-2 rounded-full border border-slate-200 bg-white px-4 py-2 text-base text-slate-600 transition hover:border-slate-300 hover:text-slate-900"
        >
          <span>{{ currentCategoryLabel ?? '点击选择种类 / Choose Category' }}</span>
          <span class="text-xs text-slate-400">▼</span>
        </button>
      </a-popover>
    </div>

    <div class="grid grid-cols-5 gap-6 mt-6">
      <button
        v-for="item in fabrics"
        :key="item.id"
        type="button"
        class="group overflow-hidden rounded-3xl border border-slate-200 bg-white text-left transition duration-200 hover:-translate-y-1 hover:border-slate-300 hover:shadow-[0_12px_30px_rgba(15,23,42,0.08)]"
        @click="goDetail(item.id)"
      >
        <div class="aspect-[4/3] overflow-hidden bg-slate-100">
          <img
            :src="`https://picsum.photos/200/200?random=${item.id}`"
            alt=""
            class="h-full w-full object-cover transition duration-500 group-hover:scale-[1.03]"
          />
        </div>
        <div class="flex flex-col gap-4 p-5">
          <div>
            <div class="line-clamp-2 text-base font-semibold leading-7 text-slate-900">
              {{ formatBilingualValue(item.title) }}
            </div>
            <div class="mt-1 text-sm text-slate-500">
              {{ formatBilingualValue(item.category_name, '未分类 / Uncategorized') }}
            </div>
          </div>

          <div class="grid grid-cols-2 gap-3 text-sm text-slate-500">
            <div class="rounded-2xl bg-slate-50 px-3 py-2">
              <div class="text-xs uppercase tracking-[0.16em] text-slate-400">国家 / Country</div>
              <div class="mt-1 text-slate-700">{{ formatBilingualValue(item.country) }}</div>
            </div>
            <div class="rounded-2xl bg-slate-50 px-3 py-2">
              <div class="text-xs uppercase tracking-[0.16em] text-slate-400">图案 / Pattern</div>
              <div class="mt-1 text-slate-700">{{ formatBilingualValue(item.pattern) }}</div>
            </div>
          </div>

          <div class="flex items-center justify-between border-t border-slate-100 pt-4">
            <div>
              <div class="text-xs uppercase tracking-[0.16em] text-slate-400">价格 / Price</div>
              <div class="mt-1 text-2xl font-semibold text-slate-900">{{ item.price }}</div>
            </div>
            <div class="text-sm text-slate-400 transition group-hover:text-slate-600">查看详情 / View Detail →</div>
          </div>
        </div>
      </button>
    </div>
  </div>
</template>
<script setup>
import api from '@/api'
import { formatBilingualValue, mapBilingualOptions } from '@/utils/bilingual'
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const categories = ref([])
const currentCategory = ref(null)
const fabrics = ref([])

const currentCategoryLabel = computed(() => {
  const matched = categories.value.find((item) => item.value === currentCategory.value)
  return matched?.label || formatBilingualValue(currentCategory.value, '')
})

const getFabrics = () => {
  api
    .fabrics({
      page: 1,
      page_size: 10,
      ordering: '-like',
      category_name: currentCategory.value,
    })
    .then((res) => {
      fabrics.value = res.data.results
    })
}

const getOptions = () => {
  api.fabricsOptions('category_name').then((res) => {
    if (res.data.code === 200) {
      categories.value = mapBilingualOptions(res.data.data)
      if (categories.value.length) {
        choseCategory(categories.value[0].value)
      }
    }
  })
}

const choseCategory = (category) => {
  currentCategory.value = category
  getFabrics()
}

const goDetail = (id) => {
  router.push(`/fabric/${id}`)
}

onMounted(() => {
  getOptions()
})
</script>
