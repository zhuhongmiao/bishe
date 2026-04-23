<template>
  <div>
    <div class="px-5 text-3xl font-bold">今日推荐</div>
    <a-carousel autoplay>
      <div v-for="(item, index) in recommends" :key="index" class="p-3">
        <div class="flex gap-10 bg-white p-5 rounded-xl">
          <img :src="item.image" alt="" class="w-60" />
          <div class="flex flex-col gap-5">
            <div class="text-2xl">
              {{ item.title }}
            </div>
            <div>
              <span class="text-[#1c2752]">国家：</span>
              <span class="font-bold text-xl">
                {{ item.country }}
              </span>
            </div>
            <div>
              <span class="text-[#1c2752]">价格：</span>
              <span class="font-bold text-xl">
                {{ item.price }}
              </span>
            </div>
            <div>
              <span class="text-[#1c2752]">图案：</span>
              <span class="font-bold text-xl">
                {{ item.pattern }}
              </span>
            </div>
            <div>
              <span class="text-[#1c2752]">类别：</span>
              <span class="font-bold text-xl">
                {{ item.category_name }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </a-carousel>
  </div>
</template>
<script setup>
import api from '@/api'
import { onMounted, ref } from 'vue'
const recommends = ref([])

const getRecommend = () => {
  api
    .fabrics({
      page: 1,
      page_size: 5,
      ordering: '-like',
    })
    .then((res) => {
      recommends.value = res.data.results.map((item, index) => {
        return {
          ...item,
          image: `recommends/${index + 1}.jpg`,
        }
      })
    })
}

onMounted(() => {
  getRecommend()
})
</script>
