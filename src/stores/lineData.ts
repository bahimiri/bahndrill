import { computed, ref } from 'vue'
import { defineStore } from 'pinia'
import type { Line, LineName, LineStop } from '@/types/lines.ts'
import { isSBahn, isUBahn } from '@/utils/lineType.ts'

type StopData = Record<
  string,
  {
    lines: Array<string>
    zone: string
  }
>

export const useLineData = defineStore('lineData', () => {
  const initialized = ref(false)
  const lines = ref<Array<Line>>([])
  const undergroundLines = computed(() => lines.value.filter(isUBahn))
  const trainLines = computed(() => lines.value.filter(isSBahn))
  const stops = ref<Array<LineStop>>([])

  function setLines(storageLines: Record<LineName, { color: string; text_color: string }>) {
    lines.value = (Object.keys(storageLines) as Array<LineName>).map((lineName: LineName) => ({
      name: lineName,
      color: `#${storageLines[lineName].color}`,
      textColor: `#${storageLines[lineName].text_color}`,
    }))
    if (lines.value.length && stops.value.length) {
      initialized.value = true
    }
  }

  function setStops(storageStops: StopData) {
    stops.value = Object.keys(storageStops).map((stopName: string) => ({
      name: stopName,
      lines: storageStops[stopName]!.lines as Array<LineName>,
      zone: storageStops[stopName]!.zone as 'A' | 'B' | 'C',
    }))
    if (lines.value.length && stops.value.length) {
      initialized.value = true
    }
  }

  return {
    initialized,
    lines,
    undergroundLines,
    trainLines,
    stops,
    setLines,
    setStops,
  }
})
