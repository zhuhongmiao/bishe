<template>
  <div class="rounded-2xl bg-white flex-1 h-100 text-black py-3 px-5">
    <div class="text-xl font-bold text-[#3c3c42]">布料价格统计</div>
    <div class="mt-10 grid grid-cols-2 gap-5 px-10">
      <div class="cell">
        <span class="label">平均价格：</span>
        <span class="price">{{ priceData.mean }}</span>
      </div>
      <div class="cell">
        <span class="label">最高价格：</span>
        <span class="price">{{ priceData.max }}</span>
      </div>
      <div class="cell">
        <span class="label">最低价格：</span>
        <span class="price">{{ priceData.min }}</span>
      </div>
      <div class="cell">
        <span class="label">标准差：</span>
        <span class="price">{{ priceData.std }}</span>
      </div>
      <div class="cell">
        <span class="label">中位数：</span>
        <span class="price">{{ priceData.median }}</span>
      </div>
      <div class="cell">
        <span class="label">众数：</span>
        <span class="price">{{ priceData.mode }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import api from '../api'
import { onMounted, ref } from 'vue'

const priceData = ref({})

const getPriceData = () => {
  api.priceData().then((res) => {
    priceData.value = res.data.data
    console.log(priceData.value)
  })
}

onMounted(() => {
  getPriceData()
})
</script>
<style scoped>
.cell {
  height: 80px;
  display: flex;
  align-items: center;
}
.label {
  font-size: 20px;
  color: #6b7280;
  margin-right: 10px;
  font-weight: bold;
  height: 100%;
  display: flex;
  align-items: center;
}
.price {
  font-size: 42px;
  color: #3b82f6;
  font-weight: bold;
  height: 100%;
  display: flex;
  align-items: center;
  padding: 0;
}
.price:hover {
  font-size: 60px;
  transition: all 0.3s ease-in-out;
}
</style>
