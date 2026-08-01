<script setup lang="ts">
import { useLineData } from '@/stores/lineData.ts'
import { storeToRefs } from 'pinia'
import type { LineName, LineStop } from '@/types/lines.ts'
import BaseLine from '@/components/BaseLine.vue'
import { useTemplateRef } from 'vue'

defineProps<{ stop: LineStop; labelledById: string; describedById: string }>()
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
    <div
      role="listbox"
      :aria-labelledby="labelledById"
      :aria-describedby="describedById"
      aria-multiselectable="true"
      aria-orientation="horizontal"
    >
      <div class="lines" role="group" aria-label="U-Bahn">
        <base-line
          v-for="line in undergroundLines"
          :key="line.name"
          :line="line"
          :is-selected="lineSelections[line.name]"
          is-actionable
          @click="toggleLine(line.name)"
        />
      </div>
      <div class="lines" role="group" aria-label="S-Bahn">
        <base-line
          v-for="line in trainLines"
          :key="line.name"
          :line="line"
          :is-selected="lineSelections[line.name]"
          is-actionable
          @click="toggleLine(line.name)"
        />
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.lines {
  display: flex;
  column-gap: 0.5rem;
  row-gap: 0.75rem;
  flex-wrap: wrap;

  &:not(:last-of-type) {
    margin-bottom: 1rem;
  }
}
</style>
