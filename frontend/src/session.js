import { reactive } from 'vue'

// Built app: www/lms.py injects window.user. Vite dev server (:8080) skips lms.py, so ask the API.
export const user = reactive(window.user || { full_name: '', user_image: null })

if (!window.user) {
  fetch('/api/v2/method/learning.api.get_session')
    .then((r) => (r.ok ? r.json() : Promise.reject(r)))
    .then((r) => Object.assign(user, r.data))
    .catch(() => (window.location.href = '/login?redirect-to=' + encodeURIComponent(window.location.pathname)))
}
