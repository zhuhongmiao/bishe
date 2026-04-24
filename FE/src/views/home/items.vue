<template>
  <div class="flex-1 w-full overflow-auto hidden-scrollbar" ref="father">
    <div class="grid grid-cols-5 gap-10 p-10">
      <div
        v-for="item in store.searchResults"
        :key="item.id"
        class="w-full h-90 bg-white p-2 rounded-xl flex flex-col items-center justify-between hover:bg-gray-200"
      >
        <img
          :src="getItemImage(item.id)"
          alt=""
          class="w-full h-60 rounded-md shadow-md object-cover"
          @error="handleImageError"
        />
        <div class="text-center">
          {{ formatBilingualValue(item.title) }}
        </div>
        <div class="flex items-center gap-1 flex-wrap justify-center">
          <a-tag color="orange">{{ formatBilingualValue(item.category_name) }}</a-tag>
          <a-tag color="cyan">{{ formatBilingualValue(item.pattern) }}</a-tag>
          <a-tag color="purple">{{ formatBilingualValue(item.country) }}</a-tag>
        </div>
      </div>
    </div>
    <div class="cc h-10" ref="loadmore">
      <a-spin v-if="store.isloading" size="large" />
    </div>
  </div>
</template>
<script setup>
import { useSearchStore } from '@/stores/search'
import { formatBilingualValue } from '@/utils/bilingual'
import { onMounted, onUnmounted, useTemplateRef, nextTick } from 'vue'

const store = useSearchStore()
const father = useTemplateRef('father')
const loadmore = useTemplateRef('loadmore')
let observer = null

// const getItemImage = (id) => `https://picsum.photos/200/200?random=${id}`
const getItemImage = (id) => {
  const MIN = 1
  const MAX = 4896
  const RANGE = MAX - MIN + 1

  const str = String(id)

  // FNV-1a 32位哈希
  let hash = 2166136261

  for (let i = 0; i < str.length; i++) {
    hash ^= str.charCodeAt(i)
    hash = Math.imul(hash, 16777619)
  }

  // 转成无符号整数
  hash = hash >>> 0

  const imgNum= MIN + (hash % RANGE)
  return `/fabrics/${imgNum}.jpg`
}

const handleImageError = (event) => {
  event.target.src = '/bg1.jpg'
}

const handleIntersect = (entries) => {
  const entry = entries[0]
  if (entry.isIntersecting) {
    if (store.searchResults.length < store.total || store.total === 0) {
      store.page += 1
      store.seachFun()
    }
  }
}

onMounted(async () => {
  await nextTick()
  observer = new IntersectionObserver(handleIntersect, {
    root: father.value,
    threshold: 0,
    rootMargin: '0px',
  })
  if (loadmore.value) {
    observer.observe(loadmore.value)
  }
})

onUnmounted(() => {
  if (observer) {
    observer.disconnect()
  }
})
</script>
<style scoped>
.hidden-scrollbar {
  overflow: auto;
  scrollbar-width: none;
  -ms-overflow-style: none;
}

.hidden-scrollbar::-webkit-scrollbar {
  display: none;
}
</style>
