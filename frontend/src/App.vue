<template>
  <FrappeUIProvider>
    <div class="min-h-screen bg-surface-gray-1">
      <header class="sticky top-0 z-10 border-b border-outline-gray-2 bg-surface-base">
        <div class="mx-auto flex h-14 max-w-6xl items-center gap-3 px-4 sm:gap-6">
          <router-link to="/" class="flex items-center gap-2 font-semibold text-ink-gray-9">
            <span class="grid size-7 place-items-center rounded-3 bg-surface-blue-6 text-sm text-ink-base">L</span>
            <span class="hidden sm:inline">LearnHub</span>
          </router-link>
          <nav class="flex gap-1">
            <Button variant="ghost" label="Khoá học" icon-left="lucide-book-open" :route="{ name: 'Courses' }" />
            <Button variant="ghost" label="Bài nộp của tôi" icon-left="lucide-file-check" :route="{ name: 'Submissions' }" />
          </nav>
          <div class="ml-auto flex items-center gap-3">
            <Avatar :label="user.full_name" :image="user.user_image" size="md" />
            <span class="hidden text-sm text-ink-gray-7 sm:inline">{{ user.full_name }}</span>
            <Button variant="ghost" icon="lucide-log-out" label="Đăng xuất" tooltip="Đăng xuất" @click="logout" />
          </div>
        </div>
      </header>
      <main class="mx-auto max-w-6xl px-4 py-8">
        <router-view />
      </main>
    </div>
  </FrappeUIProvider>
</template>

<script setup>
import { Avatar, Button, FrappeUIProvider } from 'frappe-ui'
import { user } from './session'

async function logout() {
  await fetch('/api/method/logout', { method: 'POST', headers: { 'X-Frappe-CSRF-Token': window.csrf_token } })
  window.location.href = '/login'
}
</script>
