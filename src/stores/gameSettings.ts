import { ref } from 'vue'
import { defineStore } from 'pinia'
import { ZoneSettings } from '@/types/zones.ts'
import type { LineStop } from '@/types/lines.ts'

export const useGameSettings = defineStore('gameSettings', () => {
  const selectedZones = ref<ZoneSettings>(ZoneSettings.ABC)
  const updateSelectedZones = (zones: ZoneSettings) => {
    selectedZones.value = zones
  }
  const zonesToArray = (zones: ZoneSettings) => zones.split('') as Array<'A' | 'B' | 'C'>

  const getStopsForZone = (stops: Array<LineStop>, zone: 'A' | 'B' | 'C') =>
    stops.filter((stop) => stop.zone === zone)

  return {
    selectedZones,
    updateSelectedZones,
    zonesToArray,
    getStopsForZone,
  }
})
