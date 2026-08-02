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
    <header>
      <div>
        <img src="/src/assets/img/logo.svg" alt="" />
        <h1>Bahndrill</h1>
      </div>
    </header>
    <main>
      <h2 class="mb-24">Welche Bahn fährt hier?</h2>
      <match-lines-for-stations />
    </main>
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

  main {
    padding: 24px;
    display: flex;
    flex-direction: column;
    flex-grow: 1;
  }

  @include viewports.above-tablet {
    flex-grow: unset;
    border-radius: 0.5rem;
    box-shadow: var(--dark-green) 0 0 0.5rem;
    width: 600px;
    height: 30rem;
    box-sizing: border-box;
  }

  header {
    box-shadow: var(--dark-green) 0 0.5rem 0.5rem -0.5rem;
    padding: 16px 24px;
    display: flex;
    justify-content: center;

    div {
      display: flex;
      align-items: center;
      gap: var(--space-12);

      img {
        width: 2rem;
        height: 2rem;
      }

      h1 {
        font-size: 1.75rem;
      }

      @include viewports.above-tablet {
        img {
          width: 1.75rem;
          height: 1.75rem;
        }

        h1 {
          font-size: 1.75rem;
        }
      }
    }
  }
}
</style>
