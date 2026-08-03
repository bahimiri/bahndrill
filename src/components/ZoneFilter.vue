<script setup lang="ts">
import SelectableZones from '@/components/SelectableZones.vue'
import { storeToRefs } from 'pinia'
import { useGameSettings } from '@/stores/gameSettings.ts'
import { ZoneSettings } from '@/types/zones.ts'

const gameSettingsStore = useGameSettings()
const { selectedZones } = storeToRefs(gameSettingsStore)
</script>

<template>
  <div class="zone-filter">
    <p id="zone-label">Tarifbereich</p>
    <div
      role="listbox"
      aria-labelledby="zone-label"
      aria-multiselectable="true"
      aria-orientation="horizontal"
    >
      <selectable-zones
        v-for="(zones, index) in [
          ZoneSettings.ABC,
          ZoneSettings.AB,
          ZoneSettings.BC,
          ZoneSettings.A,
          ZoneSettings.B,
          ZoneSettings.C,
        ]"
        :key="index"
        :zones="gameSettingsStore.zonesToArray(zones)"
        :is-selected="selectedZones === zones"
        @click="gameSettingsStore.updateSelectedZones(zones)"
      />
    </div>
  </div>
</template>

<style lang="scss" scoped>
.zone-filter {
  display: flex;
  justify-content: space-between;
  gap: var(--space-24);
  align-items: center;

  p {
    font-size: 0.9rem;
  }

  [role='listbox'] {
    flex-grow: 1;
    display: flex;
    flex-wrap: wrap;
    column-gap: var(--space-4);
  }
}
</style>
