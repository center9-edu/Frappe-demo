<template>
  <div class="space-y-4">
    <h1 class="text-5xl font-semibold text-ink-gray-9">Bài nộp của tôi</h1>
    <ErrorMessage v-if="subs.error" :message="errorText(subs.error)" />
    <LoadingText v-else-if="!subs.data" />
    <div v-else-if="!subs.data.length" class="rounded-6 border border-dashed border-outline-gray-3 p-10 text-center text-ink-gray-5">
      Bạn chưa nộp bài tập nào.
    </div>
    <div v-else class="overflow-hidden rounded-6 border border-outline-gray-2 bg-surface-base">
      <table class="w-full text-left text-base">
        <thead class="bg-surface-gray-2 text-sm text-ink-gray-5">
          <tr>
            <th class="px-4 py-2 font-medium">Bài tập</th>
            <th class="px-4 py-2 font-medium">Khoá học</th>
            <th class="px-4 py-2 font-medium">Trạng thái</th>
            <th class="px-4 py-2 font-medium">Điểm</th>
            <th class="px-4 py-2 font-medium">Cập nhật</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="s in subs.data"
            :key="s.name"
            class="cursor-pointer border-t border-outline-gray-1 hover:bg-surface-gray-1"
            @click="router.push({ name: 'Lesson', params: { course: s.course, lesson: s.lesson } })"
          >
            <td class="px-4 py-3 font-medium text-ink-gray-9">{{ s.assignment_title }}</td>
            <td class="px-4 py-3 text-ink-gray-7">{{ s.course_title }}</td>
            <td class="px-4 py-3">
              <StatusBadge :submission="s" />
            </td>
            <td class="px-4 py-3 text-ink-gray-7">{{ s.status === 'Graded' ? s.score : '—' }}</td>
            <td class="px-4 py-3 text-ink-gray-5">{{ formatDate(s.modified) }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { ErrorMessage, LoadingText } from 'frappe-ui'
import { errorText, formatDate, useApi } from '../api'
import StatusBadge from '../components/StatusBadge.vue'

const router = useRouter()
const subs = useApi('get_my_submissions')
</script>
