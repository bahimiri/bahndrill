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
  border: 1px solid var(--color-primary-text);
  border-radius: 0.5rem;
  background-color: var(--color-primary);
  color: var(--color-primary-text);
  font-size: 1.25rem;
  padding: 8px 16px;
  cursor: pointer;

  &:hover {
    background-color: var(--color-primary-text);
    color: var(--color-primary);
  }
}
</style>
