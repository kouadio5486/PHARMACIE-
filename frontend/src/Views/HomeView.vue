<script setup lang="ts">
import BaseButton from '../components/BaseButton.vue'
import BaseCard from '../components/BaseCard.vue'
import heroImage from '../assets/phar.jpg'
import paracetamolImage from '../assets/image/paracetamol.png'
import amoxicillineImage from '../assets/image/amoxicilline.png'
import metformineImage from '../assets/image/metformine.png'
import phar1Image from '../assets/image/pha1.webp'
import phar2Image from '../assets/image/phar2.jpg'
import phar3Image from '../assets/image/phar3.avif'
import ord1Image from '../assets/image/ord1.webp'
import ord2Image from '../assets/image/ord2.webp'
import ord3Image from '../assets/image/ord3.jpg'

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
  <div>
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
      <symbol id="phone" viewBox="0 0 24 24">
        <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z" />
      </symbol>
      <symbol id="clock" viewBox="0 0 24 24">
        <circle cx="12" cy="12" r="10" />
        <polyline points="12 6 12 12 16 14" />
      </symbol>
    </svg>

    <!-- Hero Section -->
    <section class="hero-section" :style="{ backgroundImage: `linear-gradient(rgba(0, 0, 0, 0.4), rgba(0, 0, 0, 0.6)), url(${heroImage})` }">
      <div class="hero-content">
        <h1 class="hero-title">PharmaCI</h1>
        <p class="hero-subtitle">Votre plateforme pour consulter les prix des médicaments et vérifier leur disponibilité en pharmacie.</p>
        <div class="hero-buttons">
          <BaseButton size="large">Rechercher un médicament</BaseButton>
          <BaseButton variant="secondary" size="large">Voir les pharmacies</BaseButton>
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

    <!-- Médicaments Section -->
    <section id="medicaments" class="medicaments-section">
      <div class="container">
        <div class="section-header">
          <h2 class="section-title">Médicaments populaires</h2>
          <p class="section-subtitle">
            Découvrez quelques médicaments couramment utilisés
          </p>
        </div>

        <div class="medicaments-grid">
          <!-- Médicament 1 -->
          <BaseCard class="medicament-card" variant="elevated">
            <div class="medicament-image">
              <img :src="paracetamolImage" alt="Paracétamol" />
              <div class="medicament-category antalgique">
                Antalgique
              </div>
            </div>
            <div class="medicament-content">
              <h3 class="medicament-title">Paracétamol</h3>
              <p class="medicament-description">
                Utilisé pour soulager les douleurs légères à modérées
                et réduire la fièvre.
              </p>
              <div class="medicament-meta">
                <span class="dosage">500 mg</span>
                <span class="forme">Comprimé</span>
              </div>
            </div>
          </BaseCard>

          <!-- Médicament 2 -->
          <BaseCard class="medicament-card" variant="elevated">
            <div class="medicament-image">
              <img :src="amoxicillineImage" alt="Amoxicilline" />
              <div class="medicament-category antibiotique">
                Antibiotique
              </div>
            </div>
            <div class="medicament-content">
              <h3 class="medicament-title">Amoxicilline</h3>
              <p class="medicament-description">
                Antibiotique utilisé pour traiter diverses infections
                bactériennes.
              </p>
              <div class="medicament-meta">
                <span class="dosage">500 mg</span>
                <span class="forme">Gélule</span>
              </div>
            </div>
          </BaseCard>

          <!-- Médicament 3 -->
          <BaseCard class="medicament-card" variant="elevated">
            <div class="medicament-image">
              <img :src="metformineImage" alt="Metformine" />
              <div class="medicament-category diabete">
                Antidiabétique
              </div>
            </div>
            <div class="medicament-content">
              <h3 class="medicament-title">Metformine</h3>
              <p class="medicament-description">
                Médicament utilisé pour le traitement du diabète de type 2.
              </p>
              <div class="medicament-meta">
                <span class="dosage">850 mg</span>
                <span class="forme">Comprimé</span>
              </div>
            </div>
          </BaseCard>
        </div>
      </div>
    </section>
    <!-- Pharmacies Section -->
    <section id="pharmacies" class="pharmacies-section">
      <div class="container">
        <div class="section-header">
          <h2 class="section-title">Nos pharmacies</h2>
          <p class="section-subtitle">
            Découvrez les pharmacies les plus proches de vous
          </p>
        </div>

        <div class="pharmacies-grid">
          <!-- Pharmacie 1 -->
          <BaseCard class="pharmacy-card" variant="elevated">
            <div class="pharmacy-image">
              <img :src="phar1Image" alt="Pharmacie 1" />
              <div class="pharmacy-status open">
                Ouvert
              </div>
            </div>
            <div class="pharmacy-content">
              <h3 class="pharmacy-title">pharmacies de Gade</h3>
              <p class="pharmacy-address">
                Place de Gade, Cocody, Abidjan
              </p>
              <div class="pharmacy-meta">
                <span class="phone">+225 21 23 45 67</span>
                <span class="hours">24:00 - 24:00</span>
              </div>
            </div>
          </BaseCard>

          <!-- Pharmacie 2 -->
          <BaseCard class="pharmacy-card" variant="elevated">
            <div class="pharmacy-image">
              <img :src="phar2Image" alt="Pharmacie 2" />
              <div class="pharmacy-status open">
                Ouvert
              </div>
            </div>
            <div class="pharmacy-content">
              <h3 class="pharmacy-title">Pharmacies paul</h3>
              <p class="pharmacy-address">
                Boulevard de la République, Plateau, Abidjan
              </p>
              <div class="pharmacy-meta">
                <span class="phone">+225 21 98 76 54</span>
                <span class="hours">08:00 - 20:00</span>
              </div>
            </div>
          </BaseCard>

          <!-- Pharmacie 3 -->
          <BaseCard class="pharmacy-card" variant="elevated">
            <div class="pharmacy-image">
              <img :src="phar3Image" alt="Pharmacie 3" />
              <div class="pharmacy-status closed">
                Fermé
              </div>
            </div>
            <div class="pharmacy-content">
              <h3 class="pharmacy-title">Pharmacies de Riviera</h3>
              <p class="pharmacy-address">
                Rue des Martyrs, Riviera 2, Abidjan
              </p>
              <div class="pharmacy-meta">
                <span class="phone">+225 21 12 34 56</span>
                <span class="hours">08:00 - 20:00</span>
              </div>
            </div>
          </BaseCard>
        </div>
      </div>
    </section>
    <!-- réservations Section -->
    <section id="reservations" class="reservations-section">
      <div class="container">
        <div class="section-header">
          <h2 class="section-title">Réservations</h2>
          <p class="section-subtitle">
            Réservez votre rendez-vous en ligne
          </p>
        </div>
      </div>
    </section>

    <!-- Réservation Section -->
    <section id="reservation" class="reservation-section">
      <div class="container">
        <div class="reservation-cta">
          <h2 class="cta-title">Besoin de médicaments ?</h2>
          <p class="cta-subtitle">
            Réservez en ligne et récupérez en pharmacie ou choisissez la livraison par Yango Moto
          </p>
          <BaseButton size="extra-large" class="cta-button">
            Faire une réservation
          </BaseButton>
        </div>
      </div>
    </section>
    <!-- Ordonnance Section -->
    <section id="ordonnance" class="ordonnance-section">
      <div class="container">
        <div class="section-header ordonnance-header">
          <span class="ordonnance-eyebrow">Dépôt en ligne</span>
          <h2 class="section-title">Ordonnance</h2>
          <p class="section-subtitle ordonnance-subtitle">
            Déposez votre ordonnance et choisissez la pharmacie la plus proche de vous
          </p>
        </div>

        <div class="ordonnance-grid">
          <BaseCard class="ordonnance-card" variant="elevated">
            <div class="ordonnance-image-wrap">
              <div class="ordonnance-image">
                <img :src="ord1Image" alt="Ordonnance — pharmacies de Gade" />
              </div>
              <div class="ordonnance-status open">
                <span class="status-dot" aria-hidden="true" />
                Ouvert
              </div>
            </div>
            <div class="ordonnance-content">
              <h3 class="ordonnance-title">pharmacies de Gade</h3>
              <p class="ordonnance-address">
                <svg class="ordonnance-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                  <use xlink:href="#map-pin" />
                </svg>
                Place de Gade, Cocody, Abidjan
              </p>
              <div class="ordonnance-meta">
                <span class="ordonnance-meta-item phone">
                  <svg class="ordonnance-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                    <use xlink:href="#phone" />
                  </svg>
                  +225 21 23 45 67
                </span>
                <span class="ordonnance-meta-item hours">
                  <svg class="ordonnance-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                    <use xlink:href="#clock" />
                  </svg>
                  24:00 - 24:00
                </span>
              </div>
            </div>
          </BaseCard>

          <BaseCard class="ordonnance-card" variant="elevated">
            <div class="ordonnance-image-wrap">
              <div class="ordonnance-image">
                <img :src="ord2Image" alt="Ordonnance — Pharmacies paul" />
              </div>
              <div class="ordonnance-status open">
                <span class="status-dot" aria-hidden="true" />
                Ouvert
              </div>
            </div>
            <div class="ordonnance-content">
              <h3 class="ordonnance-title">Pharmacies paul</h3>
              <p class="ordonnance-address">
                <svg class="ordonnance-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                  <use xlink:href="#map-pin" />
                </svg>
                Boulevard de la République, Plateau, Abidjan
              </p>
              <div class="ordonnance-meta">
                <span class="ordonnance-meta-item phone">
                  <svg class="ordonnance-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                    <use xlink:href="#phone" />
                  </svg>
                  +225 21 98 76 54
                </span>
                <span class="ordonnance-meta-item hours">
                  <svg class="ordonnance-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                    <use xlink:href="#clock" />
                  </svg>
                  08:00 - 20:00
                </span>
              </div>
            </div>
          </BaseCard>

          <BaseCard class="ordonnance-card" variant="elevated">
            <div class="ordonnance-image-wrap">
              <div class="ordonnance-image">
                <img :src="ord3Image" alt="Ordonnance — Pharmacies de Riviera" />
              </div>
              <div class="ordonnance-status closed">
                <span class="status-dot" aria-hidden="true" />
                Fermé
              </div>
            </div>
            <div class="ordonnance-content">
              <h3 class="ordonnance-title">Pharmacies de Riviera</h3>
              <p class="ordonnance-address">
                <svg class="ordonnance-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                  <use xlink:href="#map-pin" />
                </svg>
                Rue des Martyrs, Riviera 2, Abidjan
              </p>
              <div class="ordonnance-meta">
                <span class="ordonnance-meta-item phone">
                  <svg class="ordonnance-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                    <use xlink:href="#phone" />
                  </svg>
                  +225 21 12 34 56
                </span>
                <span class="ordonnance-meta-item hours">
                  <svg class="ordonnance-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                    <use xlink:href="#clock" />
                  </svg>
                  08:00 - 20:00
                </span>
              </div>
            </div>
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
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

