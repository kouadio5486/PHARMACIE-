from django.contrib import admin

from .models import Pharmacie, Ville


@admin.register(Ville)
class VilleAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "type",
        "code",
        "nom",
        "district",
        "region",
        "population",
        "is_active",
        "created_at",
    )
    list_filter = ("type", "is_active", "district", "region")
    search_fields = ("code", "nom", "district", "region", "slug")
    ordering = ("type", "nom")
    readonly_fields = ("slug", "created_at", "updated_at")
    list_per_page = 30
    fieldsets = (
        (
            "Identification",
            {
                "fields": (
                    "type",
                    "nom",
                    "code",
                    "slug",
                ),
            },
        ),
        (
            "Organisation",
            {
                "fields": (
                    "district",
                    "region",
                    "population",
                    "is_active",
                ),
            },
        ),
        (
            "Localisation GPS",
            {
                "fields": (
                    "latitude",
                    "longitude",
                ),
            },
        ),
        (
            "Dates",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                ),
            },
        ),
    )


@admin.register(Pharmacie)
class PharmacieAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "nom",
        "ville",
        "localite_libre",
        "commune",
        "telephone",
        "email",
        "responsable",
        "is_active",
        "is_pharmacie_de_garde",
        "note_moyenne",
        "created_at",
    )

    list_filter = (
        "ville__type",
        "ville",
        "localite_libre",
        "commune",
        "is_active",
        "is_pharmacie_de_garde",
        "created_at",
    )

    search_fields = (
        "nom",
        "ville__nom",
        "localite_libre",
        "commune",
        "adresse",
        "telephone",
        "email",
        "responsable__nom",
        "responsable__prenom",
    )

    ordering = ("-created_at",)
    list_per_page = 20

    readonly_fields = (
        "created_at",
        "updated_at",
        "note_moyenne",
    )

    fieldsets = (
        (
            " Informations générales",
            {
                "fields": (
                    "nom",
                    "responsable",
                    "description",
                    "image",
                )
            },
        ),
        (
            " Localisation",
            {
                "fields": (
                    "ville",
                    "localite_libre",
                    "commune",
                    "adresse",
                    "latitude",
                    "longitude",
                ),
                "description": (
                    "Règle : remplissez « ville » pour une localité référencée "
                    "(ville/commune/village existant dans la base). "
                    "Sinon, laissez « ville » vide et écrivez le nom du village "
                    "dans « localite_libre ». Le GPS est obligatoire."
                ),
            },
        ),
        (
            " Contact",
            {
                "fields": (
                    "telephone",
                    "email",
                )
            },
        ),
        (
            " Horaires",
            {
                "fields": (
                    "horaire_ouverture",
                    "horaire_fermeture",
                )
            },
        ),
        (
            " Statut",
            {
                "fields": (
                    "is_active",
                    "is_pharmacie_de_garde",
                )
            },
        ),
        (
            " Système",
            {
                "fields": (
                    "note_moyenne",
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )
