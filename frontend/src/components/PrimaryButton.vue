<!-- Level 5: wraps frappe-ui Button so the brand CTA style lives in one place.
     Every Button prop/slot/event still works: <PrimaryButton label="..." :route="..." @click="..." /> -->
<template>
  <Button variant="solid" theme="blue" :size="size" class="rounded-full px-5 shadow-sm" v-bind="$attrs">
    <template v-for="(_, name) in $slots" #[name]="slotProps">
      <slot :name="name" v-bind="slotProps || {}" />
    </template>
  </Button>
</template>

<script setup>
import { Button } from 'frappe-ui'

defineOptions({ inheritAttrs: false })
defineProps({ size: { type: String, default: 'md' } })
</script>
