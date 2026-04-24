<template>
  <div class="h-full flex flex-col items-center gap-5">
    <searchControl />
    <items />
  </div>
</template>

<script setup>
import { useSearchStore } from '@/stores/search'
import searchControl from './searchControl.vue'
import items from './items.vue'
</script>
