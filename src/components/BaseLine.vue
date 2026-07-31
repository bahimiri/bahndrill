<script setup lang="ts">
import type { Line } from '@/types/lines.ts'
import { isSBahn } from '@/utils/lineType.ts'

withDefaults(defineProps<{ line: Line; isSelected?: boolean }>(), { isSelected: false })

defineEmits(['clicked'])
</script>

<template>
  <div>
    <button
      role="option"
      :class="{ selected: isSelected, 's-bahn': isSBahn(line) }"
      :aria-checked="isSelected"
      @click="$emit('clicked')"
    >
      {{ line.name }}
    </button>
  </div>
</template>
<style lang="scss" scoped>
button {
  background-color: v-bind('`${line.color}`');
  color: v-bind('`${line.textColor}`');
  border: none;
  padding: 4px 12px;
  font-size: 1.25rem;
  font-weight: 550;

  &.s-bahn {
    border-radius: 1rem;
  }

  &.selected {
    border: 2px solid red;
  }
}
</style>
