from django.db import models
from apps.pharmacies.models import Pharmacie
from apps.medicaments.models import Medicament


class Stock(models.Model):
    """
    Stock des médicaments par pharmacie.
    """

    pharmacie = models.ForeignKey(
        Pharmacie,
        on_delete=models.CASCADE,
        related_name="stocks",
        verbose_name="Pharmacie",
    )

    medicament = models.ForeignKey(
        Medicament,
        on_delete=models.CASCADE,
        related_name="stocks",
        verbose_name="Médicament",
    )

    quantite = models.PositiveIntegerField(
        default=0,
        verbose_name="Quantité disponible",
    )

    prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Prix (FCFA)",
        help_text="Prix du médicament dans cette pharmacie",
    )

    seuil_alerte = models.PositiveIntegerField(
        default=5,
        verbose_name="Seuil d'alerte",
        help_text="Quantité minimale avant déclenchement d'une alerte",
    )

    date_mise_a_jour = models.DateTimeField(
        auto_now=True,
        verbose_name="Date de mise à jour",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de création",
    )

    class Meta:
        db_table = "stocks"
        verbose_name = "Stock"
        verbose_name_plural = "Stocks"
        ordering = ["pharmacie", "medicament"]

        #  VERSION PRO (remplace unique_together)
        constraints = [
            models.UniqueConstraint(
                fields=["pharmacie", "medicament"],
                name="unique_stock_par_pharmacie_medicament"
            )
        ]

        #  Index pour optimiser les requêtes
        indexes = [
            models.Index(fields=["pharmacie"]),
            models.Index(fields=["medicament"]),
            models.Index(fields=["date_mise_a_jour"]),
        ]

    def __str__(self):
        return f"{self.medicament.nom} - {self.pharmacie.nom} ({self.quantite})"

    @property
    def stock_faible(self):
        return self.quantite <= self.seuil_alerte