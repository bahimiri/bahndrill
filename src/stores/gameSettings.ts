import { ref } from 'vue'
import { defineStore } from 'pinia'
import { ZoneSettings } from '@/types/zones.ts'
import type { LineStop } from '@/types/lines.ts'

const DEFAULT_ZONES = ZoneSettings.ABC
const STORAGE_KEY = 'tarif-zonen'
const getZonesFromStorage = () => {
  const value = localStorage.getItem(STORAGE_KEY) as ZoneSettings
  return value && Object.values(ZoneSettings).includes(value) ? value : DEFAULT_ZONES
}

export const useGameSettings = defineStore('gameSettings', () => {
  const selectedZones = ref<ZoneSettings>(getZonesFromStorage())
  const updateSelectedZones = (zones: ZoneSettings) => {
    selectedZones.value = zones
    if (zones === DEFAULT_ZONES) {
      localStorage.removeItem(STORAGE_KEY)
    } else {
      localStorage.setItem(STORAGE_KEY, zones)
    }
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
