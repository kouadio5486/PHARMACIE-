from django.db import models
from apps.users.models import User
from apps.pharmacies.models import Pharmacie
from apps.medicaments.models import Medicament


class Reservation(models.Model):
    """
    Réservation de médicaments en pharmacie.
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
        verbose_name="Utilisateur",
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

    class Meta:
        db_table = "reservations"
        verbose_name = "Réservation"
        verbose_name_plural = "Réservations"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} - {self.medicament} ({self.quantite})"

    # ==========================
    # PRIX TOTAL (IMPORTANT)
    # ==========================
    @property
    def total_prix(self):
        stock = self.medicament.stocks.filter(pharmacie=self.pharmacie).first()

        if stock:
            return self.quantite * stock.prix

        return 0