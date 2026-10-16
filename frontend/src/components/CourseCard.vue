<!-- Level 6: app-specific card built from Tailwind + frappe-ui tokens,
     with frappe-ui Badge/Progress inside. -->
<template>
  <router-link
    :to="{ name: 'Course', params: { course: course.name } }"
    class="group flex flex-col overflow-hidden rounded-7 border border-outline-gray-2 bg-surface-base transition duration-200 hover:-translate-y-1 hover:border-outline-blue-3 hover:shadow-xl"
  >
    <div
      class="relative grid h-40 place-items-center bg-cover bg-center"
      :class="!course.image && 'bg-gradient-to-br from-surface-blue-3 via-surface-blue-2 to-surface-amber-2'"
      :style="course.image ? { backgroundImage: `url(${course.image})` } : {}"
    >
      <span v-if="!course.image" class="text-12xl font-bold text-ink-blue-6 transition group-hover:scale-110">
        {{ course.title[0] }}
      </span>
      <Badge v-if="course.enrolled" theme="green" variant="solid" label="Đã ghi danh" class="absolute right-3 top-3" />
    </div>

    <div class="flex flex-1 flex-col gap-2 p-5">
      <h3 class="text-2xl font-semibold text-ink-gray-9 group-hover:text-ink-blue-6">{{ course.title }}</h3>
      <p class="line-clamp-2 text-base text-ink-gray-6">{{ course.short_intro }}</p>

      <div class="mt-auto flex items-center gap-4 pt-3 text-sm text-ink-gray-5">
        <span class="flex items-center gap-1"><span class="lucide-book-open size-4" /> {{ course.lesson_count }} bài học</span>
        <span v-if="course.instructor_name" class="flex items-center gap-1"><span class="lucide-user size-4" /> {{ course.instructor_name }}</span>
      </div>

      <Progress v-if="course.enrolled" class="progress-brand pt-2" :value="course.progress" :label="`Tiến độ ${course.progress}%`" size="sm" />
      <div v-else class="flex items-center gap-1 pt-2 text-sm font-medium text-ink-blue-6">
        Xem khoá học <span class="lucide-arrow-right size-4 transition group-hover:translate-x-1" />
      </div>
    </div>
  </router-link>
</template>

<script setup>
import { Badge, Progress } from 'frappe-ui'

defineProps({
  course: { type: Object, required: true },
})
</script>
