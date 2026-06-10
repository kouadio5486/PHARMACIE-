from django.db import models

from apps.users.models import User
from apps.reservations.models import Reservation


class Delivery(models.Model):
    """
    Gestion des livraisons avec suivi GPS des livreurs.
    """

    STATUS_EN_COURS = "en_cours"
    STATUS_LIVRE = "livre"
    STATUS_ANNULE = "annule"

    STATUS_CHOICES = [
        (STATUS_EN_COURS, "En cours"),
        (STATUS_LIVRE, "Livré"),
        (STATUS_ANNULE, "Annulé"),
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

    latitude = models.FloatField(
        blank=True,
        null=True,
        verbose_name="Latitude",
    )

    longitude = models.FloatField(
        blank=True,
        null=True,
        verbose_name="Longitude",
    )

    statut = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_EN_COURS,
        verbose_name="Statut",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de création",
    )

    class Meta:
        db_table = "deliveries"
        verbose_name = "Livraison"
        verbose_name_plural = "Livraisons"
        ordering = ["-created_at"]

    def __str__(self):
        return (
            f"Livraison #{self.id} - "
            f"{self.reservation.medicament.nom} - "
            f"{self.livreur.nom}"
        )