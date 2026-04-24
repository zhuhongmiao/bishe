<template>
  <div>
    <splashCursor />
    <div>
      <GradientText
        text="面料数据分析与可视化"
        :colors="['#ffaa40', '#9c40ff', '#ffaa40']"
        :animation-speed="8"
        :show-border="false"
        class-name="your-custom-class"
      />
    </div>
    <div class="flex items-center justify-between gap-10 mt-10">
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
</template>

<script setup>
import splashCursor from '../components/splashCursor.vue'
import country from '../cards/country.vue'
import priceBase from '../cards/priceBase.vue'
import categoryBoxplot from '../cards/categoryBoxplot.vue'
import patternBoxplot from '../cards/patternBoxplot.vue'
import clusteringAnalysis from '../cards/clusteringAnalysis.vue'
import prediction from '../cards/prediction.vue'
import GradientText from '../components/gradientText.vue'
</script>
