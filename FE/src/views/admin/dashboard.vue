<template>
  <div class="flex flex-col gap-6">
    <div class="rounded-2xl bg-white p-6 shadow-sm border border-gray-100">
      <div class="text-3xl font-bold text-gray-800">后台概览</div>
      <div class="mt-3 text-gray-500 leading-7">
        这里展示系统的基础统计信息，可以帮助管理员快速了解当前用户和面料数据的整体情况。
      </div>
    </div>

    <div class="grid grid-cols-1 gap-5 md:grid-cols-2 xl:grid-cols-4">
      <div
        v-for="item in cards"
        :key="item.label"
        class="bg-white rounded-2xl p-6 shadow-sm border border-gray-100"
      >
        <div class="flex items-center justify-between">
          <div class="text-gray-500 text-sm">{{ item.label }}</div>
          <div :class="item.iconClass" class="w-10 h-10 rounded-full flex items-center justify-center text-sm font-bold">
            {{ item.icon }}
          </div>
        </div>
        <div class="text-4xl font-bold text-gray-800 mt-4">{{ item.value }}</div>
        <div class="text-sm text-gray-500 mt-3">{{ item.desc }}</div>
      </div>
    </div>

    <div class="grid grid-cols-1 gap-6 xl:grid-cols-2">
      <div class="bg-white rounded-2xl p-6 shadow-sm border border-gray-100">
        <div class="text-xl font-bold text-gray-800 mb-4">数据情况</div>
        <div class="space-y-5">
          <div v-for="item in progressList" :key="item.label">
            <div class="flex items-center justify-between text-sm mb-2">
              <span class="text-gray-700">{{ item.label }}</span>
              <span class="text-gray-500">{{ item.text }}</span>
            </div>
            <div class="h-2 bg-gray-100 rounded-full overflow-hidden">
              <div class="h-full rounded-full" :class="item.barClass" :style="{ width: `${item.percent}%` }"></div>
            </div>
            <div class="text-sm text-gray-500 mt-2 leading-6">{{ item.desc }}</div>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-2xl p-6 shadow-sm border border-gray-100">
        <div class="text-xl font-bold text-gray-800 mb-4">常用功能</div>
        <div class="grid gap-4">
          <div
            v-for="item in quickList"
            :key="item.title"
            class="rounded-xl border border-gray-100 bg-gray-50 px-4 py-4"
          >
            <div class="text-base font-semibold text-gray-800">{{ item.title }}</div>
            <div class="text-sm text-gray-500 mt-2 leading-6">{{ item.desc }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, inject, onMounted, ref } from 'vue'
import api from '@/api'

const info = inject('info')
const overview = ref({
  total_users: 0,
  total_admin_users: 0,
  total_fabrics: 0,
  active_users: 0,
})

const percentage = (value, total) => {
  if (!total) return 0
  return Math.round((value / total) * 100)
}

const inactiveUsers = computed(() => Math.max(overview.value.total_users - overview.value.active_users, 0))
const normalUsers = computed(() => Math.max(overview.value.total_users - overview.value.total_admin_users, 0))
const activeRate = computed(() => percentage(overview.value.active_users, overview.value.total_users))
const adminRate = computed(() => percentage(overview.value.total_admin_users, overview.value.total_users))

const cards = computed(() => [
  {
    label: '用户总数',
    value: overview.value.total_users,
    desc: '当前系统中的全部用户数量',
    icon: '用',
    iconClass: 'bg-blue-100 text-blue-600',
  },
  {
    label: '管理员数量',
    value: overview.value.total_admin_users,
    desc: '拥有后台管理权限的账号数量',
    icon: '管',
    iconClass: 'bg-purple-100 text-purple-600',
  },
  {
    label: '面料总数',
    value: overview.value.total_fabrics,
    desc: '当前系统中可管理的面料数量',
    icon: '料',
    iconClass: 'bg-cyan-100 text-cyan-600',
  },
  {
    label: '启用用户数',
    value: overview.value.active_users,
    desc: '目前可以正常使用系统的用户数量',
    icon: '启',
    iconClass: 'bg-green-100 text-green-600',
  },
])

const progressList = computed(() => [
  {
    label: '用户启用率',
    text: `${activeRate.value}%`,
    percent: activeRate.value,
    desc: `启用用户 ${overview.value.active_users} 人，未启用用户 ${inactiveUsers.value} 人。`,
    barClass: 'bg-green-500',
  },
  {
    label: '管理员占比',
    text: `${adminRate.value}%`,
    percent: adminRate.value,
    desc: `管理员 ${overview.value.total_admin_users} 人，普通用户 ${normalUsers.value} 人。`,
    barClass: 'bg-purple-500',
  },
  {
    label: '数据完整情况',
    text: overview.value.total_fabrics > 0 ? '较完整' : '较少',
    percent: overview.value.total_fabrics > 0 ? 80 : 20,
    desc: `当前共有 ${overview.value.total_fabrics} 条面料数据。`,
    barClass: 'bg-cyan-500',
  },
])

const quickList = computed(() => [
  {
    title: '用户管理',
    desc: `可以对 ${overview.value.total_users} 个用户进行查看、搜索、编辑和删除等操作。`,
  },
  {
    title: '面料管理',
    desc: `可以对 ${overview.value.total_fabrics} 条面料数据进行维护和状态调整。`,
  },
  {
    title: '账号状态检查',
    desc: `当前有 ${inactiveUsers.value} 个未启用用户，可以重点关注。`,
  },
])

const getOverview = async () => {
  try {
    const res = await api.adminOverview()
    if (res.data.code === 200) {
      overview.value = res.data.data
    } else {
      info('获取后台概览失败', 'error')
    }
  } catch {
    info('获取后台概览失败', 'error')
  }
}

onMounted(() => {
  getOverview()
})
</script>
