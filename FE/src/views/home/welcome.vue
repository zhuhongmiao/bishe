<template>
  <div class="w-screen h-full">
    <div class="w-full h-full overflow-auto hidden-scrollbar">
      <carousel />
      <categrory />
    </div>
  </div>
</template>
<script setup>
import carousel from './carousel.vue'
import categrory from './categrory.vue'
</script>
<style scoped>
.hidden-scrollbar {
  overflow: auto; /* 或 scroll */
  scrollbar-width: none; /* Firefox */
  -ms-overflow-style: none; /* IE 和 Edge 旧版 */
}

.hidden-scrollbar::-webkit-scrollbar {
  display: none; /* Chrome、Safari、Edge 新版 */
}
</style>
