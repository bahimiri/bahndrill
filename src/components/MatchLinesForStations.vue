<script setup lang="ts">
import SelectableLines from '@/components/SelectableLines.vue'
import { storeToRefs } from 'pinia'
import { useLineData } from '@/stores/lineData.ts'
import { nextTick, onBeforeMount, onMounted, ref, watch, watchEffect } from 'vue'
import type { LineName, LineStop } from '@/types/lines.ts'

const { initialized, stops, lines } = storeToRefs(useLineData())

const lineSelections = ref(
  Object.fromEntries(Object.keys(lines).map((lineName) => [lineName, false])) as Record<
    LineName,
    boolean
  >,
)

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

const checkAnswer = () => {
  const selectedLines = Object.keys(lineSelections.value).filter(
    (lineName) => lineSelections.value[lineName as LineName],
  )
  const correctAnswer = stop.value!.lines
  const isCorrect =
    correctAnswer.filter((line) => selectedLines.includes(line)).length === correctAnswer.length
  if (!isCorrect) {
    correctedAnswer.value = correctAnswer
  }
}

const handleContinue = () => {
  if (correctedAnswer.value) {
    correctedAnswer.value = null
    stop.value = getNextStop()
  } else {
    checkAnswer()
  }
}
</script>

<template>
  <div>
    <h2>{{ stop?.name }}</h2>
    <selectable-lines v-model="lineSelections" />
    <button @click="handleContinue()">Weiter</button>
    <p v-if="correctedAnswer">{{ correctedAnswer.join(', ') }}</p>
  </div>
</template>
