<template>
  <ErrorMessage v-if="course.error" :message="errorText(course.error)" />
  <div v-else-if="c" class="space-y-6">
    <Breadcrumbs :items="[{ label: 'Khoá học', route: { name: 'Courses' } }, { label: c.title }]" />

    <section class="rounded-6 border border-outline-gray-2 bg-surface-base p-6">
      <div class="flex flex-wrap items-start justify-between gap-6">
        <div class="max-w-2xl space-y-3">
          <h1 class="text-8xl font-semibold text-ink-gray-9">{{ c.title }}</h1>
          <p class="text-xl text-ink-gray-6">{{ c.short_intro }}</p>
          <div class="flex flex-wrap gap-2">
            <Badge :label="`${c.chapters.length} chương`" />
            <Badge :label="`${c.lesson_count} bài học`" />
            <Badge v-if="c.instructor_name" theme="blue" :label="`Giảng viên: ${c.instructor_name}`" />
          </div>
        </div>
        <div v-if="c.enrolled" class="w-full space-y-3 sm:w-64">
          <Progress :value="c.progress" :label="`Hoàn thành ${c.progress}%`" size="md" />
          <Button
            v-if="c.next_lesson"
            variant="solid"
            size="lg"
            class="w-full"
            :label="c.progress ? 'Học tiếp' : 'Bắt đầu học'"
            icon-right="lucide-arrow-right"
            :route="{ name: 'Lesson', params: { course: c.name, lesson: c.next_lesson } }"
          />
        </div>
      </div>
    </section>

    <div class="grid gap-6 lg:grid-cols-[1fr_320px]">
      <section class="space-y-4">
        <div v-if="c.description" class="lesson-content rounded-6 border border-outline-gray-2 bg-surface-base p-6" v-html="c.description" />

        <div class="rounded-6 border border-outline-gray-2 bg-surface-base">
          <h2 class="border-b border-outline-gray-2 px-5 py-3 text-2xl font-semibold text-ink-gray-9">Nội dung khoá học</h2>
          <div v-for="(ch, i) in c.chapters" :key="ch.name" class="border-b border-outline-gray-1 px-5 py-4 last:border-0">
            <div class="mb-2 font-medium text-ink-gray-8">Chương {{ i + 1 }}. {{ ch.title }}</div>
            <component
              :is="c.enrolled ? 'router-link' : 'div'"
              v-for="l in ch.lessons"
              :key="l.name"
              :to="{ name: 'Lesson', params: { course: c.name, lesson: l.name } }"
              class="flex items-center gap-3 rounded-3 px-2 py-2 text-base text-ink-gray-7"
              :class="c.enrolled && 'hover:bg-surface-gray-2'"
            >
              <span v-if="l.completed" class="lucide-circle-check size-4 text-ink-green-6" />
              <span v-else-if="c.enrolled" class="lucide-circle size-4 text-ink-gray-4" />
              <span v-else class="lucide-lock size-4 text-ink-gray-4" />
              {{ l.title }}
            </component>
          </div>
        </div>
      </section>

      <aside class="space-y-3">
        <div class="rounded-6 border border-outline-gray-2 bg-surface-base p-5">
          <h3 class="mb-3 font-semibold text-ink-gray-9">Lớp học</h3>
          <Alert v-if="!c.enrolled" theme="blue" title="Ghi danh để mở khoá bài học" class="mb-3" />
          <div v-if="!c.batches.length" class="text-sm text-ink-gray-5">Chưa có lớp nào đang mở.</div>
          <div v-for="b in c.batches" :key="b.name" class="space-y-2 border-t border-outline-gray-1 py-3 first:border-0 first:pt-0">
            <div class="font-medium text-ink-gray-8">{{ b.title }}</div>
            <div class="flex items-center gap-1 text-sm text-ink-gray-5">
              <span class="lucide-calendar size-4" />
              {{ formatDate(b.start_date) }}<template v-if="b.end_date"> – {{ formatDate(b.end_date) }}</template>
            </div>
            <div class="flex items-center gap-1 text-sm text-ink-gray-5">
              <span class="lucide-users size-4" /> {{ b.student_count }} học viên
            </div>
            <Badge v-if="b.is_member" theme="green" label="Bạn đang trong lớp này" />
            <Button
              v-else
              variant="solid"
              class="w-full"
              label="Ghi danh"
              :loading="enroll.loading && enrolling === b.name"
              @click="doEnroll(b.name)"
            />
          </div>
        </div>
      </aside>
    </div>
  </div>
  <LoadingText v-else />
</template>

<script setup>
import { computed, ref } from 'vue'
import { useRoute } from 'vue-router'
import { Alert, Badge, Breadcrumbs, Button, ErrorMessage, LoadingText, Progress, toast } from 'frappe-ui'
import { errorText, formatDate, useApi } from '../api'

const route = useRoute()
const course = useApi('get_course', { params: () => ({ course: route.params.course }), refetch: true })
const c = computed(() => course.data)

const enrolling = ref(null)
const enroll = useApi('enroll', { method: 'POST', immediate: false })

async function doEnroll(batch) {
  enrolling.value = batch
  await enroll.submit({ batch })
  if (enroll.error) return toast.error(errorText(enroll.error))
  toast.success('Ghi danh thành công!')
  course.reload()
}
</script>
