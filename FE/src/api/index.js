import instance from './request'

const getCountriesDate = () => {
  return instance.get('/analysis/countries')
}
const priceData = () => {
  return instance.get('/analysis/price-stats')
}

const categoryPriceBoxplotData = () => {
  return instance.get('/analysis/category-price-boxplot')
}

const patternPriceBoxplotData = () => {
  return instance.get('/analysis/pattern-price-boxplot')
}

const clusteringAnalysisData = (k = null) => {
  return instance.get('/analysis/clustering-analysis', { params: { k } })
}

const getPrediction = () => {
  return instance.get('/analysis/price-prediction-model')
}

const predictPrice = (data) => {
  return instance.post('/analysis/price-predict', data)
}

const getPricePredictOptions = () => {
  return instance.get('/analysis/price-predict-options')
}

const aiChat = (data) => {
  return instance.post('/analysis/ai-chat', data)
}

const aiChatStream = async (data, onChunk) => {
  const baseURL = import.meta.env.VITE_APP_BASE_API_URL || '/api'
  const url = `${baseURL}/analysis/ai-chat-stream`

  const response = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${localStorage.getItem('access_token') || ''}`,
    },
    body: JSON.stringify(data),
  })

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`)
  }

  const reader = response.body.getReader()
  const decoder = new TextDecoder()

  while (true) {
    const { done, value } = await reader.read()
    if (done) break

    const chunk = decoder.decode(value, { stream: true })
    const lines = chunk.split('\n')

    for (const line of lines) {
      if (line.startsWith('data: ')) {
        const lineData = line.slice(6)
        if (lineData === '[DONE]') {
          return
        }
        try {
          const json = JSON.parse(lineData)
          if (json.content) {
            onChunk(json.content)
          }
        } catch {
          // ignore parse error
        }
      }
    }
  }
}

const login = (username, password) => {
  return instance.post('user/login', { username, password })
}
const register = (username, password, email, phone_number, is_admin = false) => {
  return instance.post('user', { username, password, email, phone_number, is_admin })
}
const tokenVerify = () => {
  return instance.post('user/token/verify', {
    token: localStorage.getItem('access_token'),
  })
}
const fabrics = (params) => {
  return instance.get('fabric/fabrics/', { params })
}
const fabricDetail = (id) => {
  return instance.get(`fabric/fabrics/${id}/`)
}
const fabricsOptions = (field) => {
  return instance.get('fabric/options/', { params: { field } })
}
const userSearch = (params) => {
  return instance.get('user/manage', { params })
}
const userUpdate = (data) => {
  return instance.put('user/manage', data)
}
const userDelete = (user_id) => {
  return instance.delete('user/manage', { data: { id: user_id } })
}
const fabricUpdate = (data) => {
  return instance.put('fabric/manage', data)
}
const fabricDelete = (fabric_id) => {
  return instance.delete('fabric/manage', { data: { id: fabric_id } })
}

const adminOverview = () => {
  return instance.get('manage/overview/')
}
const adminUsers = (params) => {
  return instance.get('manage/users/', { params })
}
const adminUserDetail = (id) => {
  return instance.get(`manage/users/${id}/`)
}
const adminCreateUser = (data) => {
  return instance.post('manage/users/', data)
}
const adminUpdateUser = (id, data) => {
  return instance.put(`manage/users/${id}/`, data)
}
const adminDeleteUser = (id) => {
  return instance.delete(`manage/users/${id}/`)
}
const adminResetUserPassword = (id, password) => {
  return instance.post(`manage/users/${id}/reset-password/`, { password })
}
const adminBatchUsers = (data) => {
  return instance.post('manage/users/batch/', data)
}
const adminFabrics = (params) => {
  return instance.get('manage/fabrics/', { params })
}
const adminFabricDetail = (id) => {
  return instance.get(`manage/fabrics/${id}/`)
}
const adminCreateFabric = (data) => {
  return instance.post('manage/fabrics/', data)
}
const adminUpdateFabric = (id, data) => {
  return instance.put(`manage/fabrics/${id}/`, data)
}
const adminDeleteFabric = (id) => {
  return instance.delete(`manage/fabrics/${id}/`)
}
const adminBatchFabrics = (data) => {
  return instance.post('manage/fabrics/batch/', data)
}

export default {
  getCountriesDate,
  priceData,
  categoryPriceBoxplotData,
  patternPriceBoxplotData,
  clusteringAnalysisData,
  getPrediction,
  predictPrice,
  getPricePredictOptions,
  aiChat,
  aiChatStream,
  login,
  register,
  tokenVerify,
  fabrics,
  fabricDetail,
  fabricsOptions,
  userSearch,
  userUpdate,
  userDelete,
  fabricUpdate,
  fabricDelete,
  adminOverview,
  adminUsers,
  adminUserDetail,
  adminCreateUser,
  adminUpdateUser,
  adminDeleteUser,
  adminResetUserPassword,
  adminBatchUsers,
  adminFabrics,
  adminFabricDetail,
  adminCreateFabric,
  adminUpdateFabric,
  adminDeleteFabric,
  adminBatchFabrics,
}
