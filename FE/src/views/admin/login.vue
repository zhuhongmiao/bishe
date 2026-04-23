<template>
  <div class="w-full h-full cc bg-[url('bg1.jpg')] bg-cover">
    <div class="flex flex-col gap-6 bg-white rounded-2xl p-10 w-[32%] shadow-xl">
      <div class="text-3xl font-bold cc">后台登录</div>
      <div>
        <a-input v-model:value="username" placeholder="管理员用户名" />
      </div>
      <div>
        <a-input v-model:value="password" type="password" placeholder="密码" />
      </div>
      <a-button type="primary" @click="handleLogin">登录后台</a-button>
      <div class="cc text-sm text-gray-500">
        登录后可进行用户与面料数据管理
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, inject } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import api from '@/api'

const router = useRouter()
const userStore = useUserStore()
const info = inject('info')

const username = ref('admin')
const password = ref('1')

const handleLogin = async () => {
  if (!username.value || !password.value) {
    info('用户名或密码不能为空', 'error')
    return
  }

  try {
    const res = await api.login(username.value, password.value)
    if (res.data.code !== 200) {
      info(res.data.msg || '登录失败', 'error')
      return
    }

    const user = res.data.data.user
    if (!user.is_admin) {
      info('当前账号不是管理员，无法进入后台', 'error')
      return
    }

    localStorage.setItem('access_token', res.data.data.access)
    localStorage.setItem('refresh_token', res.data.data.refresh)
    userStore.update(user)
    router.push('/admin')
  } catch {
    info('后台登录失败', 'error')
  }
}
</script>
