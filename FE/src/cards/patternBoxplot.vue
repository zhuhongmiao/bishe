<template>
  <div ref="chart" class="w-full h-100 bg-white rounded-2xl"></div>
</template>
<script setup>
import api from '../api'
import { onMounted, useTemplateRef, ref,onUnmounted } from 'vue'
import * as echarts from 'echarts'

const chartRef = useTemplateRef('chart')
const data = ref([])
const getData = () => {
  api.patternPriceBoxplotData().then((res) => {
    data.value = res.data.data
    console.log(data.value)
    render()
  })
}
const render = () => {
  const chart = echarts.init(chartRef.value)
  const option = {
    title: { text: '各图案价格分布箱线图' },
    grid: {
      left: 50,
      right: 50,
    },
    tooltip: { trigger: 'item' },
    toolbox: {
      feature: {
        saveAsImage: {
          title: '下载',
          // pixelRatio: 2, // 可选，导出图片的清晰度
          name: 'my-chart', // 可选，导出的文件名
        },
      },
    },
    xAxis: {
      type: 'category',
      data: data.value.xAxis,
      axisLabel: {
        rotate: 90, // 或 60/90
        interval: 0, // 强制显示全部标签
      },
    },
    yAxis: { type: 'value' },
    series: [
      {
        type: 'boxplot',
        data: data.value.data,
      },
    ],
  }
  chart.setOption(option)
}
onMounted(() => {
  getData()
  window.addEventListener('resize', () => {
    const chart = echarts.init(chartRef.value)
    chart.resize()
  })
})
onUnmounted(() => {
  window.removeEventListener('resize', () => {
    const chart = echarts.init(chartRef.value)
    chart.resize()
  })
})
</script>
