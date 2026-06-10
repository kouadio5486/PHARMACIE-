from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify

from apps.users.models import User


class Ville(models.Model):
    """Référentiel des villes de Côte d'Ivoire utilisé par l'application."""

    nom = models.CharField(max_length=100, unique=True, verbose_name="Nom de la ville")
    code = models.CharField(max_length=20, unique=True, blank=True, verbose_name="Code")
    slug = models.SlugField(max_length=120, unique=True, blank=True, verbose_name="Slug")
    district = models.CharField(max_length=120, blank=True, null=True, verbose_name="District")
    region = models.CharField(max_length=120, blank=True, null=True, verbose_name="Région")
    latitude = models.FloatField(blank=True, null=True, validators=[MinValueValidator(-90), MaxValueValidator(90)], verbose_name="Latitude")
    longitude = models.FloatField(blank=True, null=True, validators=[MinValueValidator(-180), MaxValueValidator(180)], verbose_name="Longitude")
    is_active = models.BooleanField(default=True, verbose_name="Active")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "villes"
        verbose_name = "Ville"
        verbose_name_plural = "Villes"
        ordering = ["nom"]

    def __str__(self):
        return self.nom

    def save(self, *args, **kwargs):
        base_slug = slugify(self.nom)
        if not self.slug:
            self.slug = base_slug
        if not self.code:
            self.code = base_slug.replace("-", "_").upper()[:20]
        super().save(*args, **kwargs)


class Pharmacie(models.Model):
    """
    Pharmacie partenaire de la plateforme PharmaCI.
    """

    #  Responsable de la pharmacie
    responsable = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="pharmacies",
        limit_choices_to={"role": "pharmacien"},
        verbose_name="Pharmacien responsable",
    )

    #  Infos générales
    nom = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="Nom de la pharmacie",
    )

    adresse = models.TextField(verbose_name="Adresse")

    ville = models.ForeignKey(
        Ville,
        on_delete=models.PROTECT,
        related_name="pharmacies",
        verbose_name="Ville",
    )

    commune = models.CharField(
        max_length=100,
        verbose_name="Commune / quartier",
        help_text="Quartier ou secteur (ex. Cocody à Abidjan, centre-ville à M'batto).",
    )

    telephone = models.CharField(
        max_length=20,
        verbose_name="Téléphone",
    )

    email = models.EmailField(
        unique=True,
        verbose_name="Email",
    )

    #  GPS
    latitude = models.FloatField(
        validators=[MinValueValidator(-90), MaxValueValidator(90)],
        verbose_name="Latitude",
    )

    longitude = models.FloatField(
        validators=[MinValueValidator(-180), MaxValueValidator(180)],
        verbose_name="Longitude",
    )

    #  Horaires
    horaire_ouverture = models.TimeField()
    horaire_fermeture = models.TimeField()

    #  Statut
    is_active = models.BooleanField(default=True)

    #  NOUVEAUX AJOUTS IMPORTANTS
    is_pharmacie_de_garde = models.BooleanField(
        default=False,
        verbose_name="Pharmacie de garde",
    )

    note_moyenne = models.FloatField(
        default=0.0,
        verbose_name="Note moyenne",
    )

    image = models.ImageField(
        upload_to="pharmacies/",
        blank=True,
        null=True,
        verbose_name="Image de la pharmacie",
    )

    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Description",
    )

    #  timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "pharmacies"
        verbose_name = "Pharmacie"
        verbose_name_plural = "Pharmacies"
        ordering = ["nom"]

    def __str__(self):
        return f"{self.nom} - {self.ville.nom} ({self.commune})"

    #  Permissions métier
    @property
    def permissions(self):
        return {
            "pharmacien": [
                "gestion_pharmacie",
                "gestion_stock",
                "validation_reservations",
                "gestion_horaires",
            ],
            "admin": [
                "gestion_toutes_pharmacies",
                "statistiques",
                "modification_globale",
            ],
            "patient": [
                "voir_pharmacies",
                "recherche",
            ],
        }
