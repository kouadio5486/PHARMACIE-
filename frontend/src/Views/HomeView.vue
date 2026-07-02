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
        <div class="section-header">
          <h2 class="section-title">Ordonnance</h2>
          <p class="section-subtitle">
            Réservez votre ordonnance en ligne
          </p>
        </div>

        <div class="ordonnance-grid">
          <BaseCard class="ordonnance-card" variant="elevated">
            <div class="ordonnance-image">
              <img :src="ord1Image" alt="Pharmacies de Gade" />
              <div class="ordonnance-status open">
                Ouvert
              </div>
            </div>
            <div class="ordonnance-content">
              <h3 class="ordonnance-title">pharmacies de Gade</h3>
              <p class="ordonnance-address">
                Place de Gade, Cocody, Abidjan
              </p>
              <div class="ordonnance-meta">
                <span class="phone">+225 21 23 45 67</span>
                <span class="hours">24:00 - 24:00</span>
              </div>
            </div>
          </BaseCard>

          <BaseCard class="ordonnance-card" variant="elevated">
            <div class="ordonnance-image">
              <img :src="ord2Image" alt="Pharmacies paul" />
              <div class="ordonnance-status open">
                Ouvert
              </div>
            </div>
            <div class="ordonnance-content">
              <h3 class="ordonnance-title">Pharmacies paul</h3>
              <p class="ordonnance-address">
                Boulevard de la République, Plateau, Abidjan
              </p>
              <div class="ordonnance-meta">
                <span class="phone">+225 21 98 76 54</span>
                <span class="hours">08:00 - 20:00</span>
              </div>
            </div>
          </BaseCard>

          <BaseCard class="ordonnance-card" variant="elevated">
            <div class="ordonnance-image">
              <img :src="ord3Image" alt="Pharmacies de Riviera" />
              <div class="ordonnance-status closed">
                Fermé
              </div>
            </div>
            <div class="ordonnance-content">
              <h3 class="ordonnance-title">Pharmacies de Riviera</h3>
              <p class="ordonnance-address">
                Rue des Martyrs, Riviera 2, Abidjan
              </p>
              <div class="ordonnance-meta">
                <span class="phone">+225 21 12 34 56</span>
                <span class="hours">08:00 - 20:00</span>
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
  padding: 30px 0 80px;
  background: #f8fafc;
}

.ordonnance-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.ordonnance-card {
  overflow: hidden;
  transition: all 0.3s ease;
  border-radius: 12px;
}

.ordonnance-card :deep(.base-card) {
  padding: 0;
}

.ordonnance-card:hover {
  transform: translateY(-8px);
}

.ordonnance-image {
  position: relative;
  height: 220px;
  border-radius: 12px 12px 0 0;
  overflow: hidden;
}

.ordonnance-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.ordonnance-status {
  position: absolute;
  top: 15px;
  right: 15px;
  color: white;
  padding: 6px 14px;
  border-radius: 30px;
  font-size: 0.8rem;
  font-weight: 600;
}

.ordonnance-content {
  padding: 1.25rem;
  background: white;
  text-align: center;
}

.ordonnance-title {
  font-size: 1.3rem;
  margin-bottom: 0.5rem;
  color: #111827;
  font-weight: 700;
  line-height: 1.2;
}

.ordonnance-address {
  color: #4b5563;
  line-height: 1.6;
  margin-bottom: 1rem;
  font-size: 0.95rem;
}

.ordonnance-meta {
  margin-top: 1rem;
  display: flex;
  justify-content: space-between;
  font-weight: 700;
  padding-top: 0.75rem;
  border-top: 1px solid #e5e7eb;
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
