<template>
  <div class="flex flex-col gap-6">
    <div class="flex items-center justify-between">
      <div class="text-3xl font-bold">面料管理</div>
      <div class="flex items-center gap-3 flex-wrap">
        <a-button danger :disabled="selectedRowKeys.length === 0" @click="handleBatchDelete">批量删除</a-button>
        <a-button type="primary" @click="openCreate">新增面料</a-button>
      </div>
    </div>

    <div class="bg-white rounded-2xl p-5 border border-gray-100 shadow-sm flex items-center gap-4 flex-wrap">
      <a-input v-model:value="query.keyword" placeholder="面料名称/类别/国家/图案搜索" class="!w-80" />
      <a-input v-model:value="query.category_name" placeholder="类别" class="!w-40" />
      <a-input v-model:value="query.country" placeholder="国家" class="!w-40" />
      <a-input v-model:value="query.pattern" placeholder="图案" class="!w-40" />
      <a-select v-model:value="query.ordering" class="!w-44" :options="orderOptions" />
      <a-button type="primary" @click="fetchFabrics">查询</a-button>
      <a-button @click="resetQuery">重置</a-button>
    </div>

    <div class="bg-white rounded-2xl p-4 border border-gray-100 shadow-sm">
      <a-table
        :dataSource="fabrics"
        :columns="columns"
        :pagination="false"
        rowKey="id"
        :scroll="{ x: 1200 }"
        :row-selection="rowSelection"
      >
        <template #bodyCell="{ column, record }">
          <template v-if="column.key === 'action'">
            <div class="flex items-center gap-2">
              <a-button size="small" type="primary" @click="openEdit(record)">编辑</a-button>
              <a-button size="small" danger @click="handleDelete(record)">删除</a-button>
            </div>
          </template>
        </template>
      </a-table>
      <div class="flex justify-end mt-4">
        <a-pagination
          v-model:current="pagination.page"
          :total="pagination.total"
          :pageSize="pagination.page_size"
          :showSizeChanger="false"
          @change="handlePageChange"
        />
      </div>
    </div>

    <a-modal v-model:open="modalOpen" :title="editingId ? '编辑面料' : '新增面料'" @ok="submitForm" width="760px">
      <div class="grid grid-cols-2 gap-4 pt-4">
        <a-input v-model:value="form.title" placeholder="面料名称" />
        <a-input v-model:value="form.category_name" placeholder="类别名称" />
        <a-input-number v-model:value="form.category_id" placeholder="类别ID" class="!w-full" />
        <a-input-number v-model:value="form.weight" placeholder="重量" class="!w-full" />
        <a-input v-model:value="form.country" placeholder="国家" />
        <a-input-number v-model:value="form.price" placeholder="价格" class="!w-full" :min="0" :step="0.01" />
        <a-input v-model:value="form.pattern" placeholder="图案" />
        <a-input-number v-model:value="form.like" placeholder="点赞数" class="!w-full" :min="0" />
      </div>
    </a-modal>
  </div>
</template>

<script setup>
import { computed, inject, onMounted, ref } from 'vue'
import { Modal } from 'ant-design-vue'
import api from '@/api'

const info = inject('info')
const fabrics = ref([])
const modalOpen = ref(false)
const editingId = ref(null)
const selectedRowKeys = ref([])

const query = ref({
  keyword: '',
  category_name: '',
  country: '',
  pattern: '',
  ordering: 'id',
})

const pagination = ref({
  page: 1,
  page_size: 10,
  total: 0,
})

const form = ref({
  title: '',
  category_name: '',
  category_id: 0,
  weight: null,
  country: '',
  price: 0,
  pattern: '',
  like: 0,
})

const orderOptions = [
  { label: '最早创建', value: 'id' },
  { label: '最新创建', value: '-id' },
  { label: '价格升序', value: 'price' },
  { label: '价格降序', value: '-price' },
  { label: '重量升序', value: 'weight' },
  { label: '重量降序', value: '-weight' },
  { label: '点赞升序', value: 'like' },
  { label: '点赞降序', value: '-like' },
]

