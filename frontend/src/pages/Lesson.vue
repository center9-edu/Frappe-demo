<template>
  <ErrorMessage v-if="lesson.error" :message="errorText(lesson.error)" />
  <div v-else-if="l" class="grid gap-6 lg:grid-cols-[280px_1fr]">
    <aside class="h-fit rounded-6 border border-outline-gray-2 bg-surface-base p-4 lg:sticky lg:top-20">
      <router-link :to="{ name: 'Course', params: { course } }" class="mb-3 flex items-center gap-1 text-sm text-ink-gray-5 hover:text-ink-gray-8">
        <span class="lucide-arrow-left size-4" /> {{ l.course_title }}
      </router-link>
      <Progress :value="l.progress" :label="`Hoàn thành ${l.progress}%`" size="sm" class="progress-brand mb-4" />
      <div v-for="(ch, i) in l.chapters" :key="ch.name" class="mb-3">
        <div class="mb-1 px-2 text-xs font-semibold uppercase tracking-wide text-ink-gray-5">{{ i + 1 }}. {{ ch.title }}</div>
        <router-link
          v-for="item in ch.lessons"
          :key="item.name"
          :to="{ name: 'Lesson', params: { course, lesson: item.name } }"
          class="flex items-center gap-2 rounded-3 px-2 py-1.5 text-sm"
          :class="item.name === l.name ? 'bg-surface-gray-3 font-medium text-ink-gray-9' : 'text-ink-gray-7 hover:bg-surface-gray-2'"
        >
          <span :class="item.completed ? 'lucide-circle-check text-ink-green-6' : 'lucide-circle text-ink-gray-4'" class="size-4 shrink-0" />
          {{ item.title }}
        </router-link>
      </div>
    </aside>

    <article class="min-w-0 space-y-6">
      <div class="rounded-6 border border-outline-gray-2 bg-surface-base p-6">
        <div class="mb-4 flex flex-wrap items-center justify-between gap-3">
          <div>
            <div class="text-sm text-ink-gray-5">Bài {{ l.position }}/{{ l.total }}</div>
            <h1 class="text-7xl font-semibold text-ink-gray-9">{{ l.title }}</h1>
          </div>
          <Button
            :variant="l.completed ? 'subtle' : 'solid'"
            :theme="l.completed ? 'green' : 'blue'"
            :icon-left="l.completed ? 'lucide-circle-check' : 'lucide-check'"
            :label="l.completed ? 'Đã hoàn thành' : 'Đánh dấu hoàn thành'"
            :loading="progress.loading"
            @click="toggleCompleted"
          />
        </div>

        <div v-if="embedUrl" class="mb-6 aspect-video overflow-hidden rounded-4 bg-surface-gray-2">
          <iframe :src="embedUrl" class="size-full" allowfullscreen />
        </div>
        <Button v-else-if="l.video_url" class="mb-6" icon-left="lucide-play" label="Xem video" :href="l.video_url" />

        <div class="lesson-content" v-html="l.content" />
      </div>

      <div v-for="a in l.assignments" :key="a.name" class="rounded-6 border border-outline-amber-2 bg-surface-amber-1 p-6">
        <div class="mb-2 flex flex-wrap items-center justify-between gap-2">
          <h2 class="flex items-center gap-2 text-2xl font-semibold text-ink-gray-9">
            <span class="lucide-clipboard-pen size-5" /> Bài tập: {{ a.title }}
          </h2>
          <StatusBadge :submission="a.submission" />
        </div>
        <div class="lesson-content mb-4" v-html="a.question" />
        <Alert v-if="a.submission?.feedback" theme="green" title="Nhận xét của giảng viên" :description="a.submission.feedback" class="mb-4" />
        <PrimaryButton
          v-if="a.submission?.status !== 'Graded'"
          :icon-left="a.submission ? 'lucide-pencil' : 'lucide-send'"
          :label="a.submission ? 'Sửa bài nộp' : 'Nộp bài'"
          @click="openSubmit(a)"
        />
      </div>

      <nav class="flex items-center justify-between gap-3">
        <Button v-if="l.prev" variant="outline" size="md" class="rounded-full" icon-left="lucide-arrow-left" :label="l.prev.title" :route="{ name: 'Lesson', params: { course, lesson: l.prev.name } }" />
        <span v-else />
        <PrimaryButton v-if="l.next" icon-right="lucide-arrow-right" :label="l.next.title" :route="{ name: 'Lesson', params: { course, lesson: l.next.name } }" />
      </nav>
    </article>

    <Dialog v-model:open="dialog.open" :title="`Nộp bài: ${dialog.assignment?.title || ''}`" size="lg">
      <template #default>
        <Textarea
          v-model="dialog.answer"
          :rows="6"
          :placeholder="dialog.assignment?.submission_type === 'URL' ? 'https://github.com/...' : 'Nhập câu trả lời của bạn'"
        />
        <ErrorMessage v-if="submit.error" class="mt-2" :message="errorText(submit.error)" />
      </template>
      <template #actions>
        <div class="flex justify-end gap-2">
          <Button label="Huỷ" @click="dialog.open = false" />
          <PrimaryButton size="sm" label="Nộp bài" :loading="submit.loading" @click="doSubmit" />
        </div>
      </template>
    </Dialog>
  </div>
  <LoadingText v-else />
</template>

<script setup>
import { computed, reactive } from 'vue'
import { useRoute } from 'vue-router'
import { Alert, Button, Dialog, ErrorMessage, LoadingText, Progress, Textarea, toast } from 'frappe-ui'
import { errorText, useApi } from '../api'
import PrimaryButton from '../components/PrimaryButton.vue'
import StatusBadge from '../components/StatusBadge.vue'

const route = useRoute()
const course = computed(() => route.params.course)
const lesson = useApi('get_lesson', {
  params: () => ({ course: route.params.course, lesson: route.params.lesson }),
  refetch: true,
})
const l = computed(() => lesson.data)

const embedUrl = computed(() => {
  const m = l.value?.video_url?.match(/(?:youtube\.com\/watch\?v=|youtu\.be\/)([\w-]{11})/)
  return m && `https://www.youtube.com/embed/${m[1]}`
})

const progress = useApi('set_lesson_completed', { method: 'POST', immediate: false })
async function toggleCompleted() {
  await progress.submit({ lesson: l.value.name, completed: !l.value.completed })
  if (progress.error) return toast.error(errorText(progress.error))
  if (!l.value.completed) toast.success('Tuyệt! Đã hoàn thành bài học 🎉')
  lesson.reload()
}

const dialog = reactive({ open: false, assignment: null, answer: '' })
const submit = useApi('submit_assignment', { method: 'POST', immediate: false })
function openSubmit(a) {
  Object.assign(dialog, { open: true, assignment: a, answer: a.submission?.answer || '' })
}
async function doSubmit() {
  await submit.submit({ assignment: dialog.assignment.name, answer: dialog.answer })
  if (submit.error) return
  dialog.open = false
  toast.success('Đã nộp bài')
  lesson.reload()
}
</script>
