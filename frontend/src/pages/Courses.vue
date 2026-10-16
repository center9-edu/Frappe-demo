<template>
  <div>
    <div class="mb-6 flex flex-wrap items-end justify-between gap-4">
      <div>
        <h1 class="text-5xl font-semibold text-ink-gray-9">Xin chào, {{ firstName }} 👋</h1>
        <p class="mt-1 text-base text-ink-gray-5">Tiếp tục hành trình học tập của bạn.</p>
      </div>
      <TabButtons v-model="tab" :options="tabs" />
    </div>

    <ErrorMessage v-if="courses.error" :message="errorText(courses.error)" />
    <div v-else-if="courses.loading && !courses.data" class="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
      <Skeleton v-for="i in 3" :key="i" class="h-64 rounded-6" />
    </div>
    <div v-else-if="!visible.length" class="rounded-6 border border-dashed border-outline-gray-3 p-10 text-center text-ink-gray-5">
      {{ tab === 'mine' ? 'Bạn chưa ghi danh khoá học nào.' : 'Chưa có khoá học nào.' }}
    </div>
    <div v-else class="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
      <router-link
        v-for="c in visible"
        :key="c.name"
        :to="{ name: 'Course', params: { course: c.name } }"
        class="group flex flex-col overflow-hidden rounded-6 border border-outline-gray-2 bg-surface-base transition hover:shadow-lg"
      >
        <div
          class="grid h-36 place-items-center bg-gradient-to-br from-surface-blue-2 to-surface-violet-3 bg-cover bg-center"
          :style="c.image ? { backgroundImage: `url(${c.image})` } : {}"
        >
          <span v-if="!c.image" class="text-12xl font-bold text-ink-violet-5">{{ c.title[0] }}</span>
        </div>
        <div class="flex flex-1 flex-col gap-2 p-4">
          <div class="flex items-start justify-between gap-2">
            <h3 class="text-2xl font-semibold text-ink-gray-9 group-hover:underline">{{ c.title }}</h3>
            <Badge v-if="c.enrolled" theme="green" label="Đã ghi danh" />
          </div>
          <p class="line-clamp-2 text-sm text-ink-gray-6">{{ c.short_intro }}</p>
          <div class="mt-auto flex items-center justify-between pt-2 text-sm text-ink-gray-5">
            <span class="flex items-center gap-1"><span class="lucide-book-open size-4" /> {{ c.lesson_count }} bài học</span>
            <span v-if="c.instructor_name" class="flex items-center gap-1"><span class="lucide-user size-4" /> {{ c.instructor_name }}</span>
          </div>
          <Progress v-if="c.enrolled" :value="c.progress" :label="`Tiến độ ${c.progress}%`" size="sm" />
        </div>
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { Badge, ErrorMessage, Progress, Skeleton, TabButtons } from 'frappe-ui'
import { errorText, useApi } from '../api'

const firstName = (window.user?.full_name || '').split(' ').pop()
const tab = ref('all')
const tabs = [
  { label: 'Tất cả', value: 'all' },
  { label: 'Của tôi', value: 'mine' },
]

const courses = useApi('get_courses')
const visible = computed(() => (courses.data || []).filter((c) => tab.value === 'all' || c.enrolled))
</script>
