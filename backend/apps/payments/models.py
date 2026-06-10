from django.db import models

from apps.reservations.models import Reservation


class Payment(models.Model):
    """
    Gestion des paiements des réservations.
    """

    METHODE_ORANGE_MONEY = "orange_money"
    METHODE_MTN = "mtn"
    METHODE_WAVE = "wave"
    METHODE_CARTE = "carte"

    METHODE_CHOICES = [
        (METHODE_ORANGE_MONEY, "Orange Money"),
        (METHODE_MTN, "MTN Mobile Money"),
        (METHODE_WAVE, "Wave"),
        (METHODE_CARTE, "Carte Bancaire"),
    ]

    STATUS_PENDING = "pending"
    STATUS_SUCCESS = "success"
    STATUS_FAILED = "failed"

    STATUS_CHOICES = [
        (STATUS_PENDING, "En attente"),
        (STATUS_SUCCESS, "Succès"),
        (STATUS_FAILED, "Échec"),
    ]

    reservation = models.ForeignKey(
        Reservation,
        on_delete=models.CASCADE,
        related_name="payments",
        verbose_name="Réservation",
    )

    montant = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name="Montant",
        help_text="Montant payé en FCFA",
    )

    methode = models.CharField(
        max_length=20,
        choices=METHODE_CHOICES,
        verbose_name="Méthode de paiement",
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
        db_table = "payments"
        verbose_name = "Paiement"
        verbose_name_plural = "Paiements"
        ordering = ["-created_at"]

    def __str__(self):
        return (
            f"Paiement #{self.id} - "
            f"{self.montant} FCFA - "
            f"{self.get_statut_display()}"
        )