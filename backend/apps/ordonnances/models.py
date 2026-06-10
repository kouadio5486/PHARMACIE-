from django.db import models
from apps.users.models import User


class Ordonnance(models.Model):
    """
    Gestion des ordonnances médicales uploadées par les patients
    et validées par les pharmaciens.
    """

    STATUT_EN_ATTENTE = "en_attente"
    STATUT_VALIDEE = "validee"
    STATUT_REFUSEE = "refusee"

    STATUT_CHOICES = [
        (STATUT_EN_ATTENTE, "En attente"),
        (STATUT_VALIDEE, "Validée"),
        (STATUT_REFUSEE, "Refusée"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="ordonnances",
        verbose_name="Utilisateur",
    )

    fichier = models.FileField(
        upload_to="ordonnances/",
        verbose_name="Fichier ordonnance",
    )

    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default=STATUT_EN_ATTENTE,
        verbose_name="Statut",
    )

    commentaire = models.TextField(
        blank=True,
        null=True,
        verbose_name="Commentaire",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de création",
    )

    class Meta:
        db_table = "ordonnances"
        verbose_name = "Ordonnance"
        verbose_name_plural = "Ordonnances"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Ordonnance #{self.id} - {self.user}"