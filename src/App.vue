<script setup lang="ts">
import { onBeforeMount } from 'vue'
import { useLineData } from '@/stores/lineData.ts'

const lineDataStore = useLineData()
onBeforeMount(async () => {
  const data = (await import('../data/extract/data.json')).default
  lineDataStore.setLines(data.lines)
  lineDataStore.setStops(data.stops)
})
</script>

<template>
  <h1>You did it!</h1>
  <p>well done</p>
</template>

<style scoped></style>
