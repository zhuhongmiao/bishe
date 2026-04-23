<template>
  <div>
    <div v-if="editUser" class="mb-10 flex flex-col gap-5">
      <div class="text-3xl font-bold flex items-center justify-between">
        更改用户信息：
        <button class="text-xl font-normal text-blue-500" @click="handleClose">返回新增用户</button>
      </div>
      <div class="flex items-center">
        <span class="text-nowrap"> 用户名： </span>
        <a-input v-model:value="editUser.username" class="w-60" />
      </div>
      <div class="flex items-center mt-3">
        <span class="text-nowrap"> 邮箱： </span>
        <a-input v-model:value="editUser.email" class="w-60" />
      </div>
      <div class="flex items-center mt-3">
        <span class="text-nowrap"> 电话： </span>
        <a-input v-model:value="editUser.phone_number" class="w-60" />
      </div>
      <div class="mt-3">
        <span class="text-nowrap"> 是否为管理员： </span>
        <a-switch v-model:checked="editUser.is_admin" />
      </div>
      <a-button type="primary" @click="handleSave">保存</a-button>
    </div>
    <div v-else class="mb-10 flex flex-col gap-5">
      <div class="text-3xl font-bold">新增用户：</div>
      <div class="flex items-center">
        <span class="text-nowrap"> 用户名： </span>
        <a-input v-model:value="newUser.username" class="w-60" />
      </div>
      <div class="flex items-center mt-3">
        <span class="text-nowrap"> 邮箱： </span>
        <a-input v-model:value="newUser.email" class="w-60" />
      </div>
      <div class="flex items-center mt-3">
        <span class="text-nowrap"> 电话： </span>
        <a-input v-model:value="newUser.phone_number" class="w-60" />
      </div>
      <div class="flex items-center mt-3">
        <span class="text-nowrap"> 密码： </span>
        <a-input v-model:value="newUser.password" type="password" class="w-60" />
      </div>
      <div class="mt-3">
        <span class="text-nowrap"> 是否为管理员： </span>
        <a-switch v-model:checked="newUser.is_admin" />
      </div>
      <a-button type="primary" @click="handleAdd">新增</a-button>
    </div>
    <div class="text-3xl font-bold mb-5">
      所有用户
      <span class="text-xl text-gray-500 ml-5">（点击用户可编辑信息）</span>
    </div>
    <div class="divide-y divide-gray-300 p-2 rounded-2xl border border-gray-300">
      <div>
        <div class="flex items-center gap-10 p-3 font-bold">
          <div class="flex-1">用户名</div>
          <div class="w-30">邮箱</div>
          <div class="w-30">电话</div>
          <div class="w-30">身份</div>
          <div class="w-30">操作</div>
        </div>
      </div>
      <div
        v-for="item in users"
        :key="item.id"
        class="flex items-center gap-10 p-3"
        @click="handleClick(item)"
      >
        <div class="text-2xl flex-1">{{ item.username }}</div>
        <div class="w-30">{{ item.email || '无' }}</div>
        <div class="w-30">{{ item.phone_number || '无' }}</div>
        <div class="w-30">
          <a-tag v-if="item.is_admin" color="blue">管理员</a-tag>
          <a-tag v-else color="green">普通用户</a-tag>
        </div>
        <div class="w-30">
          <a-button
            type="primary"
            danger
            @click.stop="handleDelete(item.id)"
            :disabled="item.is_admin"
            >删除</a-button
          >
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
import { onMounted, ref, inject } from 'vue'
import api from '@/api'

const info = inject('info')
const users = ref([])
const editUser = ref(null)
const newUser = ref({ username: '', password: '', is_admin: false, email: '', phone_number: '' })
const handleClick = (user) => {
  editUser.value = { ...user }
}
const getUsers = () => {
  api.userSearch().then((res) => {
    console.log(res)
    if (res.data.code === 200) {
      users.value = res.data.data
    } else {
      info('获取用户列表失败', 'error')
    }
  })
}
const handleSave = () => {
  api.userUpdate(editUser.value).then((res) => {
    console.log(res)
    if (res.data.code === 200) {
      info('保存成功', 'success')
      getUsers()
    } else {
      info('保存失败', 'error')
    }
  })
}
const handleDelete = (user_id) => {
  api.userDelete(user_id).then((res) => {
    console.log(res)
    if (res.data.code === 200) {
      info('删除成功', 'success')
      getUsers()
    } else {
      info('删除失败', 'error')
    }
  })
}
const handleAdd = () => {
  api
    .register(newUser.value.username, newUser.value.password, newUser.value.email, newUser.value.phone_number, newUser.value.is_admin)
    .then((res) => {
      if (res.data.code === 200) {
        info('新增成功', 'success')
        newUser.value = { username: '', password: '', email: '', phone_number: '', is_admin: false }
        getUsers()
      } else {
        info(res.data.msg, 'error')
      }
    })
}
const handleClose = () => {
  editUser.value = null
}
onMounted(() => {
  getUsers()
})
</script>
