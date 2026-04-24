<template>
  <div class="w-full h-full cc bg-[url('bg1.jpg')] bg-cover">
    <div class="flex flex-col gap-6 bg-white rounded-2xl p-10 w-[30%]">
      <div class="text-3xl font-bold cc">登录</div>
      <div>
        <a-input v-model:value="username" placeholder="用户名"></a-input>
      </div>
      <div>
        <a-input v-model:value="password" type="password" placeholder="密码"></a-input>
      </div>
      <a-button type="primary" @click="login">登录</a-button>
      <div class="cc text-sm">
        没有账号？<router-link to="/register" class="text-blue-300">去注册</router-link>
      </div>
      <div class="cc text-sm text-gray-500">
        管理员可前往<router-link to="/admin/login" class="text-blue-400 ml-1">后台登录</router-link>
      </div>
    </div>
  </div>
</template>
<script setup>
import { ref, inject } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import api from '@/api'

const store = useUserStore()
const router = useRouter()
const info = inject('info')
const username = ref('admin')
const password = ref('1')

const login = () => {
  if (!username.value || !password.value) {
    info('用户名或密码不能为空', 'error')
    return
  }
  api
    .login(username.value, password.value)
    .then((res) => {
      if (res.data.code === 200) {
        localStorage.setItem('access_token', res.data.data.access)
        localStorage.setItem('refresh_token', res.data.data.refresh)
        store.update(res.data.data.user)
        router.push('/')
      } else {
        info(res.data.msg || '登录失败', 'error')
      }
    })
    .catch(() => {
      info('登录失败', 'error')
    })
}
</script>
