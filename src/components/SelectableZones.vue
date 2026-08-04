<script lang="ts" setup>
defineProps<{ zones: ReadonlyArray<'A' | 'B' | 'C'>; isSelected: boolean }>()
defineEmits(['click'])
</script>

<template>
  <button
    role="option"
    :class="{ selected: isSelected }"
    :aria-checked="isSelected"
    @click="$emit('click')"
  >
    <span v-for="zone in zones" :key="zone" :class="{ [`zone-${zone}`]: true }">{{ zone }}</span>
  </button>
</template>

<style lang="scss" scoped>
$color-zone-a: #be5a00;
$color-zone-b: #008190;
$color-zone-c: #5a821e;

button {
  display: flex;
  gap: var(--space-4);
  background: none;
  border: 1px solid transparent;
  cursor: pointer;
  padding: 6px;
  align-items: center;
  box-sizing: border-box;

  span {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    color: #fff;
    font-weight: bold;
    font-size: 0.8rem;
    height: 1.5rem;
    width: 1.5rem;

    &.zone-A {
      background-color: $color-zone-a;
    }

    &.zone-B {
      background-color: $color-zone-b;
    }

    &.zone-C {
      background-color: $color-zone-c;
    }
  }

  &.selected {
    box-shadow: var(--light-green) 0 0 0.3rem;
    border: 1px solid var(--light-green);
    border-radius: 0.25rem;
  }
}
</style>
