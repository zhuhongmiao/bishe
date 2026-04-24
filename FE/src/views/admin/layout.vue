<template>
  <div class="min-h-screen bg-[#f5f7fb]">
    <div class="fixed top-0 left-0 right-0 h-16 bg-white shadow-sm z-20 flex items-center justify-between px-8">
      <div class="flex items-center gap-3">
        <div class="text-3xl font-bold cursor-pointer" @click="$router.push('/admin')">Fabrics</div>
        <div class="text-sm text-gray-400 pt-2">后台管理系统</div>
      </div>
      <div class="flex items-center gap-4">
        <span class="text-gray-600">{{ userStore.username }}</span>
        <a-tag color="blue" v-if="userStore.isAdmin">管理员</a-tag>
        <a-button @click="goFront">返回前台</a-button>
        <a-button danger @click="logout">退出登录</a-button>
      </div>
    </div>

    <div class="flex pt-16 min-h-screen">
      <div class="w-60 bg-white border-r border-gray-200 px-4 py-6 flex flex-col gap-2">
        <div
          v-for="item in menus"
          :key="item.path"
          class="px-4 py-3 rounded-xl cursor-pointer transition-all"
          :class="route.path === item.path ? 'bg-blue-500 text-white' : 'text-gray-700 hover:bg-gray-100'"
          @click="router.push(item.path)"
        >
          {{ item.label }}
        </div>
      </div>
      <div class="flex-1 p-6 overflow-auto">
        <RouterView />
      </div>
    </div>
  </div>
</template>

<script setup>
import { RouterView, useRoute, useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const menus = [
  { label: '后台概览', path: '/admin' },
  { label: '用户管理', path: '/admin/users' },
  { label: '面料管理', path: '/admin/fabrics' },
]

const logout = () => {
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
  userStore.isLogin = false
  router.push('/admin/login')
}

const goFront = () => {
  router.push('/')
}
</script>
