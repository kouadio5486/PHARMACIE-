<script setup lang="ts">
</script>

<template>
  <div class="base-card">
    <slot />
  </div>
</template>

<style scoped>
.base-card {
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 24px;
  box-shadow: var(--shadow);
  transition: transform 0.2s ease;
}

.base-card:hover {
  transform: translateY(-4px);
}
</style>
