<script setup lang="ts">
import AppHeader from './components/AppHeader.vue'
import BaseButton from './components/BaseButton.vue'
import BaseCard from './components/BaseCard.vue'

const features = [
  {
    title: 'Recherche de médicaments',
    description: 'Trouvez rapidement vos médicaments et vérifiez leur disponibilité en temps réel.',
    icon: 'search'
  },
  {
    title: 'Comparaison de prix',
    description: 'Comparez les prix des médicaments dans différentes pharmacies près de chez vous.',
    icon: 'dollar-sign'
  },
  {
    title: 'Localisation de pharmacies',
    description: 'Trouvez les pharmacies disponibles à proximité et consultez leurs horaires.',
    icon: 'map-pin'
  },
  {
    title: 'Réservations en ligne',
    description: 'Réservez vos médicaments en ligne et récupérez-les en pharmacie.',
    icon: 'shopping-cart'
  },
  {
    title: 'Gestion des ordonnances',
    description: 'Gérez vos ordonnances électroniques facilement depuis votre compte.',
    icon: 'file-text'
  },
  {
    title: 'Notifications',
    description: 'Recevez des notifications pour vos réservations et rappels de médicaments.',
    icon: 'bell'
  }
]
</script>

<template>
  <div id="app">
    <!-- SVG Icons -->
    <svg style="display: none" xmlns="http://www.w3.org/2000/svg">
      <symbol id="search" viewBox="0 0 24 24">
        <circle cx="11" cy="11" r="8" />
        <line x1="21" y1="21" x2="16.65" y2="16.65" />
      </symbol>
      <symbol id="dollar-sign" viewBox="0 0 24 24">
        <line x1="12" y1="1" x2="12" y2="23" />
        <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6" />
      </symbol>
      <symbol id="map-pin" viewBox="0 0 24 24">
        <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z" />
        <circle cx="12" cy="10" r="3" />
      </symbol>
      <symbol id="shopping-cart" viewBox="0 0 24 24">
        <circle cx="9" cy="21" r="1" />
        <circle cx="20" cy="21" r="1" />
        <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6" />
      </symbol>
      <symbol id="file-text" viewBox="0 0 24 24">
        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
        <polyline points="14 2 14 8 20 8" />
        <line x1="16" y1="13" x2="8" y2="13" />
        <line x1="16" y1="17" x2="8" y2="17" />
        <polyline points="10 9 9 9 8 9" />
      </symbol>
      <symbol id="bell" viewBox="0 0 24 24">
        <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9" />
        <path d="M13.73 21a2 2 0 0 1-3.46 0" />
      </symbol>
    </svg>

    <AppHeader />

    <!-- Hero Section -->
    <section class="hero-section">
      <div class="container">
        <div class="hero-content">
          <h1 class="hero-title">PharmaCI</h1>
          <p class="hero-subtitle">Votre plateforme pour consulter les prix des médicaments et vérifier leur disponibilité en pharmacie.</p>
          <div class="hero-buttons">
            <BaseButton size="large">Rechercher un médicament</BaseButton>
            <BaseButton variant="secondary" size="large">Voir les pharmacies</BaseButton>
          </div>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section class="features-section">
      <div class="container">
        <h2 class="section-title">Nos Services</h2>
        <p class="section-subtitle">Découvrez toutes les fonctionnalités qui facilitent votre accès aux médicaments</p>
        <div class="features-grid">
          <BaseCard v-for="(feature, index) in features" :key="index" class="feature-card">
            <div class="feature-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <use :xlink:href="`#${feature.icon}`" />
              </svg>
            </div>
            <h3 class="feature-title">{{ feature.title }}</h3>
            <p class="feature-description">{{ feature.description }}</p>
          </BaseCard>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="footer">
      <div class="container">
        <div class="footer-content">
          <div class="footer-logo">
            <span class="logo-text">PharmaCI</span>
            <p class="footer-text">Votre santé, notre priorité</p>
          </div>
          <div class="footer-links">
            <a href="#" class="footer-link">À propos</a>
            <a href="#" class="footer-link">Contact</a>
            <a href="#" class="footer-link">Conditions d'utilisation</a>
            <a href="#" class="footer-link">Politique de confidentialité</a>
          </div>
        </div>
        <div class="footer-bottom">
          <p>&copy; 2026 PharmaCI. Tous droits réservés.</p>
        </div>
      </div>
    </footer>
  </div>
</template>

<style scoped>
#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

/* Hero Section */
.hero-section {
  padding: 80px 0;
  background: linear-gradient(135deg, var(--accent-bg) 0%, var(--bg) 100%);
}

.hero-content {
  text-align: center;
  max-width: 800px;
  margin: 0 auto;
}

.hero-title {
  font-size: 64px;
  margin-bottom: 16px;
  color: var(--accent);
}

.hero-subtitle {
  font-size: 20px;
  color: var(--text);
  margin-bottom: 40px;
  line-height: 1.6;
}

.hero-buttons {
  display: flex;
  gap: 16px;
  justify-content: center;
  flex-wrap: wrap;
}

/* Features Section */
.features-section {
  padding: 80px 0;
}

.section-title {
  text-align: center;
  margin-bottom: 12px;
}

.section-subtitle {
  text-align: center;
  color: var(--text);
  margin-bottom: 48px;
  font-size: 18px;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 24px;
}

.feature-card {
  text-align: center;
}

.feature-icon {
  width: 64px;
  height: 64px;
  margin: 0 auto 20px;
  background: var(--accent-bg);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--accent);
}

.feature-icon svg {
  width: 32px;
  height: 32px;
}

.feature-title {
  margin-bottom: 12px;
}

.feature-description {
  color: var(--text);
  line-height: 1.6;
}

/* Footer */
.footer {
  margin-top: auto;
  background: var(--text-h);
  color: var(--bg);
  padding: 40px 0 20px;
}

.footer-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 24px;
  margin-bottom: 24px;
}

.footer-logo .logo-text {
  font-size: 24px;
  font-weight: 700;
  color: var(--accent);
  display: block;
  margin-bottom: 8px;
}

.footer-text {
  color: var(--border);
}

.footer-links {
  display: flex;
  gap: 24px;
  flex-wrap: wrap;
}

.footer-link {
  color: var(--border);
  text-decoration: none;
  transition: color 0.2s ease;
}

.footer-link:hover {
  color: var(--accent);
}

.footer-bottom {
  text-align: center;
  padding-top: 20px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.footer-bottom p {
  color: var(--border);
  font-size: 14px;
}

@media (max-width: 1024px) {
  .hero-title {
    font-size: 48px;
  }

  .hero-section {
    padding: 60px 0;
  }

  .features-section {
    padding: 60px 0;
  }

  .footer-content {
    flex-direction: column;
    text-align: center;
  }
}

@media (max-width: 640px) {
  .hero-title {
    font-size: 36px;
  }

  .hero-buttons {
    flex-direction: column;
    width: 100%;
  }

  .hero-buttons button {
    width: 100%;
  }
}
</style>
