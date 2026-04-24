<template>
  <div
    class="flex items-center justify-between px-5 w-full fixed top-0 bg-white py-3 shadow-md shadow-gray-300 z-10"
  >
    <div class="text-3xl font-bold cursor-pointer" @click="$router.push('/')">Fabrics</div>
    <div class="border flex p-2 w-1/3 rounded-lg">
      <input type="text" v-model="store.title" placeholder="布料搜索" class="outline-none flex-1" />
      <button @click="search">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 640" class="w-6">
          <path
            d="M480 272C480 317.9 465.1 360.3 440 394.7L566.6 521.4C579.1 533.9 579.1 554.2 566.6 566.7C554.1 579.2 533.8 579.2 521.3 566.7L394.7 440C360.3 465.1 317.9 480 272 480C157.1 480 64 386.9 64 272C64 157.1 157.1 64 272 64C386.9 64 480 157.1 480 272zM272 416C351.5 416 416 351.5 416 272C416 192.5 351.5 128 272 128C192.5 128 128 192.5 128 272C128 351.5 192.5 416 272 416z"
          />
        </svg>
      </button>
    </div>
    <div class="flex items-center gap-4 ml-4">
      <RouterLink
        to="/price-prediction"
        class="px-4 py-2 rounded-lg text-black hover:bg-gray-100 whitespace-nowrap"
      >
        价格预测
      </RouterLink>
      <RouterLink
        to="/analysis"
        class="px-4 py-2 rounded-lg text-black hover:bg-gray-100 whitespace-nowrap"
      >
        数据分析
      </RouterLink>
      <RouterLink
        to="/ai-chat"
        class="px-4 py-2 rounded-lg text-black hover:bg-gray-100 whitespace-nowrap"
      >
        AI问答
      </RouterLink>
      <div @click="$router.push('/profile')">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 640" class="w-8 h-8">
          <path
            d="M240 192C240 147.8 275.8 112 320 112C364.2 112 400 147.8 400 192C400 236.2 364.2 272 320 272C275.8 272 240 236.2 240 192zM448 192C448 121.3 390.7 64 320 64C249.3 64 192 121.3 192 192C192 262.7 249.3 320 320 320C390.7 320 448 262.7 448 192zM144 544C144 473.3 201.3 416 272 416L368 416C438.7 416 496 473.3 496 544L496 552C496 565.3 506.7 576 520 576C533.3 576 544 565.3 544 552L544 544C544 446.8 465.2 368 368 368L272 368C174.8 368 96 446.8 96 544L96 552C96 565.3 106.7 576 120 576C133.3 576 144 565.3 144 552L144 544z"
          />
        </svg>
      </div>
    </div>
  </div>
</template>
<script setup>
import { ref,inject } from 'vue'
import { useRouter,useRoute, RouterLink } from 'vue-router'
import { useSearchStore } from '@/stores/search'
import { useUserStore } from '@/stores/user'
const userStore = useUserStore()
const store = useSearchStore()
const router = useRouter()
const route = useRoute()
const info=inject('info')
const search = () => {
  if (!store.title) {
    info('请输入搜索内容','warning')
    return
  }
  console.log(route.path)
  if (route.path !== '/search'){
    router.push({ path: '/search' })
  }else{
    store.search()
  }
}
</script>
