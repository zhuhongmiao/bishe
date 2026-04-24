<template>
  <div class="p-10 flex flex-col gap-10">
    <div>
      <span class="text-2xl text-gray-700">用户名:&nbsp;</span>
      <span class="text-xl text-stone-400">{{ userStore.username }}</span>
    </div>
    <div>
      <span class="text-2xl text-gray-700">邮箱:&nbsp;</span>
      <span class="text-xl text-stone-400">{{ userStore.email }}</span>
    </div>
    <div>
      <span class="text-2xl text-gray-700">电话:&nbsp;</span>
      <span class="text-xl text-stone-400">{{ userStore.phone_number }}</span>
    </div>
    <div class="flex items-center">
      <span class="text-2xl text-gray-700">是否是管理员:&nbsp;</span>
      <a-tag color="cyan" v-if="userStore.isAdmin">管理员</a-tag>
      <a-tag color="green" v-else>普通用户</a-tag>
    </div>
    <div class="flex items-center gap-4">
      <a-button type="primary" v-if="userStore.isAdmin" @click="$router.push('/admin')">进入后台</a-button>
      <a-button type="primary" danger @click="handleLogout">退出登录</a-button>
    </div>
  </div>
</template>
<script setup>
import { useUserStore } from '@/stores/user'
import { useRouter } from 'vue-router'
const userStore = useUserStore()
const router = useRouter()
const handleLogout = () => {
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
  userStore.clear()
  router.push('/login')
}
</script>
