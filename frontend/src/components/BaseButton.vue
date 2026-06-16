<script setup lang="ts">
interface Props {
  variant?: 'primary' | 'secondary' | 'outline'
  size?: 'small' | 'medium' | 'large'
  disabled?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'primary',
  size: 'medium',
  disabled: false,
})
</script>

<template>
  <button
    :disabled="disabled"
    class="base-button"
    :class="[
      `variant-${variant}`,
      `size-${size}`,
      { disabled: disabled }
    ]"
  >
    <slot />
  </button>
</template>

<style scoped>
.base-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-family: var(--sans);
  font-weight: 500;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  text-decoration: none;
  gap: 8px;
}

.base-button:not(.disabled):hover {
  transform: translateY(-1px);
  box-shadow: var(--shadow);
}

.base-button.disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.variant-primary {
  background: var(--accent);
  color: white;
}

.variant-secondary {
  background: var(--accent-bg);
  color: var(--accent);
  border: 1px solid var(--accent-border);
}

.variant-outline {
  background: transparent;
  color: var(--accent);
  border: 2px solid var(--accent);
}

.size-small {
  padding: 6px 12px;
  font-size: 14px;
}

.size-medium {
  padding: 10px 20px;
  font-size: 16px;
}

.size-large {
  padding: 14px 28px;
  font-size: 18px;
}
</style>
