import { ref } from 'vue'
import { defineStore } from 'pinia'
import api from '@/api'

export const useUserStore = defineStore('user', () => {
  const id = ref(null)
  const username = ref('')
  const email = ref('')
  const phone_number = ref('')
  const isAdmin = ref(false)
  const isLogin = ref(false)

  const update = (data) => {
    id.value = data.id
    username.value = data.username
    email.value = data.email
    phone_number.value = data.phone_number
    isAdmin.value = data.is_admin
    isLogin.value = true
  }

  const clear = () => {
    id.value = null
    username.value = ''
    email.value = ''
    phone_number.value = ''
    isAdmin.value = false
    isLogin.value = false
  }

  const init = async () => {
    let res
    try {
      res = await api.tokenVerify()
    } catch {
      clear()
      return
    }

    if (res.data.code === 200) {
      update(res.data.data)
    } else {
      clear()
    }
  }

  return { id, username, email, phone_number, isAdmin, isLogin, update, clear, init }
})
