from django.db import models
from apps.users.models import User
from apps.pharmacies.models import Pharmacie
from apps.medicaments.models import Medicament


class Reservation(models.Model):
    """
    Réservation de médicaments en pharmacie.

    Flow :
    1. Patient réserve + indique besoin_livraison
    2. Si besoin_livraison : paie les médicaments en ligne → l'argent va à LA PHARMACIE
    3. Pharmacie valide → crée une livraison (Delivery) avec montant_livraison et adresse
    4. Livreur livre → PATIENT PAYE LA LIVRAISON au livreur (cash ou Mobile Money)
    """

    STATUS_PENDING = "pending"
    STATUS_CONFIRMED = "confirmed"
    STATUS_CANCELLED = "cancelled"
    STATUS_DONE = "done"

    STATUS_CHOICES = [
        (STATUS_PENDING, "En attente"),
        (STATUS_CONFIRMED, "Confirmée"),
        (STATUS_CANCELLED, "Annulée"),
        (STATUS_DONE, "Terminée"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reservations",
        verbose_name="Patient",
    )

    pharmacie = models.ForeignKey(
        Pharmacie,
        on_delete=models.CASCADE,
        related_name="reservations",
        verbose_name="Pharmacie",
    )

    medicament = models.ForeignKey(
        Medicament,
        on_delete=models.CASCADE,
        related_name="reservations",
        verbose_name="Médicament",
    )

    quantite = models.PositiveIntegerField(
        verbose_name="Quantité",
    )

    # ===== OPTION LIVRAISON =====
    besoin_livraison = models.BooleanField(
        default=False,
        verbose_name="Besoin de livraison à domicile",
        help_text="Si coché : la pharmacie organisera une livraison après paiement des médicaments. Le client paie la livraison au livreur.",
    )

    adresse_livraison = models.TextField(
        blank=True,
        null=True,
        verbose_name="Adresse de livraison souhaitée",
        help_text="Pré-remplie par le patient si besoin_livraison = True. La pharmacie peut modifier avant création de la livraison.",
    )

    contact_livraison = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        verbose_name="Téléphone contact pour la livraison",
    )

    # ===== STATUT =====
    statut = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
        verbose_name="Statut",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de création",
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Dernière mise à jour",
    )

    class Meta:
        db_table = "reservations"
        verbose_name = "Réservation"
        verbose_name_plural = "Réservations"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user", "statut"]),
            models.Index(fields=["pharmacie", "statut"]),
            models.Index(fields=["besoin_livraison"]),
        ]

    def __str__(self):
        livraison_txt = " (à livrer)" if self.besoin_livraison else " (sur place)"
        return f"{self.user} - {self.medicament} ({self.quantite}){livraison_txt}"

    # ===== PRIX DES MÉDICAMENTS (sans livraison) =====
    @property
    def total_prix(self):
        stock = self.medicament.stocks.filter(pharmacie=self.pharmacie).first()
        if stock:
            return self.quantite * stock.prix
        return 0

    # ===== EST-CE QUE CETTE RÉSERVATION A DÉJÀ ÉTÉ PAYÉE ? =====
    @property
    def paiement_medicaments_ok(self):
        return self.payments.filter(
            type_paiement="medicaments",
            statut="success",
        ).exists()

    # ===== EST-CE QU'UNE LIVRAISON EXISTE DÉJÀ ? =====
    @property
    def a_livraison(self):
        return self.deliveries.exists()