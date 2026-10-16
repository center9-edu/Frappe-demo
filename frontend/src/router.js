import { createRouter, createWebHistory } from 'vue-router'

export default createRouter({
  history: createWebHistory('/lms'),
  routes: [
    { path: '/', name: 'Courses', component: () => import('./pages/Courses.vue') },
    { path: '/courses/:course', name: 'Course', component: () => import('./pages/CourseDetail.vue') },
    { path: '/courses/:course/learn/:lesson', name: 'Lesson', component: () => import('./pages/Lesson.vue') },
    { path: '/submissions', name: 'Submissions', component: () => import('./pages/Submissions.vue') },
  ],
  scrollBehavior: () => ({ top: 0 }),
})
