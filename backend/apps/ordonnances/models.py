from django.db import models
from apps.users.models import User
from apps.pharmacies.models import Pharmacie


class Ordonnance(models.Model):
    """
    Gestion des ordonnances médicales uploadées par les patients
    et validées par les pharmaciens.

    Workflow :
    1. Patient compare les prix d'un médicament → choisit une pharmacie
    2. Patient dépose son ordonnance auprès de CETTE pharmacie
    3. Pharmacien valide ou refuse
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
        verbose_name="Patient",
    )

    pharmacie = models.ForeignKey(
        Pharmacie,
        on_delete=models.CASCADE,
        related_name="ordonnances",
        verbose_name="Pharmacie chargée du traitement",
        help_text="La pharmacie choisie par le patient (souvent la moins chère).",
        null=True,
        blank=True,
    )

    fichier = models.FileField(
        upload_to="ordonnances/",
        verbose_name="Fichier ordonnance",
    )

    medicaments_extraits = models.JSONField(
        blank=True,
        null=True,
        verbose_name="Médicaments extraits",
        help_text="Médicaments et quantités détectés sur l'ordonnance (OCR ou saisie manuelle). Format : [{nom, dosage, quantite}]",
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
        help_text="Commentaire du pharmacien lors de la validation ou du refus.",
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
        db_table = "ordonnances"
        verbose_name = "Ordonnance"
        verbose_name_plural = "Ordonnances"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["pharmacie", "statut"]),
            models.Index(fields=["user", "statut"]),
        ]

    def __str__(self):
        pharmacie_nom = self.pharmacie.nom if self.pharmacie else "Non affectée"
        return f"Ordonnance #{self.id} - {self.user} → {pharmacie_nom} ({self.get_statut_display()})"