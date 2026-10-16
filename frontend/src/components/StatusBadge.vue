<!-- Level 5: one place that maps an Assignment Submission to a frappe-ui Badge. -->
<template>
  <Badge :theme="state.theme" :label="state.label" size="md">
    <template #prefix><span :class="state.icon" class="size-3.5" /></template>
  </Badge>
</template>

<script setup>
import { computed } from 'vue'
import { Badge } from 'frappe-ui'

const props = defineProps({
  // { status: 'Submitted' | 'Graded', score } or null when nothing was submitted
  submission: { type: Object, default: null },
})

const state = computed(() => {
  const s = props.submission
  if (!s) return { theme: 'amber', label: 'Chưa nộp', icon: 'lucide-clock' }
  if (s.status === 'Graded') return { theme: 'green', label: `Đã chấm · ${s.score} điểm`, icon: 'lucide-award' }
  return { theme: 'blue', label: 'Chờ chấm', icon: 'lucide-hourglass' }
})
</script>
