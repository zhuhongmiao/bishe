<template>
  <div class="w-screen h-full">
    <div class="w-full h-full overflow-auto p-10 hidden-scrollbar">
      <div class="flex items-center justify-between gap-10">
        <country />
        <priceBase />
      </div>
      <div class="mt-10">
        <categoryBoxplot />
      </div>
      <div class="mt-10">
        <patternBoxplot />
      </div>
      <div class="mt-10">
        <clusteringAnalysis :k="2" />
        <clusteringAnalysis :k="3" class="mt-10" />
        <clusteringAnalysis :k="5" class="mt-10" />
        <clusteringAnalysis :k="10" class="mt-10" />
      </div>
      <div class="mt-10">
        <prediction />
      </div>
    </div>
  </div>
</template>

<script setup>
import country from '../../cards/country.vue'
import priceBase from '../../cards/priceBase.vue'
import categoryBoxplot from '../../cards/categoryBoxplot.vue'
import patternBoxplot from '../../cards/patternBoxplot.vue'
import clusteringAnalysis from '../../cards/clusteringAnalysis.vue'
import prediction from '../../cards/prediction.vue'
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
