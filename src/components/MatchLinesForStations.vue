<script setup lang="ts">
import SelectableLines from '@/components/SelectableLines.vue'
import { storeToRefs } from 'pinia'
import { useLineData } from '@/stores/lineData.ts'
import { nextTick, onBeforeMount, onMounted, ref, watch, watchEffect } from 'vue'
import type { LineName, LineStop } from '@/types/lines.ts'
import BaseButton from '@/components/BaseButton.vue'

const { initialized, stops, lines } = storeToRefs(useLineData())

const getAllDeselectedConfiguration = () =>
  Object.fromEntries(Object.keys(lines).map((lineName) => [lineName, false])) as Record<
    LineName,
    boolean
  >
const lineSelections = ref(getAllDeselectedConfiguration())

const correctedAnswer = ref<Array<LineName> | null>(null)
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

const showNext = () => {
  lineSelections.value = getAllDeselectedConfiguration()
  correctedAnswer.value = null
  stop.value = getNextStop()
}

const checkAnswer = () => {
  const selectedLines = Object.keys(lineSelections.value).filter(
    (lineName) => lineSelections.value[lineName as LineName],
  )
  const correctAnswer = stop.value!.lines
  const isCorrect =
    correctAnswer.filter((line) => selectedLines.includes(line)).length === correctAnswer.length
  if (!isCorrect) {
    correctedAnswer.value = correctAnswer
  } else {
    showNext()
  }
}

const handleContinue = () => {
  if (correctedAnswer.value) {
    showNext()
  } else {
    checkAnswer()
  }
}
</script>

<template>
  <div class="match-lines-for-stations">
    <selectable-lines v-if="stop" v-model="lineSelections" :stop="stop" class="mb-24" />
    <base-button @click="handleContinue()">Weiter</base-button>
    <p v-if="correctedAnswer">{{ correctedAnswer.join(', ') }}</p>
  </div>
</template>

<style lang="scss" scoped>
.match-lines-for-stations {
  display: flex;
  flex-direction: column;
}
</style>
