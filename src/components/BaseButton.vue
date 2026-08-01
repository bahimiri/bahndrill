<script setup lang="ts">
defineEmits(['click'])
</script>

<template>
  <button @click="$emit('click')">
    <slot />
  </button>
</template>

<style lang="scss" scoped>
button {
  border: 1px solid var(--color-border);
  border-radius: 0.5rem;
  background-color: var(--color-action-bg);
  color: var(--color-action-text);
  font-size: 1.25rem;
  padding: 8px 16px;
  cursor: pointer;

  &:hover {
    background-color: var(--color-action-hover-bg);
    color: var(--color-action-hover-text);
  }
}
</style>
