<script setup lang="ts">
import SelectableLines from '@/components/SelectableLines.vue'
import { ref, useTemplateRef } from 'vue'
import BaseButton from '@/components/BaseButton.vue'
import CorrectionView from '@/components/CorrectionView.vue'
import SuccessBanner from '@/components/SuccessBanner.vue'
import { useLineMatchingGame } from '@/composables/useLineMatchingGame.ts'

const { stop, selectedLines, correctLines, isCorrect, startChallenge } = useLineMatchingGame()

const nextStopRef = useTemplateRef('nextStop')
const showResult = ref(false)

const handleContinue = () => {
  if (showResult.value) {
    startChallenge()
    setTimeout(() => {
      nextStopRef.value?.focus()
    }, 0)
    showResult.value = false
  } else {
    showResult.value = true
    if (isCorrect.value) {
      setTimeout(() => handleContinue(), 1000)
    }
  }
}
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
          v-model="selectedLines"
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
