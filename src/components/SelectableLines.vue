<script setup lang="ts">
import { ref } from 'vue'
import { useLineData } from '@/stores/lineData.ts'
import { storeToRefs } from 'pinia'
import type { LineName } from '@/types/lines.ts'

const { lines, undergroundLines, trainLines } = storeToRefs(useLineData())
const lineSelections = ref(
  Object.fromEntries(Object.keys(lines).map((lineName) => [lineName, false])) as Record<
    LineName,
    boolean
  >,
)
const toggleLine = (lineName: LineName) => {
  lineSelections.value[lineName] = !lineSelections.value[lineName]
}
</script>

<template>
  <div>
    <p id="line-selection-label">Welche Bahnen halten hier?</p>
    <div
      role="listbox"
      aria-labelledby="line-selection-label"
      aria-multiselectable="true"
      aria-orientation="horizontal"
    >
      <div role="group" aria-label="U-Bahn">
        <button
          v-for="line in undergroundLines"
          :key="line.name"
          role="option"
          :class="{ selected: lineSelections[line.name] }"
          :aria-checked="lineSelections[line.name]"
          @click="toggleLine(line.name)"
        >
          {{ line.name }}
        </button>
      </div>
      <div role="group" aria-label="S-Bahn">
        <button
          v-for="line in trainLines"
          :key="line.name"
          role="option"
          :class="{ selected: lineSelections[line.name] }"
          :aria-checked="lineSelections[line.name]"
          @click="toggleLine(line.name)"
        >
          {{ line.name }}
        </button>
      </div>
    </div>
  </div>
</template>
<style lang="scss" scoped>
button {
  &.selected {
    border: 2px solid red;
  }
}
</style>
