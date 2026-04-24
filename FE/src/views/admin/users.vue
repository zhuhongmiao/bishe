<template>
  <div class="flex flex-col gap-6">
    <div class="flex items-center justify-between">
      <div class="text-3xl font-bold">用户管理</div>
      <div class="flex items-center gap-3">
        <a-button :disabled="selectedRowKeys.length === 0" @click="handleBatch('enable')">批量启用</a-button>
        <a-button :disabled="selectedRowKeys.length === 0" @click="handleBatch('disable')">批量禁用</a-button>
        <a-button danger :disabled="selectedRowKeys.length === 0" @click="handleBatch('delete')">批量删除</a-button>
        <a-button type="primary" @click="openCreate">新增用户</a-button>
      </div>
    </div>

    <div class="bg-white rounded-2xl p-5 border border-gray-100 shadow-sm flex items-center gap-4 flex-wrap">
      <a-input v-model:value="query.keyword" placeholder="用户名/邮箱/电话搜索" class="!w-72" />
      <a-select v-model:value="query.is_admin" class="!w-40" :options="adminOptions" placeholder="管理员状态" allow-clear />
      <a-select v-model:value="query.is_active" class="!w-40" :options="activeOptions" placeholder="启用状态" allow-clear />
      <a-button type="primary" @click="fetchUsers">查询</a-button>
      <a-button @click="resetQuery">重置</a-button>
    </div>

    <div class="bg-white rounded-2xl p-4 border border-gray-100 shadow-sm">
      <a-table :dataSource="users" :columns="columns" :pagination="false" rowKey="id" :row-selection="rowSelection">
        <template #bodyCell="{ column, record }">
          <template v-if="column.key === 'is_admin'">
            <a-tag :color="record.is_admin ? 'blue' : 'green'">{{ record.is_admin ? '管理员' : '普通用户' }}</a-tag>
          </template>
          <template v-else-if="column.key === 'is_active'">
            <a-tag :color="record.is_active ? 'success' : 'default'">{{ record.is_active ? '启用' : '禁用' }}</a-tag>
          </template>
          <template v-else-if="column.key === 'action'">
            <div class="flex items-center gap-2 flex-wrap">
              <a-button size="small" type="primary" @click="openEdit(record)">编辑</a-button>
              <a-button size="small" @click="openResetPassword(record)">重置密码</a-button>
              <a-button size="small" danger @click="handleDelete(record)">删除</a-button>
            </div>
          </template>
        </template>
      </a-table>
      <div class="flex justify-end mt-4">
        <a-pagination v-model:current="pagination.page" :total="pagination.total" :pageSize="pagination.page_size" :showSizeChanger="false" @change="handlePageChange" />
      </div>
    </div>

    <a-modal v-model:open="modalOpen" :title="editingId ? '编辑用户' : '新增用户'" @ok="submitForm">
      <div class="flex flex-col gap-4 pt-4">
        <a-input v-model:value="form.username" placeholder="用户名" />
        <a-input v-model:value="form.email" placeholder="邮箱" />
        <a-input v-model:value="form.phone_number" placeholder="电话" />
        <a-input-password v-model:value="form.password" :placeholder="editingId ? '不修改密码可留空' : '密码'" />
        <div class="flex items-center justify-between">
          <span>是否管理员</span>
          <a-switch v-model:checked="form.is_admin" />
        </div>
        <div class="flex items-center justify-between">
          <span>是否启用</span>
          <a-switch v-model:checked="form.is_active" />
        </div>
      </div>
    </a-modal>

    <a-modal v-model:open="passwordModalOpen" title="重置密码" @ok="submitResetPassword">
      <div class="pt-4">
        <a-input-password v-model:value="resetPasswordForm.password" placeholder="请输入新密码" />
      </div>
    </a-modal>
  </div>
</template>

<script setup>
import { computed, inject, onMounted, ref } from 'vue'
import { Modal } from 'ant-design-vue'
import { useUserStore } from '@/stores/user'
import api from '@/api'

const info = inject('info')
const userStore = useUserStore()
const users = ref([])
const modalOpen = ref(false)
const passwordModalOpen = ref(false)
const editingId = ref(null)
const resettingUserId = ref(null)
const selectedRowKeys = ref([])

const query = ref({
  keyword: '',
  is_admin: undefined,
  is_active: undefined,
})

const pagination = ref({
  page: 1,
  page_size: 10,
  total: 0,
})

const form = ref({
  username: '',
  email: '',
  phone_number: '',
  password: '',
  is_admin: false,
  is_active: true,
})

const resetPasswordForm = ref({
  password: '',
})

const adminOptions = [
  { label: '管理员', value: 'true' },
  { label: '普通用户', value: 'false' },
]

const activeOptions = [
  { label: '启用', value: 'true' },
  { label: '禁用', value: 'false' },
]

const columns = [
  { title: 'ID', dataIndex: 'id', key: 'id', width: 80 },
  { title: '用户名', dataIndex: 'username', key: 'username' },
  { title: '邮箱', dataIndex: 'email', key: 'email' },
  { title: '电话', dataIndex: 'phone_number', key: 'phone_number' },
  { title: '身份', dataIndex: 'is_admin', key: 'is_admin', width: 120 },
  { title: '状态', dataIndex: 'is_active', key: 'is_active', width: 120 },
  { title: '操作', key: 'action', width: 260 },
]