/* Hero Section */
.hero-section {
  height: 70vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  width: 100vw;
  margin-left: calc(50% - 50vw);
  margin-right: calc(50% - 50vw);
  padding: 0;
  position: relative;
  left: 0;
  right: 0;
  margin-bottom: 0;
}

.hero-content {
  text-align: center;
  max-width: 800px;
  margin: 0 auto;
  position: relative;
  z-index: 1;
  padding: 0 20px;
}

.hero-title {
  font-size: 56px;
  margin-bottom: 10px;
  color: white;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
}

.hero-subtitle {
  font-size: 18px;
  color: white;
  margin-bottom: 24px;
  line-height: 1.5;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
}

.hero-buttons {
  display: flex;
  gap: 16px;
  justify-content: center;
  flex-wrap: wrap;
}

.hero-buttons :deep(.base-button) {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

/* Features Section */
.features-section {
  padding: 40px 0 20px;
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

/* Médicaments Section */
.medicaments-section {
  padding: 30px 0 80px;
  background: #f8fafc;
}

.section-header {
  text-align: center;
  margin-bottom: 1.5rem;
}

.medicaments-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.medicament-card {
  overflow: hidden;
  transition: all 0.3s ease;
}

.medicament-card :deep(.base-card) {
  padding: 0;
}

.medicament-card:hover {
  transform: translateY(-8px);
}

.medicament-image {
  position: relative;
  height: 220px;
}

.medicament-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.medicament-category {
  position: absolute;
  top: 15px;
  right: 15px;
  color: white;
  padding: 6px 14px;
  border-radius: 30px;
  font-size: 0.8rem;
  font-weight: 600;
}

.antalgique {
  background: #10b981;
}

.antibiotique {
  background: #3b82f6;
}

.diabete {
  background: #f59e0b;
}

.medicament-content {
  padding: 1.25rem;
  background: white;
}

.medicament-title {
  font-size: 1.3rem;
  margin-bottom: 0.5rem;
  color: #111827;
  font-weight: 700;
  line-height: 1.2;
}

.medicament-description {
  color: #4b5563;
  line-height: 1.6;
  margin-bottom: 1rem;
  font-size: 0.95rem;
}

.medicament-meta {
  margin-top: 1rem;
  display: flex;
  justify-content: space-between;
  font-weight: 700;
  padding-top: 0.75rem;
  border-top: 1px solid #e5e7eb;
}

.dosage {
  color: #2563eb;
  font-size: 1rem;
}

.forme {
  color: #059669;
  font-size: 1rem;
}

/* Pharmacies Section */
.pharmacies-section {
  padding: 30px 0 80px;
  background: #ffffff;
}

.pharmacies-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.pharmacy-card {
  overflow: hidden;
  transition: all 0.3s ease;
}

.pharmacy-card :deep(.base-card) {
  padding: 0;
}

.pharmacy-card:hover {
  transform: translateY(-8px);
}

.pharmacy-image {
  position: relative;
  height: 220px;
}

.pharmacy-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.pharmacy-status {
  position: absolute;
  top: 15px;
  right: 15px;
  color: white;
  padding: 6px 14px;
  border-radius: 30px;
  font-size: 0.8rem;
  font-weight: 600;
}

.open {
  background: #10b981;
}

.closed {
  background: #ef4444;
}

.pharmacy-content {
  padding: 1.25rem;
  background: white;
}

.pharmacy-title {
  font-size: 1.3rem;
  margin-bottom: 0.5rem;
  color: #111827;
  font-weight: 700;
  line-height: 1.2;
}

.pharmacy-address {
  color: #4b5563;
  line-height: 1.6;
  margin-bottom: 1rem;
  font-size: 0.95rem;
}

.pharmacy-meta {
  margin-top: 1rem;
  display: flex;
  justify-content: space-between;
  font-weight: 700;
  padding-top: 0.75rem;
  border-top: 1px solid #e5e7eb;
}

.phone {
  color: #2563eb;
  font-size: 1rem;
}

.hours {
  color: #059669;
  font-size: 1rem;
}

/* Ordonnance Section */
.ordonnance-section {
  padding: 60px 0 80px;
  background: linear-gradient(180deg, #f8fafc 0%, #eef2ff 45%, #f8fafc 100%);
}

.ordonnance-header .ordonnance-eyebrow {
  display: inline-block;
  margin-bottom: 0.75rem;
  padding: 0.35rem 0.875rem;
  border-radius: 999px;
  background: rgba(37, 99, 235, 0.1);
  color: #2563eb;
  font-size: 0.8rem;
  font-weight: 700;
  letter-spacing: 0.04em;
  text-transform: uppercase;
}

.ordonnance-header .ordonnance-subtitle {
  max-width: 560px;
  margin-left: auto;
  margin-right: auto;
  margin-bottom: 3rem;
  line-height: 1.6;
}

.ordonnance-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.75rem;
  max-width: 1200px;
  margin: 0 auto;
}

.ordonnance-card {
  overflow: hidden;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  border-radius: 16px;
  border: 1px solid #e2e8f0;
  box-shadow: 0 4px 6px -1px rgba(15, 23, 42, 0.06), 0 2px 4px -2px rgba(15, 23, 42, 0.04);
}

.ordonnance-card :deep(.base-card) {
  padding: 0;
  background: white;
}

.ordonnance-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 20px 25px -5px rgba(15, 23, 42, 0.08), 0 8px 10px -6px rgba(15, 23, 42, 0.04);
}

.ordonnance-image-wrap {
  position: relative;
  padding: 1rem 1rem 0;
}

.ordonnance-image {
  position: relative;
  height: 280px;
  background: linear-gradient(145deg, #f8fafc 0%, #f1f5f9 100%);
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  overflow: hidden;
}

.ordonnance-image img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  object-position: center;
  padding: 0.75rem;
  box-sizing: border-box;
}

.ordonnance-status {
  position: absolute;
  top: 1.5rem;
  right: 1.5rem;
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.4rem 0.75rem;
  border-radius: 999px;
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.02em;
  backdrop-filter: blur(8px);
  box-shadow: 0 2px 8px rgba(15, 23, 42, 0.08);
}

.ordonnance-status.open {
  background: rgba(255, 255, 255, 0.95);
  color: #047857;
  border: 1px solid rgba(16, 185, 129, 0.25);
}

.ordonnance-status.closed {
  background: rgba(255, 255, 255, 0.95);
  color: #b91c1c;
  border: 1px solid rgba(239, 68, 68, 0.25);
}

.ordonnance-status .status-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  flex-shrink: 0;
}

