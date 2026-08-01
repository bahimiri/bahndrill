<script setup lang="ts">
import SelectableLines from '@/components/SelectableLines.vue'
import { storeToRefs } from 'pinia'
import { useLineData } from '@/stores/lineData.ts'
import { computed, nextTick, ref, useTemplateRef, watch } from 'vue'
import type { LineName, LineStop } from '@/types/lines.ts'
import BaseButton from '@/components/BaseButton.vue'
import ResultView from '@/components/ResultView.vue'

const { initialized, stops, lines } = storeToRefs(useLineData())

const getAllDeselectedConfiguration = () =>
  Object.fromEntries(Object.keys(lines).map((lineName) => [lineName, false])) as Record<
    LineName,
    boolean
  >
const lineSelections = ref(getAllDeselectedConfiguration())

const getNextStop = () => {
  return stops.value[Math.floor(Math.random() * stops.value.length)]!
}
const stop = ref<LineStop | null>(null)
watch(
  initialized,
  () => {
    if (initialized) {
      stop.value = getNextStop()
    }
  },
  { once: true },
)

const nextStopRef = useTemplateRef('nextStop')
const showNext = async () => {
  lineSelections.value = getAllDeselectedConfiguration()
  stop.value = getNextStop()
  await nextTick()
  nextStopRef.value?.focus()
}

// TODO line mapping refactorn
const selectedLines = computed(() => {
  const selectedLineNames = Object.keys(lineSelections.value).filter(
    (lineName) => lineSelections.value[lineName as LineName],
  )
  return selectedLineNames.map((lineName) => lines.value.find((line) => line.name === lineName)!)
})

const correctLines = computed(() =>
  (stop.value?.lines ?? []).map((lineName) => lines.value.find((line) => line.name === lineName)!),
)

const handleContinue = () => {
  if (showResult.value) {
    showNext()
    showResult.value = false
  } else {
    showResult.value = true
  }
}

const showResult = ref(false)
</script>

<template>
  <div class="match-lines-for-stations">
    <template v-if="stop">
      <p id="line-selection-description" class="mb-8">
        Wähle alle Linien, die an der Station abfahren:
      </p>
      <p id="line-selection-label" ref="nextStop" class="station mb-16" tabindex="-1">
        {{ stop.name }}
      </p>
      <div aria-live="assertive">
        <selectable-lines
          v-if="!showResult"
          ref="selectableLinesSection"
          v-model="lineSelections"
          :stop="stop"
          labelled-by-id="line-selection-label"
          described-by-id="line-selection-description"
          class="mb-24"
        />
        <result-view
          v-else
          :selected-lines="selectedLines"
          :correct-lines="correctLines"
          class="mb-24"
        />
      </div>
    </template>
    <base-button @click="handleContinue()">Weiter</base-button>
  </div>
</template>

<style lang="scss" scoped>
.match-lines-for-stations {
  display: flex;
  flex-direction: column;

  .station {
    font-weight: bold;
    font-size: 1.25rem;
  }
}
</style>
