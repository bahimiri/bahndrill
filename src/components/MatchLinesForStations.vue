<script setup lang="ts">
import SelectableLines from '@/components/SelectableLines.vue'
import { storeToRefs } from 'pinia'
import { useLineData } from '@/stores/lineData.ts'
import { computed, nextTick, ref, useTemplateRef, watch } from 'vue'
import type { LineName, LineStop } from '@/types/lines.ts'
import BaseButton from '@/components/BaseButton.vue'
import CorrectionView from '@/components/CorrectionView.vue'
import SuccessBanner from '@/components/SuccessBanner.vue'

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
  setTimeout(() => {
    nextStopRef.value?.focus()
  }, 0)
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
    if (isCorrect.value) {
      setTimeout(() => handleContinue(), 1000)
    }
  }
}

const showResult = ref(false)
const isCorrect = computed(() => {
  return (
    correctLines.value.filter((line) => selectedLines.value.includes(line)).length ===
    correctLines.value.length
  )
})
</script>

<template>
  <div class="match-lines-for-stations">
    <div class="game">
      <template v-if="stop">
        <p id="line-selection-description" class="mb-8">
          Wähle alle Linien, die an der Station abfahren:
        </p>
        <p id="line-selection-label" ref="nextStop" class="station mb-16" tabindex="-1">
          {{ stop.name }}
        </p>
        <selectable-lines
          v-if="!showResult || isCorrect"
          ref="selectableLinesSection"
          v-model="lineSelections"
          :stop="stop"
          labelled-by-id="line-selection-label"
          described-by-id="line-selection-description"
          class="mb-24"
        />
        <div aria-live="assertive">
          <template v-if="showResult">
            <success-banner v-if="isCorrect" />
            <correction-view
              v-else
              :selected-lines="selectedLines"
              :correct-lines="correctLines"
              class="mb-24"
            />
          </template>
        </div>
      </template>
    </div>
    <base-button @click="handleContinue()">Weiter</base-button>
  </div>
</template>

<style lang="scss" scoped>
.match-lines-for-stations {
  display: flex;
  flex-direction: column;
  flex-grow: 1;

  .game {
    flex-grow: 1;
  }

  .station {
    font-weight: bold;
    font-size: 1.25rem;
  }
}
</style>
