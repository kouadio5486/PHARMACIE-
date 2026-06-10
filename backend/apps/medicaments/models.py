from django.db import models


class Medicament(models.Model):
    """
    Médicaments disponibles dans les pharmacies.
    Le prix est géré dans la table Stock.
    """

    nom = models.CharField(
        max_length=255,
        verbose_name="Nom du médicament",
    )

    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Description",
    )

    dosage = models.CharField(
        max_length=100,
        verbose_name="Dosage",
        help_text="Ex : 500mg, 1g, etc."
    )

    image = models.ImageField(
        upload_to="medicaments/",
        blank=True,
        null=True,
        verbose_name="Image",
    )

    laboratoire = models.CharField(
        max_length=255,
        verbose_name="Laboratoire",
    )

    qr_code = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="QR Code",
        help_text="Code unique permettant de vérifier l'authenticité du médicament."
    )

    categorie = models.CharField(
        max_length=150,
        blank=True,
        verbose_name="Catégorie",
    )

    ordonnance_requise = models.BooleanField(
        default=False,
        verbose_name="Ordonnance requise",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de création",
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Date de modification",
    )

    class Meta:
        db_table = "medicaments"
        verbose_name = "Médicament"
        verbose_name_plural = "Médicaments"
        ordering = ["nom"]

    def __str__(self):
        return f"{self.nom} - {self.dosage}"