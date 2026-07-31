<script setup lang="ts">
import { onBeforeMount } from 'vue'
import { useLineData } from '@/stores/lineData.ts'
import MatchLinesForStations from '@/components/MatchLinesForStations.vue'

const lineDataStore = useLineData()
onBeforeMount(async () => {
  const data = (await import('../data/extract/data.json')).default
  lineDataStore.setLines(data.lines)
  lineDataStore.setStops(data.stops)
})
</script>

<template>
  <h1 class="mb-24">Welche Bahn fährt hier?</h1>
  <match-lines-for-stations />
</template>

<style scoped></style>
