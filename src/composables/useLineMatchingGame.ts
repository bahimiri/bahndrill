import { storeToRefs } from 'pinia'
import { useLineData } from '@/stores/lineData.ts'
import { useGameSettings } from '@/stores/gameSettings.ts'
import { computed, ref, watch } from 'vue'
import type { Line, LineStop } from '@/types/lines.ts'

export const useLineMatchingGame = () => {
  const { initialized, lines, stops } = storeToRefs(useLineData())
  const gameSettingsStore = useGameSettings()
  const { zonesToArray, getStopsForZone } = gameSettingsStore
  const { selectedZones } = storeToRefs(gameSettingsStore)

  const filteredStops = computed(() => {
    const zones = zonesToArray(selectedZones.value)
    return [
      ...(zones.includes('A') ? getStopsForZone(stops.value, 'A') : []),
      ...(zones.includes('B') ? getStopsForZone(stops.value, 'B') : []),
      ...(zones.includes('C') ? getStopsForZone(stops.value, 'C') : []),
    ]
  })

  watch(filteredStops, (newFilteredStops) => {
    if (stop.value && !newFilteredStops.includes(stop.value)) {
      setNextStop()
    }
  })

  const setNextStop = () => {
    stop.value = filteredStops.value[Math.floor(Math.random() * filteredStops.value.length)]!
  }
  const stop = ref<LineStop | null>(null)
  watch(
    initialized,
    () => {
      if (initialized) {
        setNextStop()
      }
    },
    { once: true },
  )

  const selectedLines = ref<Array<Line>>([])

  const correctLines = computed(() =>
    (stop.value?.lines ?? []).map(
      (lineName) => lines.value.find((line) => line.name === lineName)!,
    ),
  )

  const isCorrect = computed(
    () =>
      correctLines.value.filter((line) => selectedLines.value.includes(line)).length ===
      correctLines.value.length,
  )

  const startChallenge = () => {
    selectedLines.value = []
    setNextStop()
  }

  return {
    stop,
    selectedLines,
    correctLines,
    isCorrect,
    startChallenge,
  }
}
