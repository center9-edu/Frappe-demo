<!-- Level 6: a component frappe-ui does not ship, drawn with its color tokens
     (CSS variables), so it follows the brand theme and dark mode. -->
<template>
  <div class="relative grid shrink-0 place-items-center" :style="{ width: `${size}px`, height: `${size}px` }">
    <svg :width="size" :height="size" class="-rotate-90" role="img" :aria-label="`Hoàn thành ${percent}%`">
      <circle :cx="c" :cy="c" :r="r" fill="none" stroke="var(--surface-gray-3)" :stroke-width="stroke" />
      <circle
        :cx="c"
        :cy="c"
        :r="r"
        fill="none"
        stroke="var(--surface-blue-6)"
        :stroke-width="stroke"
        stroke-linecap="round"
        :stroke-dasharray="length"
        :stroke-dashoffset="length * (1 - percent / 100)"
        class="transition-[stroke-dashoffset] duration-700"
      />
    </svg>
    <div class="absolute text-center leading-tight">
      <div class="text-3xl font-semibold text-ink-gray-9">{{ percent }}%</div>
      <div v-if="label" class="text-xs text-ink-gray-5">{{ label }}</div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  value: { type: Number, default: 0 },
  size: { type: Number, default: 104 },
  stroke: { type: Number, default: 9 },
  label: { type: String, default: '' },
})

const percent = computed(() => Math.min(100, Math.max(0, Math.round(props.value))))
const c = computed(() => props.size / 2)
const r = computed(() => (props.size - props.stroke) / 2)
const length = computed(() => 2 * Math.PI * r.value)
</script>