const columns = [
  { title: 'ID', dataIndex: 'id', key: 'id', width: 80 },
  { title: '面料名称 / Fabric Name', dataIndex: 'title', key: 'title', width: 240 },
  { title: '类别 / Category', dataIndex: 'category_name', key: 'category_name', width: 180 },
  { title: '类别ID / Category ID', dataIndex: 'category_id', key: 'category_id', width: 120 },
  { title: '重量 / Weight', dataIndex: 'weight', key: 'weight', width: 110 },
  { title: '国家 / Country', dataIndex: 'country', key: 'country', width: 160 },
  { title: '价格 / Price', dataIndex: 'price', key: 'price', width: 100 },
  { title: '图案 / Pattern', dataIndex: 'pattern', key: 'pattern', width: 180 },
  { title: '点赞 / Likes', dataIndex: 'like', key: 'like', width: 100 },
  { title: '操作', key: 'action', width: 180, fixed: 'right' },
]

const rowSelection = computed(() => ({
  selectedRowKeys: selectedRowKeys.value,
  onChange: (keys) => {
    selectedRowKeys.value = keys
  },
}))

const fetchFabrics = async () => {
  try {
    const res = await api.adminFabrics({
      ...query.value,
      page: pagination.value.page,
      page_size: pagination.value.page_size,
    })
    fabrics.value = res.data.results || []
    pagination.value.total = res.data.count || 0
  } catch {
    info('获取面料列表失败', 'error')
  }
}

const resetQuery = () => {
  query.value = {
    keyword: '',
    category_name: '',
    country: '',
    pattern: '',
    ordering: 'id',
  }
  pagination.value.page = 1
  fetchFabrics()
}

const handlePageChange = (page) => {
  pagination.value.page = page
  fetchFabrics()
}

const resetForm = () => {
  form.value = {
    title: '',
    category_name: '',
    category_id: 0,
    weight: null,
    country: '',
    price: 0,
    pattern: '',
    like: 0,
  }
}

const openCreate = () => {
  editingId.value = null
  resetForm()
  modalOpen.value = true
}

const openEdit = (record) => {
  editingId.value = record.id
  form.value = {
    title: record.title,
    category_name: record.category_name,
    category_id: record.category_id,
    weight: record.weight,
    country: record.country,
    price: Number(record.price),
    pattern: record.pattern,
    like: record.like,
  }
  modalOpen.value = true
}

const submitForm = async () => {
  try {
    if (!form.value.title || !form.value.category_name) {
      info('面料名称和类别不能为空', 'warning')
      return
    }

    if (editingId.value) {
      const res = await api.adminUpdateFabric(editingId.value, form.value)
      if (res.data.code === 200) {
        info('面料更新成功', 'success')
      } else {
        info(res.data.msg || '面料更新失败', 'error')
        return
      }
    } else {
      const res = await api.adminCreateFabric(form.value)
      if (res.data.code === 200) {
        info('面料新增成功', 'success')
      } else {
        info(res.data.msg || '面料新增失败', 'error')
        return
      }
    }

    modalOpen.value = false
    fetchFabrics()
  } catch {
    info('保存面料失败', 'error')
  }
}

const handleDelete = (record) => {
  Modal.confirm({
    title: '确认删除该面料吗？',
    content: `面料名称：${record.title}`,
    okText: '确认删除',
    cancelText: '取消',
    async onOk() {
      try {
        const res = await api.adminDeleteFabric(record.id)
        if (res.data.code === 200) {
          info('面料删除成功', 'success')
          fetchFabrics()
        } else {
          info(res.data.msg || '面料删除失败', 'error')
        }
      } catch {
        info('面料删除失败', 'error')
      }
    },
  })
}

const handleBatchDelete = () => {
  Modal.confirm({
    title: '确认批量删除选中的面料吗？',
    okText: '确认删除',
    cancelText: '取消',
    async onOk() {
      try {
        const res = await api.adminBatchFabrics({ action: 'delete', ids: selectedRowKeys.value })
        if (res.data.code === 200) {
          info('批量删除成功', 'success')
          selectedRowKeys.value = []
          fetchFabrics()
        } else {
          info(res.data.msg || '批量删除失败', 'error')
        }
      } catch {
        info('批量删除失败', 'error')
      }
    },
  })
}

onMounted(() => {
  fetchFabrics()
})
</script>
