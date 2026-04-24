<template>
  <div class="flex items-center gap-10">
    <div ref="chart1" class="flex-1 h-100 bg-white rounded-2xl"></div>
    <div ref="chart2" class="flex-1 h-100 bg-white rounded-2xl"></div>
  </div>
</template>
<script setup>
import api from '../api'
import { onMounted, ref, useTemplateRef,onUnmounted } from 'vue'
import * as echarts from 'echarts'
const props=defineProps({
  // k: Number
  k:{
    type: Number,
    default:3
  }
})
const data = ref()
const getData = () => {
  api.clusteringAnalysisData(props.k).then((res) => {
    data.value = res.data.data
    console.log(data.value)
    render()
  })
}
const chartRef1 = useTemplateRef('chart1')
const chartRef2 = useTemplateRef('chart2')
const render = () => {
  const chart1 = echarts.init(chartRef1.value)
  const s = data.value.pca_scatter
  const option1 = {
    tooltip: {
      trigger: 'item',
      formatter: (p) => {
        const m = p.value[2] // meta
        return (
          `${p.seriesName}<br/>PC1: ${p.value[0].toFixed(2)}, PC2: ${p.value[1].toFixed(2)}<br/>` +
          `price: ${m.price}, weight: ${m.weight}<br/>${m.category} / ${m.pattern} / ${m.country}`
        )
      },
    },
    toolbox: {
      feature: {
        saveAsImage: {
          title: '下载',
          // pixelRatio: 2, // 可选，导出图片的清晰度
          name: 'my-chart', // 可选，导出的文件名
        },
      },
    },
    legend: { data: s.legend },
    xAxis: { name: s.xName },
    yAxis: { name: s.yName },
    series: s.series,
  }
  chart1.setOption(option1)

  const chart2 = echarts.init(chartRef2.value)
  const b = data.value.cluster_size_bar
  const option2 = {
    toolbox: {
      feature: {
        saveAsImage: {
          title: '下载',
          // pixelRatio: 2, // 可选，导出图片的清晰度
          name: 'my-chart', // 可选，导出的文件名
        },
      },
    },
    xAxis: { type: 'category', data: b.x },
    yAxis: { type: 'value' },
    series: [{ type: 'bar', data: b.y }],
  }
  chart2.setOption(option2)
}
onMounted(() => {
  getData()
  window.addEventListener('resize', () => {
    const chart1 = echarts.init(chartRef1.value)
    chart1.resize()
    const chart2 = echarts.init(chartRef2.value)
    chart2.resize()
  })
})
onUnmounted(() => {
  window.removeEventListener('resize', () => {
    const chart1 = echarts.init(chartRef1.value)
    chart1.resize()
    const chart2 = echarts.init(chartRef2.value)
    chart2.resize()
  })
})
</script>
