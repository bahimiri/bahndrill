<script setup lang="ts">
import type { Line } from '@/types/lines.ts'
import BaseLine from '@/components/BaseLine.vue'

defineProps<{ selectedLines: Array<Line>; correctLines: Array<Line> }>()
</script>

<template>
  <div class="correction-view">
    <h3 class="mb-12">Deine Auswahl</h3>
    <div class="mb-16">
      <ul v-if="selectedLines.length">
        <li v-for="line in selectedLines" :key="line.name">
          <base-line :line="line" />
        </li>
      </ul>
      <p v-else>keine Linien</p>
    </div>
    <h3 class="mb-12">Richtig wäre gewesen</h3>
    <ul>
      <li v-for="line in correctLines" :key="line.name">
        <base-line :line="line" />
      </li>
    </ul>
  </div>
</template>

<style lang="scss" scoped>
.correction-view {
  border: 1px solid var(--color-border);
  border-radius: 0.5rem;
  padding: 16px;

  h3 {
    font-size: 1rem;
    font-weight: bold;
  }

  ul {
    margin: 0;
    padding: 0;
    display: flex;
    flex-wrap: wrap;
    column-gap: 0.5rem;
    row-gap: 0.75rem;
  }

  li {
    list-style: none;
  }
}
</style>
