<template>
  <div>
    <div v-if="editorFabric" class="flex flex-col gap-5">
      <div class="text-3xl font-bold flex items-center justify-between">
        更改面料信息 / Edit Fabric:
        <button class="text-xl font-normal text-blue-500" @click="handleClose">关闭 / Close</button>
      </div>
      <div class="flex items-center">
        <span class="text-nowrap w-28">面料名称 / Name：</span>
        <a-input v-model:value="editorFabric.title" class="w-60 mb-3" />
      </div>
      <div class="flex items-center">
        <span class="text-nowrap w-28">类别 / Category：</span>
        <a-select
          v-model:value="editorFabric.category_name"
          class="w-60 mb-3"
          :options="store.categories"
        />
      </div>
      <div class="flex items-center">
        <span class="text-nowrap w-28">国家 / Country：</span>
        <a-select
          v-model:value="editorFabric.country"
          class="w-60 mb-3"
          :options="store.countries"
        />
      </div>
      <div class="flex items-center">
        <span class="text-nowrap w-28">图案 / Pattern：</span>
        <a-select
          v-model:value="editorFabric.pattern"
          class="w-60 mb-3"
          :options="store.patterns"
        />
      </div>
      <div class="flex items-center">
        <span class="text-nowrap w-28">价格 / Price：</span>
        <a-input v-model:value="editorFabric.price" class="w-60 mb-3" />
      </div>
      <a-button type="primary" @click="handleSave">保存 / Save</a-button>
    </div>
    <div class="text-3xl font-bold mb-5">
      所有面料 / All Fabrics
      <span class="text-xl text-gray-500 ml-5">（点击面料可编辑信息 / Click to edit）</span>
    </div>
    <div class="divide-y divide-gray-300 p-2 rounded-2xl border border-gray-300">
      <div class="flex items-center gap-5 p-3 font-bold">
        <div class="flex-1">面料名称 / Fabric Name</div>
        <div class="w-30">类别 / Category</div>
        <div class="w-28">国家 / Country</div>
        <div class="w-30">图案 / Pattern</div>
        <div class="w-20">价格 / Price</div>
        <div class="w-30">操作 / Action</div>
      </div>
      <div
        v-for="item in fabrics"
        :key="item.id"
        class="flex items-center gap-5 p-3"
        @click="handleClick(item)"
      >
        <div class="flex-1">{{ item.title }}</div>
        <div class="w-30">{{ item.category_name }}</div>
        <div class="w-28">{{ item.country }}</div>
        <div class="w-30">{{ item.pattern }}</div>
        <div class="w-20">{{ item.price }}</div>
        <div class="w-30">
          <a-button type="primary" danger @click.stop="handleDelete(item.id)" :disabled="item.is_admin"
            >删除 / Delete</a-button
          >
        </div>
      </div>
    </div>
    <div class="mt-5">
      <a-pagination
        v-model:current="page"
        :total="total"
        :pageSize="pageSize"
        :showSizeChanger="false"
        @change="handlePageChange"
      />
    </div>
  </div>
</template>
<script setup>
import { ref, onMounted, inject } from 'vue'
import { useSearchStore } from '@/stores/search'
import api from '@/api'

const info = inject('info')
const store = useSearchStore()
const fabrics = ref([])
const page = ref(1)
const pageSize = ref(10)
const total_pages = ref(0)
const total = ref(0)
const getFabrics = () => {
  api
    .fabrics({
      page: page.value,
      page_size: pageSize.value,
    })
    .then((res) => {
      fabrics.value = res.data.results
      total_pages.value = res.data.total_pages
      total.value = res.data.count
    })
}
const handlePageChange = (newPage) => {
  page.value = newPage
  getFabrics()
}
const editorFabric = ref(null)
const handleClick = (item) => {
  editorFabric.value = { ...item }
}
const handleSave = () => {
  api.fabricUpdate(editorFabric.value).then((res) => {
    if (res.data.code === 200) {
      info('保存成功 / Saved', 'success')
      getFabrics()
    } else {
      info('保存失败 / Save failed', 'error')
    }
  })
}
const handleDelete = (fabric_id) => {
  api.fabricDelete(fabric_id).then((res) => {
    if (res.data.code === 200) {
      info('删除成功 / Deleted', 'success')
      getFabrics()
    } else {
      info('删除失败 / Delete failed', 'error')
    }
  })
}
const handleClose = () => {
  editorFabric.value = null
}
onMounted(() => {
  getFabrics()
})
</script>
