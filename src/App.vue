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
  <div class="container">
    <h1 class="mb-24">Welche Bahn fährt hier?</h1>
    <match-lines-for-stations />
  </div>
</template>

<style lang="scss" scoped>
@use '@/assets/styles/viewports';

.container {
  display: flex;
  flex-direction: column;
  flex-grow: 1;
  align-self: center;
  justify-self: center;
  width: 100%;
  max-width: 600px;
  max-height: 100vh;

  @include viewports.above-tablet {
    flex-grow: unset;
    border-radius: 0.5rem;
    box-shadow: var(--dark-green) 0 0 0.5rem;
    width: 600px;
    height: 30rem;
    padding: 24px;
    box-sizing: border-box;
  }
}
</style>
