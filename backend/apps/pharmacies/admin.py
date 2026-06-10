from django.contrib import admin

from .models import Pharmacie, Ville


@admin.register(Ville)
class VilleAdmin(admin.ModelAdmin):
    list_display = ("id", "code", "nom", "district", "region", "is_active", "created_at")
    list_filter = ("is_active", "district", "region")
    search_fields = ("code", "nom", "district", "region", "slug")
    ordering = ("nom",)
    readonly_fields = ("slug", "created_at", "updated_at")
    fieldsets = (
        ("Identification", {"fields": ("nom", "code", "slug")}),
        ("Organisation", {"fields": ("district", "region", "is_active")}),
        ("Localisation", {"fields": ("latitude", "longitude")}),
        ("Dates", {"fields": ("created_at", "updated_at")}),
    )


@admin.register(Pharmacie)
class PharmacieAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "nom",
        "ville",
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
        "ville",
        "commune",
        "is_active",
        "is_pharmacie_de_garde",
        "created_at",
    )

    search_fields = (
        "nom",
        "ville__nom",
        "commune",
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
                    "commune",
                    "adresse",
                    "latitude",
                    "longitude",
                )
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
