<template>
  <div>
    <div class="mb-8 flex flex-wrap items-end justify-between gap-4">
      <div>
        <h1 class="text-5xl font-semibold text-ink-gray-9">Xin chào, {{ firstName }} 👋</h1>
        <p class="mt-1 text-base text-ink-gray-5">Tiếp tục hành trình học tập của bạn.</p>
      </div>
      <TabButtons v-model="tab" :options="tabs" />
    </div>

    <ErrorMessage v-if="courses.error" :message="errorText(courses.error)" />
    <div v-else-if="courses.loading && !courses.data" class="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
      <Skeleton v-for="i in 3" :key="i" class="h-72 rounded-7" />
    </div>
    <div v-else-if="!visible.length" class="rounded-7 border border-dashed border-outline-gray-3 p-10 text-center text-ink-gray-5">
      {{ tab === 'mine' ? 'Bạn chưa ghi danh khoá học nào.' : 'Chưa có khoá học nào.' }}
    </div>
    <div v-else class="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
      <CourseCard v-for="c in visible" :key="c.name" :course="c" />
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { ErrorMessage, Skeleton, TabButtons } from 'frappe-ui'
import { errorText, useApi } from '../api'
import CourseCard from '../components/CourseCard.vue'
import { user } from '../session'

const firstName = computed(() => user.full_name.split(' ').pop())
const tab = ref('all')
const tabs = [
  { label: 'Tất cả', value: 'all' },
  { label: 'Của tôi', value: 'mine' },
]

const courses = useApi('get_courses')
const visible = computed(() => (courses.data || []).filter((c) => tab.value === 'all' || c.enrolled))
</script>