.ordonnance-status.open .status-dot {
  background: #10b981;
  box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.2);
}

.ordonnance-status.closed .status-dot {
  background: #ef4444;
  box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.2);
}

.ordonnance-content {
  padding: 1.25rem 1.5rem 1.5rem;
  background: white;
  text-align: left;
}

.ordonnance-title {
  font-size: 1.2rem;
  margin-bottom: 0.625rem;
  color: #111827;
  font-weight: 700;
  line-height: 1.3;
}

.ordonnance-address {
  display: flex;
  align-items: flex-start;
  gap: 0.5rem;
  color: #64748b;
  line-height: 1.5;
  margin-bottom: 1rem;
  font-size: 0.9rem;
}

.ordonnance-icon {
  width: 16px;
  height: 16px;
  flex-shrink: 0;
  margin-top: 0.15rem;
}

.ordonnance-address .ordonnance-icon {
  color: #94a3b8;
}

.ordonnance-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  padding-top: 1rem;
  border-top: 1px solid #f1f5f9;
}

.ordonnance-meta-item {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  font-size: 0.875rem;
  font-weight: 600;
}

.ordonnance-meta-item.phone {
  color: #2563eb;
}

.ordonnance-meta-item.phone .ordonnance-icon {
  color: #2563eb;
}

.ordonnance-meta-item.hours {
  color: #059669;
}

.ordonnance-meta-item.hours .ordonnance-icon {
  color: #059669;
}

/* Réservation Section */
.reservation-section {
  padding: 60px 0;
  background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
  color: white;
}

.reservation-cta {
  text-align: center;
  max-width: 700px;
  margin: 0 auto;
}

.cta-title {
  font-size: 2.5rem;
  font-weight: 800;
  margin-bottom: 1rem;
  line-height: 1.2;
}

.cta-subtitle {
  font-size: 1.125rem;
  margin-bottom: 2rem;
  opacity: 0.95;
  line-height: 1.6;
}

.cta-button {
  background: white;
  color: #2563eb;
  font-weight: 700;
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
}

.cta-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
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

  .features-section {
    padding: 60px 0;
  }

  .ordonnance-grid {
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  }

  .ordonnance-section {
    padding: 50px 0 70px;
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

  .ordonnance-image {
    height: 240px;
  }

  .ordonnance-content {
    padding: 1rem 1.25rem 1.25rem;
  }

  .ordonnance-meta {
    flex-direction: column;
    gap: 0.5rem;
  }
}
</style>
