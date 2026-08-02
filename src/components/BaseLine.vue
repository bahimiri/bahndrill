<script setup lang="ts">
import type { Line } from '@/types/lines.ts'
import { isSBahn } from '@/utils/lineType.ts'

withDefaults(defineProps<{ line: Line; isActionable?: boolean; isSelected?: boolean }>(), {
  isActionable: false,
  isSelected: false,
})

defineEmits(['click'])
</script>

<template>
  <div>
    <button
      v-if="isActionable"
      role="option"
      class="line"
      :class="{ selected: isSelected, 's-bahn': isSBahn(line), actionable: isActionable }"
      :aria-checked="isSelected"
      @click="$emit('click')"
    >
      {{ line.name }}
    </button>
    <div v-else class="line" :class="{ 's-bahn': isSBahn(line) }">{{ line.name }}</div>
  </div>
</template>
<style lang="scss" scoped>
@use '@/assets/styles/utils';

.line {
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

  &.actionable {
    cursor: pointer;

    @include utils.on-active-or-hover {
      filter: brightness(1.2);
    }
  }
}
</style>
