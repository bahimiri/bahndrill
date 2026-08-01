<script setup lang="ts">
import { computed } from 'vue'
import type { Line } from '@/types/lines.ts'
import BaseLine from '@/components/BaseLine.vue'

const props = defineProps<{ selectedLines: Array<Line>; correctLines: Array<Line> }>()

const isCorrect = computed(() => {
  return (
    props.correctLines.filter((line) => props.selectedLines.includes(line)).length ===
    props.correctLines.length
  )
})
</script>

<template>
  <div class="result-view">
    <template v-if="isCorrect">
      <h2 class="mb-8">Das war korrekt!</h2>
      <p class="mb-12">Hier hat man Anschluss an</p>
    </template>
    <template v-else>
      <h2 class="mb-12">Deine Auswahl</h2>
      <div class="mb-16">
        <ul v-if="selectedLines.length">
          <li v-for="line in selectedLines" :key="line.name">
            <base-line :line="line" />
          </li>
        </ul>
        <p v-else>keine Linien</p>
      </div>
      <h2 class="mb-12">Richtig wäre gewesen</h2>
    </template>
    <ul>
      <li v-for="line in correctLines" :key="line.name">
        <base-line :line="line" />
      </li>
    </ul>
  </div>
</template>

<style lang="scss" scoped>
.result-view {
  border: 1px solid var(--color-border);
  border-radius: 0.5rem;
  padding: 16px;

  h2 {
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
