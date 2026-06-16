<script setup lang="ts">
import BaseButton from './BaseButton.vue'
import { ref } from 'vue'
import logoImage from '../assets/logo.png'

const isMobileMenuOpen = ref(false)

const navItems = [
  { name: 'Accueil', href: '#' },
  { name: 'Médicaments', href: '#' },
  { name: 'Pharmacies', href: '#' },
  { name: 'Réservations', href: '#' },
  { name: 'Ordonnances', href: '#' },
  { name: 'Contact', href: '#' },
]
</script>

<template>
  <header class="app-header">
    <div class="container">
      <div class="header-content">
        <div class="logo">
          <img :src="logoImage" alt="Logo PharmaCI" class="logo-image" />
          <span class="logo-text">PhmCI</span>
        </div>

        <nav class="desktop-nav">
          <a v-for="item in navItems" :key="item.name" :href="item.href" class="nav-link">
            {{ item.name }}
          </a>
        </nav>

        <div class="auth-buttons">
          <BaseButton variant="secondary" size="small">Se connecter</BaseButton>
          <BaseButton variant="primary" size="small">S'inscrire</BaseButton>
        </div>

        <button class="mobile-menu-btn" @click="isMobileMenuOpen = !isMobileMenuOpen">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="3" y1="6" x2="21" y2="6" />
            <line x1="3" y1="12" x2="21" y2="12" />
            <line x1="3" y1="18" x2="21" y2="18" />
          </svg>
        </button>
      </div>

      <div v-if="isMobileMenuOpen" class="mobile-menu">
        <nav class="mobile-nav">
          <a v-for="item in navItems" :key="item.name" :href="item.href" class="nav-link">
            {{ item.name }}
          </a>
        </nav>
        <div class="mobile-auth">
          <BaseButton variant="secondary" size="medium" style="width: 100%">Se connecter</BaseButton>
          <BaseButton variant="primary" size="medium" style="width: 100%">S'inscrire</BaseButton>
        </div>
      </div>
    </div>
  </header>
</template>

<style scoped>
.app-header {
  background: var(--bg);
  border-bottom: 1px solid var(--border);
  position: sticky;
  top: 0;
  z-index: 100;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  min-height: 80px;
  gap: 30px;
}

.logo {
  display: flex;
  align-items: center;
  gap: 16px;
  flex-shrink: 0;
}

.logo-image {
  height: 73px;
  width: auto;
  object-fit: contain;
}

.logo-text {
  font-size: 26px;
  font-weight: 700;
  color: var(--accent);
  font-family: var(--heading);
}

.desktop-nav {
  display: flex;
  gap: 32px;
}

.nav-link {
  color: var(--text);
  text-decoration: none;
  font-weight: 500;
  transition: color 0.2s ease;
}

.nav-link:hover {
  color: var(--accent);
}

.auth-buttons {
  display: flex;
  gap: 12px;
}

.mobile-menu-btn {
  display: none;
  background: none;
  border: none;
  cursor: pointer;
  padding: 8px;
  color: var(--text-h);
}

.mobile-menu {
  padding: 20px 0;
  border-top: 1px solid var(--border);
}

.mobile-nav {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-bottom: 20px;
}

.mobile-auth {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

@media (max-width: 1024px) {
  .desktop-nav,
  .auth-buttons {
    display: none;
  }

  .mobile-menu-btn {
    display: block;
  }
}

@media (min-width: 1025px) {
  .mobile-menu {
    display: none !important;
  }
}
</style>
