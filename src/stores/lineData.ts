import { ref } from 'vue'
import { defineStore } from 'pinia'
import type { Line, LineName, LineStop } from '@/types/lines.ts'

export const useLineData = defineStore('lineData', () => {
  const lines = ref<Array<Line>>([])
  const stops = ref<Array<LineStop>>([])

  function setLines(storageLines: Record<LineName, { color: string; text_color: string }>) {
    lines.value = (Object.keys(storageLines) as Array<LineName>).map((lineName: LineName) => ({
      name: lineName,
      color: storageLines[lineName].color,
      textColor: storageLines[lineName].text_color,
    }))
  }

  function setStops(storageStops: Record<string, Array<string>>) {
    stops.value = Object.keys(storageStops).map((stopName: string) => ({
      name: stopName,
      lines: storageStops[stopName] as Array<LineName>,
    }))
  }

  return {
    lines,
    stops,
    setLines,
    setStops,
  }
})
