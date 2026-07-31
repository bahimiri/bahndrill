<script setup lang="ts">
import { useLineData } from '@/stores/lineData.ts'
import { storeToRefs } from 'pinia'
import type { LineName } from '@/types/lines.ts'
import BaseLine from '@/components/BaseLine.vue'

const lineSelections = defineModel<Record<LineName, boolean>>({ required: true })
const emit = defineEmits(['update:modelValue'])

const { undergroundLines, trainLines } = storeToRefs(useLineData())

const toggleLine = (lineName: LineName) => {
  emit('update:modelValue', {
    ...lineSelections.value,
    [lineName]: !lineSelections.value[lineName],
  })
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
      <div class="lines" role="group" aria-label="U-Bahn">
        <base-line
          v-for="line in undergroundLines"
          :key="line.name"
          :line="line"
          :is-selected="lineSelections[line.name]"
          @toggle="toggleLine(line.name)"
        />
      </div>
      <div class="lines" role="group" aria-label="S-Bahn">
        <base-line
          v-for="line in trainLines"
          :key="line.name"
          :line="line"
          :is-selected="lineSelections[line.name]"
          @toggle="toggleLine(line.name)"
        />
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.lines {
  display: flex;
  gap: 0.25rem;
  flex-wrap: wrap;

  &:not(:last-of-type) {
    margin-bottom: 0.5rem;
  }
}
</style>
