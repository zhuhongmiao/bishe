<template>
  <div class="flex items-center justify-between px-10 py-3 mx-5 bg-white rounded-2xl w-[95%]">
    <div>筛选条件</div>
    <a-select
      v-model:value="store.category_name"
      style="width: 200px"
      :options="store.categories"
      placeholder="全部种类"
      allowClear
    ></a-select>
    <a-select
      v-model:value="store.pattern"
      style="width: 200px"
      :options="store.patterns"
      placeholder="全部图案"
      allowClear
    ></a-select>
    <a-select
      v-model:value="store.country"
      style="width: 200px"
      :options="store.countries"
      placeholder="全部国家"
      allowClear
    ></a-select>
    <a-select
      v-model:value="store.order"
      style="width: 200px"
      :options="store.orders"
      placeholder="请选择排序方式"
      allowClear
    ></a-select>
    <div>
      <a-button type="primary" @click="store.search()">搜索</a-button>
    </div>
  </div>
</template>
<script setup>
import { useSearchStore } from '@/stores/search'
const store = useSearchStore()
</script>
