import { ref, onMounted, watch } from 'vue'
import { defineStore } from 'pinia'
import api from '@/api'
import { mapBilingualOptions } from '@/utils/bilingual'

export const useSearchStore = defineStore('search', () => {
  const searchResults = ref([])
  const title = ref('')
  const category_name = ref(null)
  const country = ref(null)
  const pattern = ref(null)
  const min_price = ref(0)
  const max_price = ref(0)
  const min_weight = ref(0)
  const max_weight = ref(0)
  const order = ref(null)
  const page = ref(0)
  const page_size = ref(20)
  const total = ref(0)
  const total_pages = ref(0)

  watch(category_name, () => {
    page.value = 1
    total.value = 0
    searchResults.value = []
    seachFun()
  })
  watch(pattern, () => {
    page.value = 1
    total.value = 0
    searchResults.value = []
    seachFun()
  })
  watch(country, () => {
    page.value = 1
    total.value = 0
    searchResults.value = []
    seachFun()
  })

  const categories = ref([])
  const patterns = ref([])
  const countries = ref([])
  const orders = [
    { label: '价格从低到高', value: 'price' },
    { label: '价格从高到低', value: '-price' },
    { label: '重量从低到高', value: 'weight' },
    { label: '重量从高到低', value: '-weight' },
    { label: '点赞从低到高', value: 'likes' },
    { label: '点赞从高到低', value: '-likes' },
  ]
  const isloading = ref(false)
  const seachFun = () => {
    const params = {}
    if (title.value) params.title = title.value
    if (category_name.value) params.category_name = category_name.value
    if (country.value) params.country = country.value
    if (pattern.value) params.pattern = pattern.value
    if (min_price.value) params.min_price = min_price.value
    if (max_price.value) params.max_price = max_price.value
    if (min_weight.value) params.min_weight = min_weight.value
    if (max_weight.value) params.max_weight = max_weight.value
    if (order.value) params.order = order.value
    params.page = page.value
    params.page_size = page_size.value

    isloading.value = true
    api
      .fabrics(params)
      .then((res) => {
        if (res.status === 200) {
          searchResults.value.push(...res.data.results)
          total.value = res.data.count
          total_pages.value = res.data.total_pages
        }
      })
      .finally(() => {
        setTimeout(() => {
          isloading.value = false
        }, 4000)
      })
  }

  const search = () => {
    page.value = 1
    total.value = 0
    searchResults.value = []
    seachFun()
  }
  onMounted(() => {
    api.fabricsOptions('category_name').then((res) => {
      if (res.data.code === 200) {
        categories.value = mapBilingualOptions(res.data.data, false)
      }
    })
    api.fabricsOptions('pattern').then((res) => {
      if (res.data.code === 200) {
        patterns.value = mapBilingualOptions(res.data.data, false)
      }
    })
    api.fabricsOptions('country').then((res) => {
      if (res.data.code === 200) {
        countries.value = mapBilingualOptions(res.data.data, false)
      }
    })
  })

  return {
    searchResults,
    search,
    title,
    category_name,
    country,
    pattern,
    min_price,
    max_price,
    min_weight,
    max_weight,
    order,
    page,
    page_size,
    total,
    total_pages,
    categories,
    patterns,
    countries,
    orders,
    isloading,
    seachFun,
  }
})
