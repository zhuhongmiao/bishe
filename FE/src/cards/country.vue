<template>
  <div ref="chart" class="w-100 h-100 bg-white rounded-2xl"></div>
</template>
<script setup>
import api from '../api'
import { onMounted, useTemplateRef, ref, onUnmounted } from 'vue'
import * as echarts from 'echarts'

const chartRef = useTemplateRef('chart')
const data = ref([])
const COUNTRY_ORDER = ['China', 'Korea', 'Japan']
let chartInstance = null

const getData = () => {
  api.getCountriesDate().then((res) => {
    data.value = res.data.data
    render()
  })
}

const render = () => {
  if (!chartRef.value) return

  if (!chartInstance) {
    chartInstance = echarts.init(chartRef.value)
  }

  const countMap = Object.fromEntries(data.value)
  const chartData = COUNTRY_ORDER.map((country) => ({
    name: country,
    value: Number(countMap[country] || 0),
  }))

  const option = {
    title: {
      text: '布料来源统计',
    },
    toolbox: {
      feature: {
        saveAsImage: {
          title: '下载',
          name: 'my-chart',
        },
      },
    },
    xAxis: {
      type: 'category',
      data: chartData.map((item) => item.name),
      axisLabel: {
        fontSize: 15,
        margin: 20,
        interval: 0,
      },
    },
    yAxis: {
      type: 'value',
    },
    series: [
      {
        data: chartData.map((item) => item.value),
        type: 'bar',
      },
    ],
  }
  chartInstance.setOption(option)
}

const handleResize = () => {
  chartInstance?.resize()
}

onMounted(() => {
  getData()
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  chartInstance?.dispose()
  chartInstance = null
})
</script>
