<script setup lang="ts"></script>
<template>
  <div class="success-banner-wrapper">
    <div class="success-banner">
      <img src="/src/assets/img/check.svg" alt="Korrekt" />
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use '@/assets/styles/viewports';

.success-banner-wrapper {
  position: fixed;
  left: 0;
  right: 0;
  top: 0;
  bottom: 0;
  z-index: 1;

  @include viewports.above-tablet {
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    right: unset;
    bottom: unset;
    width: var(--game-container-width);
    height: var(--game-container-height);
  }

  .success-banner {
    position: relative;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 32px 0;
    width: 100%;
    height: 100%;
    box-sizing: border-box;

    &:after {
      content: '';
      position: absolute;
      left: 0;
      top: 0;
      right: 0;
      bottom: 0;
      background-color: var(--dark-green);
      opacity: 45%;
      backdrop-filter: blur(10px);

      @include viewports.above-tablet {
        border-radius: var(--game-container-border-radius);
      }
    }

    img {
      height: 8rem;
      width: 8rem;
      position: relative;
      z-index: 2;
    }
  }
}
</style>
