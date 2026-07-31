<script setup lang="ts">
import type { Line } from '@/types/lines.ts'
import { isSBahn } from '@/utils/lineType.ts'

withDefaults(defineProps<{ line: Line; isSelected?: boolean }>(), { isSelected: false })

defineEmits(['click'])
</script>

<template>
  <div>
    <button
      role="option"
      :class="{ selected: isSelected, 's-bahn': isSBahn(line) }"
      :aria-checked="isSelected"
      @click="$emit('click')"
    >
      {{ line.name }}
    </button>
  </div>
</template>
<style lang="scss" scoped>
button {
  box-sizing: border-box;
  background-color: v-bind('`${line.color}`');
  color: v-bind('`${line.textColor}`');
  border: 2px solid v-bind('`${line.color}`');
  padding: 2px 10px;
  font-size: 1.25rem;
  font-weight: 550;

  &.s-bahn {
    border-radius: 1rem;
  }

  &.selected {
    box-shadow: var(--light-green) 0 0 0.75rem;
    border: 2px solid var(--light-green);
  }
}
</style>
