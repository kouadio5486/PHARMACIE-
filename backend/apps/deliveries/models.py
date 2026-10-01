from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from apps.users.models import User
from apps.reservations.models import Reservation


class Delivery(models.Model):
    """
    Gestion des livraisons :
    - Déclenchée par LA PHARMACIE après validation du paiement des médicaments
    - Suivi GPS en temps réel par le livreur
    - Paiement DE LA LIVRAISON effectué par le client au livreur (cash ou Mobile Money)
    """

    STATUS_EN_COURS = "en_cours"
    STATUS_LIVRE = "livre"
    STATUS_ANNULE = "annule"

    STATUS_CHOICES = [
        (STATUS_EN_COURS, "En cours"),
        (STATUS_LIVRE, "Livré"),
        (STATUS_ANNULE, "Annulé"),
    ]

    METHODE_PAIEMENT_ESPECES = "especes"
    METHODE_PAIEMENT_ORANGE = "orange_money"
    METHODE_PAIEMENT_MTN = "mtn"
    METHODE_PAIEMENT_WAVE = "wave"

    METHODE_PAIEMENT_CHOICES = [
        (METHODE_PAIEMENT_ESPECES, "Espèces (cash au livreur)"),
        (METHODE_PAIEMENT_ORANGE, "Orange Money"),
        (METHODE_PAIEMENT_MTN, "MTN Mobile Money"),
        (METHODE_PAIEMENT_WAVE, "Wave"),
    ]

    PAIEMENT_EN_ATTENTE = "en_attente"
    PAIEMENT_PAYE = "paye"
    PAIEMENT_ANNULE = "annule"

    PAIEMENT_STATUT_CHOICES = [
        (PAIEMENT_EN_ATTENTE, "En attente (à payer au livreur)"),
        (PAIEMENT_PAYE, "Payé"),
        (PAIEMENT_ANNULE, "Annulé"),
    ]

    reservation = models.ForeignKey(
        Reservation,
        on_delete=models.CASCADE,
        related_name="deliveries",
        verbose_name="Réservation",
    )

    livreur = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="deliveries",
        verbose_name="Livreur",
        limit_choices_to={"role": "livreur"},
    )

    # ===== Informations LIVRAISON =====
    montant_livraison = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Montant de la livraison (FCFA)",
        default=0,
        validators=[MinValueValidator(0)],
        help_text="Prix que le client paie au livreur (ex: 500 FCFA).",
    )

    adresse_livraison = models.TextField(
        blank=True,
        null=True,
        verbose_name="Adresse de livraison",
        help_text="Adresse complète où livrer les médicaments (indication : porte, bâtiment, repère GPS...).",
    )

    contact_client = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        verbose_name="Téléphone du client pour la livraison",
        help_text="Souvent différent du profil, pour un proche à qui on livre.",
    )

    # ===== SUIVI GPS =====
    latitude = models.FloatField(
        blank=True,
        null=True,
        verbose_name="Latitude (position livreur)",
        validators=[MinValueValidator(-90), MaxValueValidator(90)],
    )

    longitude = models.FloatField(
        blank=True,
        null=True,
        verbose_name="Longitude (position livreur)",
        validators=[MinValueValidator(-180), MaxValueValidator(180)],
    )

    # ===== STATUT LIVRAISON =====
    statut = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_EN_COURS,
        verbose_name="Statut de la livraison",
    )

    # ===== PAIEMENT DE LA LIVRAISON =====
    methode_paiement_livraison = models.CharField(
        max_length=30,
        choices=METHODE_PAIEMENT_CHOICES,
        default=METHODE_PAIEMENT_ESPECES,
        verbose_name="Méthode de paiement de la livraison",
        help_text="Le client paie la livraison au livreur par ce moyen.",
    )

    statut_paiement_livraison = models.CharField(
        max_length=30,
        choices=PAIEMENT_STATUT_CHOICES,
        default=PAIEMENT_EN_ATTENTE,
        verbose_name="Statut du paiement de la livraison",
        help_text="Devient « Payé » quand le livreur confirme avoir reçu l'argent.",
    )

    # ===== Dates =====
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de création",
    )

    livree_a = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="Date de livraison effective",
    )

    class Meta:
        db_table = "deliveries"
        verbose_name = "Livraison"
        verbose_name_plural = "Livraisons"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["livreur", "statut"]),
            models.Index(fields=["statut_paiement_livraison"]),
            models.Index(fields=["reservation"]),
        ]

    def __str__(self):
        return (
            f"Livraison #{self.id} - "
            f"{self.reservation.medicament.nom} ({self.reservation.quantite}) → "
            f"Client : {self.reservation.user.nom} {self.reservation.user.prenom} - "
            f"Livreur : {self.livreur.nom} - "
            f"{self.montant_livraison} FCFA - {self.get_statut_display()}"
        )