const rowSelection = computed(() => ({
  selectedRowKeys: selectedRowKeys.value,
  onChange: (keys) => {
    selectedRowKeys.value = keys
  },
}))

const getErrorMessage = (res, fallback) => {
  const data = res?.data?.data
  if (!data || typeof data !== 'object') {
    return res?.data?.msg || fallback
  }
  const firstKey = Object.keys(data)[0]
  const firstValue = data[firstKey]
  if (Array.isArray(firstValue) && firstValue.length > 0) {
    return firstValue[0]
  }
  if (typeof firstValue === 'string') {
    return firstValue
  }
  return res?.data?.msg || fallback
}

const getResponseCode = (res) => {
  if (typeof res?.data?.code === 'number') {
    return res.data.code
  }
  if (typeof res?.status === 'number') {
    return res.status
  }
  return undefined
}

const fetchUsers = async () => {
  try {
    const res = await api.adminUsers({
      ...query.value,
      page: pagination.value.page,
      page_size: pagination.value.page_size,
    })
    users.value = res.data.results || []
    pagination.value.total = res.data.count || 0
  } catch {
    info('获取用户列表失败', 'error')
  }
}

const resetQuery = () => {
  query.value = { keyword: '', is_admin: undefined, is_active: undefined }
  pagination.value.page = 1
  fetchUsers()
}

const handlePageChange = (page) => {
  pagination.value.page = page
  fetchUsers()
}

const resetForm = () => {
  form.value = {
    username: '',
    email: '',
    phone_number: '',
    password: '',
    is_admin: false,
    is_active: true,
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
    username: record.username || '',
    email: record.email || '',
    phone_number: record.phone_number || '',
    password: '',
    is_admin: !!record.is_admin,
    is_active: !!record.is_active,
  }
  modalOpen.value = true
}

const openResetPassword = (record) => {
  resettingUserId.value = record.id
  resetPasswordForm.value.password = ''
  passwordModalOpen.value = true
}

const submitResetPassword = async () => {
  if (!resetPasswordForm.value.password) {
    info('新密码不能为空', 'warning')
    return
  }
  try {
    const res = await api.adminResetUserPassword(resettingUserId.value, resetPasswordForm.value.password)
    if (getResponseCode(res) === 200) {
      info('密码重置成功', 'success')
      passwordModalOpen.value = false
    } else {
      info(getErrorMessage(res, '密码重置失败'), 'error')
    }
  } catch {
    info('密码重置失败', 'error')
  }
}

const submitForm = async () => {
  try {
    if (!form.value.username) {
      info('用户名不能为空', 'warning')
      return
    }
    if (!editingId.value && !form.value.password) {
      info('新增用户时密码不能为空', 'warning')
      return
    }
    if (editingId.value === userStore.id && form.value.is_active === false) {
      info('不能禁用当前登录管理员', 'warning')
      return
    }

    const payload = {
      username: form.value.username,
      email: form.value.email || null,
      phone_number: form.value.phone_number || null,
      is_admin: form.value.is_admin,
      is_active: form.value.is_active,
    }

    if (form.value.password) {
      payload.password = form.value.password
    }

    if (editingId.value) {
      const res = await api.adminUpdateUser(editingId.value, payload)
      if (getResponseCode(res) === 200) {
        info('用户更新成功', 'success')
      } else {
        info(getErrorMessage(res, '用户更新失败'), 'error')
        return
      }
    } else {
      const res = await api.adminCreateUser(payload)
      if (getResponseCode(res) === 200) {
        info('用户新增成功', 'success')
      } else {
        info(getErrorMessage(res, '用户新增失败'), 'error')
        return
      }
    }

    modalOpen.value = false
    fetchUsers()
  } catch {
    info('保存用户失败', 'error')
  }
}

const handleDelete = (record) => {
  Modal.confirm({
    title: '确认删除该用户吗？',
    content: `用户名：${record.username}`,
    okText: '确认删除',
    cancelText: '取消',
    async onOk() {
      try {
        const res = await api.adminDeleteUser(record.id)
        if (getResponseCode(res) === 200) {
          info(res?.data?.msg || '用户删除成功', 'success')
          selectedRowKeys.value = selectedRowKeys.value.filter((id) => id !== record.id)
          fetchUsers()
        } else {
          info(getErrorMessage(res, '用户删除失败'), 'error')
        }
      } catch (error) {
        info(error?.response?.data?.msg || '用户删除失败', 'error')
      }
    },
  })
}

const handleBatch = (action) => {
  const textMap = {
    enable: '批量启用',
    disable: '批量禁用',
    delete: '批量删除',
  }
  Modal.confirm({
    title: `确认${textMap[action]}选中的用户吗？`,
    okText: '确认',
    cancelText: '取消',
    async onOk() {
      try {
        const res = await api.adminBatchUsers({ action, ids: selectedRowKeys.value })
        if (getResponseCode(res) === 200) {
          info(res.data.msg || '批量操作成功', 'success')
          selectedRowKeys.value = []
          fetchUsers()
        } else {
          info(getErrorMessage(res, '批量操作失败'), 'error')
        }
      } catch (error) {
        info(error?.response?.data?.msg || '批量操作失败', 'error')
      }
    },
  })
}

onMounted(() => {
  fetchUsers()
})
</script>
