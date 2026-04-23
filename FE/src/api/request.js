import axios from 'axios'
import { useUserStore } from '@/stores/user'

const request = axios.create({
  baseURL: import.meta.env.VITE_APP_BASE_API_URL,
})

let isRefreshing = false
let subscribers = []

function onRefreshed(token) {
  subscribers.forEach((callback) => callback(token))
  subscribers = []
}

function addSubscriber(callback) {
  subscribers.push(callback)
}

request.interceptors.request.use(
  (config) => {
    const access = localStorage.getItem('access_token')
    if (access) {
      config.headers.Authorization = `Bearer ${access}`
    }
    return config
  },
  (error) => Promise.reject(error),
)

request.interceptors.response.use(
  (response) => response,
  async (error) => {
    const { config, response } = error
    const refresh = localStorage.getItem('refresh_token')

    if (response && response.status === 401 && refresh) {
      if (!isRefreshing) {
        isRefreshing = true
        try {
          const res = await axios.post(`${import.meta.env.VITE_APP_BASE_API_URL}token/refresh`, {
            refresh,
          })
          const newAccess = res.data.access
          localStorage.setItem('access_token', newAccess)
          isRefreshing = false
          onRefreshed(newAccess)
          config.headers.Authorization = `Bearer ${newAccess}`
          return request(config)
        } catch (err) {
          isRefreshing = false
          localStorage.removeItem('access_token')
          localStorage.removeItem('refresh_token')
          try {
            useUserStore().clear()
          } catch {
            // ignore store cleanup error
          }
          window.location.href = config?.url?.startsWith('manage/') ? '/admin/login' : '/login'
          return Promise.reject(err)
        }
      }

      return new Promise((resolve) => {
        addSubscriber((token) => {
          config.headers.Authorization = `Bearer ${token}`
          resolve(request(config))
        })
      })
    }
    return Promise.reject(error)
  },
)

export default request
