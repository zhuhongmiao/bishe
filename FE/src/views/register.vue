<template>
  <div class="w-full h-full cc bg-[url('bg1.jpg')] bg-cover">
    <div class="flex flex-col gap-6 bg-white rounded-2xl p-10 w-[30%]">
      <div class="text-3xl font-bold cc">注册</div>
      <div>
        <a-input v-model:value="username" placeholder="用户名"></a-input>
      </div>
      <div>
        <a-input v-model:value="email" placeholder="邮箱"></a-input>
      </div>
      <div>
        <a-input v-model:value="phone_number" placeholder="电话"></a-input>
      </div>
      <div>
        <a-input v-model:value="password" type="password" placeholder="密码"></a-input>
      </div>
      <a-button type="primary" @click="register">注册</a-button>
      <div class="cc text-sm">
        已有账号？<router-link to="/login" class="text-blue-300">去登录</router-link>
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
const username = ref('')
const password = ref('')
const email = ref('')
const phone_number = ref('')

const register = () => {
  if (!username.value || !password.value) {
    info('用户名或密码不能为空', 'error')
    return
  }
  api.register(username.value, password.value, email.value, phone_number.value).then((res) => {
    console.log(res)
    if (res.data.code === 200) {
      info(res.data.msg, 'success')
      router.push('/login')
    }else{
      info(res.data.msg,'error')
    }
  })
}
</script>
