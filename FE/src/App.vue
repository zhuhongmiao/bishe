<template>
  <div>
    <context-holder />
    <RouterView class="w-screen h-screen"/>
  </div>
</template>
<script setup>
import { provide } from 'vue'
import { message } from 'ant-design-vue';


const [messageApi, contextHolder] = message.useMessage();
const info = (msg, type = 'success') => {
  if (type === 'error') {
    messageApi.error(msg);
  } else if (type === 'success') {
    messageApi.success(msg);
  } else if (type === 'warning') {
    messageApi.warning(msg);
  }
}
provide('info', info)
</script>
