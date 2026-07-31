<script setup lang="ts">
import SelectableLines from '@/components/SelectableLines.vue'
import { storeToRefs } from 'pinia'
import { useLineData } from '@/stores/lineData.ts'
import { ref, watch } from 'vue'
import type { Line, LineName, LineStop } from '@/types/lines.ts'
import BaseButton from '@/components/BaseButton.vue'
import BaseLine from '@/components/BaseLine.vue'

const { initialized, stops, lines } = storeToRefs(useLineData())

const getAllDeselectedConfiguration = () =>
  Object.fromEntries(Object.keys(lines).map((lineName) => [lineName, false])) as Record<
    LineName,
    boolean
  >
const lineSelections = ref(getAllDeselectedConfiguration())

const correctedAnswer = ref<Array<Line> | null>(null)
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
    correctedAnswer.value = correctAnswer.map(
      (lineName) => lines.value.find((line) => line.name === lineName)!,
    )
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
    <div v-if="correctedAnswer" class="mt-24">
      <p class="mb-12">Richtig wäre gewesen:</p>
      <ul>
        <li v-for="line in correctedAnswer" :key="line.name">
          <base-line :line="line" />
        </li>
      </ul>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.match-lines-for-stations {
  display: flex;
  flex-direction: column;
}

ul {
  margin: 0;
  padding: 0;
  display: flex;
  flex-wrap: wrap;
  column-gap: 0.5rem;
  row-gap: 0.75rem;
}

li {
  list-style: none;
}
</style>
