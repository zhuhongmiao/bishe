<template>
  <div>
    <div ref="chart1" class="w-full h-100 bg-white rounded-2xl"></div>
    <div ref="chart2" class="w-full h-100 bg-white rounded-2xl mt-10"></div>
  </div>
</template>
<script setup>
import api from '../api'
import { onMounted, useTemplateRef, ref,onUnmounted } from 'vue'
import * as echarts from 'echarts'
const chartRef1 = useTemplateRef('chart1')
const chartRef2 = useTemplateRef('chart2')
const data = ref()
const getData = () => {
  api.getPrediction().then((res) => {
    data.value = res.data.data
    console.log(data.value)
    render()
  })
}
const render = () => {
  const spa = data.value.echarts.scatter_pred_vs_actual
  const chart1 = echarts.init(chartRef1.value)
  const option1 = {
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
    legend: { data: ['LinearRegression', 'RandomForest'] },
    xAxis: { name: spa.xName },
    yAxis: { name: spa.yName },
    series: [
      { type: 'scatter', name: 'LinearRegression', data: spa.series.LinearRegression },
      { type: 'scatter', name: 'RandomForest', data: spa.series.RandomForest },
      // 45°参考线（可选）
      {
        type: 'line',
        name: 'y = x',
        data: [
          [
            Math.min(...spa.series.RandomForest.map((p) => p[0])),
            Math.min(...spa.series.RandomForest.map((p) => p[0])),
          ],
          [
            Math.max(...spa.series.RandomForest.map((p) => p[0])),
            Math.max(...spa.series.RandomForest.map((p) => p[0])),
          ],
        ],
        showSymbol: false,
        lineStyle: { type: 'dashed' },
        emphasis: { disabled: true },
      },
    ],
  }
  chart1.setOption(option1)


  const chart2 = echarts.init(chartRef2.value)
  const bar = data.value.echarts.bar_feature_importance
  const option2 = {
    tooltip: { trigger: 'axis' },
    toolbox: {
      feature: {
        saveAsImage: {
          title: '下载',
          // pixelRatio: 2, // 可选，导出图片的清晰度
          name: 'my-chart', // 可选，导出的文件名
        },
      },
    },
    grid: { left: 120, right: 20, top: 20, bottom: 40 },
    xAxis: { type: 'value', name: 'Importance' },
    yAxis: { type: 'category', data: bar.features.slice(0, 10) },
    series: [{ type: 'bar', data: bar.importance.slice(0, 10) }],
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
