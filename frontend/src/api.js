import { useCall } from 'frappe-ui'

// Every call goes to a whitelisted function in apps/learning/learning/api.py
export function useApi(method, options = {}) {
  return useCall({ url: `/api/v2/method/learning.api.${method}`, ...options })
}

export function errorText(error) {
  return error?.message?.replace(/^\w+: /, '') || 'Đã có lỗi xảy ra'
}

export function formatDate(value) {
  return value ? new Date(value).toLocaleDateString('vi-VN') : ''
}
