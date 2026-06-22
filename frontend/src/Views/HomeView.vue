<script setup lang="ts">
import { onMounted } from 'vue'
import BaseButton from '../components/BaseButton.vue'
import BaseCard from '../components/BaseCard.vue'
import heroImage from '../assets/phar.jpg'
import paracetamolImage from '../assets/image/paracetamol.png'
import amoxicillineImage from '../assets/image/amoxicilline.png'
import metformineImage from '../assets/image/metformine.png'
import phar1Image from '../assets/image/pha1.webp'
import phar2Image from '../assets/image/phar2.jpg'
import phar3Image from '../assets/image/phar3.avif'

// Toggle delivery address based on selected mode
onMounted(() => {
  const modeInputs = document.querySelectorAll('input[name="mode"]')
  const deliveryGroup = document.getElementById('deliveryAddressGroup')

  modeInputs.forEach((input) => {
    input.addEventListener('change', () => {
      if (deliveryGroup) {
        deliveryGroup.style.display = (input as HTMLInputElement).value === 'delivery' ? 'block' : 'none'
      }
    })
  })
})

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
        <div class="section-header">
          <h2 class="section-title">Réserver un médicament</h2>
          <p class="section-subtitle">
            Réservez vos médicaments en ligne et récupérez-les en pharmacie
          </p>
        </div>

        <div class="reservation-form-container">
          <BaseCard class="reservation-card">
            <form class="reservation-form">
              <div class="form-group">
                <label for="medicament">Médicament</label>
                <select id="medicament" class="form-input">
                  <option value="">Choisissez un médicament</option>
                  <option value="paracetamol">Paracétamol 500mg</option>
                  <option value="amoxicilline">Amoxicilline 500mg</option>
                  <option value="metformine">Metformine 850mg</option>
                </select>
              </div>

              <div class="form-group">
                <label for="pharmacie">Pharmacie</label>
                <select id="pharmacie" class="form-input">
                  <option value="">Choisissez une pharmacie</option>
                  <option value="gare">Pharmacie de la Gare</option>
                  <option value="leclerc">Pharmacie Leclerc</option>
                  <option value="riviera">Pharmacie de Riviera</option>
                </select>
              </div>

              <div class="form-group">
                <label for="nom">Nom complet</label>
                <input type="text" id="nom" class="form-input" placeholder="Votre nom complet" />
              </div>

              <div class="form-group">
                <label for="phone">Numéro de téléphone</label>
                <input type="tel" id="phone" class="form-input" placeholder="+225 XX XX XX XX XX" />
              </div>

              <div class="form-group">
                <label for="quantity">Quantité</label>
                <input type="number" id="quantity" class="form-input" min="1" value="1" />
              </div>

              <div class="form-group">
                <label>Mode de récupération</label>
                <div class="radio-group">
                  <label class="radio-option">
                    <input type="radio" name="mode" value="pickup" checked />
                    <span>Retrait en pharmacie</span>
                  </label>
                  <label class="radio-option">
                    <input type="radio" name="mode" value="delivery" />
                    <span>Livraison par Yango Moto</span>
                  </label>
                </div>
              </div>

              <div class="form-group delivery-address" id="deliveryAddressGroup" style="display: none;">
                <label for="address">Adresse de livraison</label>
                <textarea id="address" class="form-input" rows="3" placeholder="Votre adresse complète"></textarea>
              </div>

              <div class="form-group">
                <label for="date">Date souhaitée</label>
                <input type="date" id="date" class="form-input" />
              </div>

              <div class="form-actions">
                <BaseButton type="submit" size="large" class="submit-btn">
                  Confirmer la réservation
                </BaseButton>
              </div>
            </form>
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

/* Réservation Section */
.reservation-section {
  padding: 30px 0 80px;
  background: #f8fafc;
}

.reservation-form-container {
  max-width: 600px;
  margin: 0 auto;
}

.reservation-card :deep(.base-card) {
  padding: 2rem;
}

.reservation-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-size: 1rem;
  font-weight: 600;
  color: #111827;
}

.form-input {
  padding: 0.875rem 1rem;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
  background: white;
}

.form-input:focus {
  outline: none;
  border-color: #2563eb;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
}

.radio-group {
  display: flex;
  gap: 1.5rem;
  flex-wrap: wrap;
}

.radio-option {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
}

.radio-option input[type="radio"] {
  width: 1.25rem;
  height: 1.25rem;
  accent-color: #2563eb;
}

.radio-option span {
  font-size: 1rem;
  color: #111827;
}

.form-actions {
  margin-top: 0.5rem;
}

.submit-btn {
  width: 100%;
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
