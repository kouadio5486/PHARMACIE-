<script setup lang="ts">
interface Props {
  name: string
  size?: number
}

const props = withDefaults(defineProps<Props>(), {
  size: 24,
})
</script>

<template>
  <svg
    :width="size"
    :height="size"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    stroke-width="2"
    stroke-linecap="round"
    stroke-linejoin="round"
  >
    <use :xlink:href="`#${name}`" />
  </svg>
</template>
