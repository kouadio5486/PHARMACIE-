from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify

from apps.users.models import User


class Ville(models.Model):
    """
    Référentiel des localités de Côte d'Ivoire :
    - "ville"    : grande ville (Abidjan, Bouaké, Yamoussoukro...)
    - "commune"  : commune ou arrondissement (Cocody, Plateau, Abobo...)
    - "village"  : village ou zone rurale (Kouto, Tiébissou Est, Danané...)

    La même table regroupe les 3 types (même informations : nom, GPS, région...),
    ce qui permet d'ajouter progressivement toutes les localités sans nouveau modèle.
    """

    TYPE_VILLE = "ville"
    TYPE_COMMUNE = "commune"
    TYPE_VILLAGE = "village"

    TYPE_CHOICES = (
        (TYPE_VILLE, "Ville"),
        (TYPE_COMMUNE, "Commune"),
        (TYPE_VILLAGE, "Village"),
    )

    type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        default=TYPE_VILLE,
        verbose_name="Type de localité",
        help_text="Permet de distinguer les grandes villes des communes et villages.",
    )

    nom = models.CharField(max_length=120, unique=True, verbose_name="Nom de la localité")
    code = models.CharField(max_length=20, unique=True, blank=True, verbose_name="Code")
    slug = models.SlugField(max_length=140, unique=True, blank=True, verbose_name="Slug")
    district = models.CharField(max_length=120, blank=True, null=True, verbose_name="District")
    region = models.CharField(max_length=120, blank=True, null=True, verbose_name="Région")
    latitude = models.FloatField(blank=True, null=True, validators=[MinValueValidator(-90), MaxValueValidator(90)], verbose_name="Latitude")
    longitude = models.FloatField(blank=True, null=True, validators=[MinValueValidator(-180), MaxValueValidator(180)], verbose_name="Longitude")
    population = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name="Population approximative",
        help_text="Optionnel, utile pour prioriser les zones.",
    )
    is_active = models.BooleanField(default=True, verbose_name="Active")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "villes"
        verbose_name = "Localité (ville / commune / village)"
        verbose_name_plural = "Localités (villes / communes / villages)"
        ordering = ["type", "nom"]
        indexes = [
            models.Index(fields=["type", "is_active"]),
            models.Index(fields=["region", "type"]),
        ]

    def __str__(self):
        return f"{self.nom} ({self.get_type_display()})"

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
        null=True,
        blank=True
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
        verbose_name="Localité (ville / commune / village)",
        null=True,
        blank=True,
        help_text="Choisissez dans la liste si votre localité existe. Sinon, laissez vide et remplissez le champ « Localité (texte libre) » ci-dessous.",
    )

    localite_libre = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        verbose_name="Localité (texte libre)",
        help_text="Si votre village/commune n'est pas dans la liste déroulante du dessus : écrivez son nom ici (ex: Village Tiébissou, Kouto, Danané).",
    )

    commune = models.CharField(
        max_length=100,
        verbose_name="Commune / quartier / secteur",
        help_text="Précision dans la localité (ex: Cocody à Abidjan, centre-ville à M'batto, marché du village).",
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
        localite = None
        if self.ville:
            localite = str(self.ville)
        elif self.localite_libre:
            localite = self.localite_libre
        localite_txt = localite or "Localité non renseignée"
        return f"{self.nom} - {localite_txt} ({self.commune})"

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
